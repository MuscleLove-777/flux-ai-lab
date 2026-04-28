#!/usr/bin/env python3
"""GitHub Actions用一括実行スクリプト

キーワード選定 → 記事生成 → SEO最適化 → サイトビルド を一括実行する。
JSON-LD構造化データ（BlogPosting / FAQPage / BreadcrumbList）対応。
"""
import sys
import os
import json
import re
import time
import logging
from datetime import datetime
from pathlib import Path

# blog_engineへのパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Gemini APIリトライ設定
MAX_RETRIES = 5
RETRY_DELAY = 3  # 秒


def repair_json_text(text):
    """Gemini APIレスポンスからJSONを抽出・修復する"""
    if not text:
        return text

    # コードブロックの除去
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            text = parts[1]
        elif len(parts) >= 2:
            text = parts[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    # JSON部分のみ抽出（最初の { から最後の } まで）
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    first_bracket = text.find("[")
    last_bracket = text.rfind("]")

    if first_brace >= 0 and last_brace > first_brace:
        if first_bracket >= 0 and first_bracket < first_brace:
            text = text[first_bracket:last_bracket + 1]
        else:
            text = text[first_brace:last_brace + 1]
    elif first_bracket >= 0 and last_bracket > first_bracket:
        text = text[first_bracket:last_bracket + 1]

    # 制御文字の除去（改行・タブは残す）
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)

    # 末尾カンマの修復（JSON仕様違反）
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)

    return text.strip()


def parse_json_safe(text):
    """JSONパースを複数の方法で試行する"""
    repaired = repair_json_text(text)

    # strict=False でパース試行
    try:
        return json.loads(repaired, strict=False)
    except json.JSONDecodeError:
        pass

    # シングルクォートをダブルクォートに置換して再試行
    try:
        fixed = repaired.replace("'", '"')
        return json.loads(fixed, strict=False)
    except json.JSONDecodeError:
        pass

    raise json.JSONDecodeError(
        f"JSON修復失敗。元テキスト: {text[:200]}...", text, 0
    )


def call_gemini_json(client, model, prompt, response_schema=None):
    """Gemini APIを呼び出してJSONレスポンスを取得する（リトライ付き）"""
    from llm import get_llm_client
    from google.genai import types

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Gemini API呼び出し（試行 %d/%d）", attempt, MAX_RETRIES)

            # JSON出力を強制するconfig
            gen_config = types.GenerateContentConfig(
                response_mime_type="application/json",
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=gen_config,
            )
            response_text = response.text.strip()
            logger.info("Gemini APIレスポンス取得（%d文字）", len(response_text))

            data = parse_json_safe(response_text)
            return data

        except Exception as e:
            last_error = e
            logger.warning(
                "Gemini API試行 %d/%d 失敗: %s", attempt, MAX_RETRIES, e
            )
            if attempt < MAX_RETRIES:
                # 429 Rate Limit: wait longer based on retry-after hint
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    retry_match = re.search(r"retry(?:Delay|After)[^\d]*(\d+)", error_str, re.IGNORECASE)
                    wait_time = int(retry_match.group(1)) + 5 if retry_match else 60
                    logger.info("Rate limit hit, waiting %d seconds", wait_time)
                    time.sleep(wait_time)
                else:
                    time.sleep(RETRY_DELAY * attempt)

    raise last_error


def run(config, prompts=None):
    """メイン処理: キーワード選定 → 記事生成 → SEO最適化 → サイトビルド"""
    logger.info("=== %s 自動生成開始 ===", config.BLOG_NAME)
    start_time = datetime.now()

    # ステップ1: キーワード選定
    logger.info("ステップ1: キーワード選定")
    try:
        client = get_llm_client(config)

        if prompts and hasattr(prompts, "build_keyword_prompt"):
            prompt = prompts.build_keyword_prompt(config)
        else:
            categories_text = "\n".join(f"- {cat}" for cat in config.TARGET_CATEGORIES)
            prompt = (
                f"{config.BLOG_NAME}用のキーワードを選定してください。\n\n"
                "以下のカテゴリから1つ選び、そのカテゴリで今注目されている"
                "トピック・キーワードを1つ提案してください。\n\n"
                f"カテゴリ一覧:\n{categories_text}\n\n"
                "以下の形式でJSON形式のみで回答してください（説明不要）:\n"
                '{"category": "カテゴリ名", "keyword": "キーワード"}'
            )

        data = call_gemini_json(client, config.GEMINI_MODEL, prompt)

        # Geminiがリストで返す場合があるので先頭要素を取得
        if isinstance(data, list):
            data = data[0] if data else {}

        # 必須フィールドのデフォルト値設定
        import random
        category = data.get("category", random.choice(config.TARGET_CATEGORIES))
        keyword = data.get("keyword", f"{category} 最新情報 2026")
        logger.info("選定結果 - カテゴリ: %s, キーワード: %s", category, keyword)

    except Exception as e:
        logger.error("キーワード選定に失敗: %s", e)
        # フォールバック: ランダムにカテゴリとキーワードを選定
        import random
        category = random.choice(config.TARGET_CATEGORIES)
        keyword = f"{category} 最新情報 2026"
        logger.warning("フォールバック使用 - カテゴリ: %s, キーワード: %s", category, keyword)

    # ステップ2: 記事生成
    logger.info("ステップ2: 記事生成")
    try:
        from blog_engine.article_generator import ArticleGenerator
        from seo_optimizer import FluxSEOOptimizer

        generator = ArticleGenerator(config)
        article = generator.generate_article(
            keyword=keyword, category=category, prompts=prompts
        )
        logger.info("記事生成完了: %s", article.get("title", "不明"))

        optimizer = FluxSEOOptimizer(config)
        seo_result = optimizer.check_seo_score(article)
        article["seo_score"] = seo_result.get("total_score", 0)
        logger.info("SEOスコア: %d/100", article["seo_score"])

        # JSON-LD構造化データを記事に追加
        jsonld_scripts = optimizer.generate_all_jsonld(article)
        article["jsonld"] = jsonld_scripts
        logger.info("JSON-LD構造化データ: %d件生成", len(jsonld_scripts))

    except Exception as e:
        logger.error("記事生成に失敗: %s", e)
        sys.exit(1)

    # ステップ2.5: アフィリエイトリンク挿入
    logger.info("ステップ2.5: アフィリエイトリンク挿入")
    try:
        from blog_engine.affiliate import AffiliateManager
        affiliate_mgr = AffiliateManager(config)
        article = affiliate_mgr.insert_affiliate_links(article)
        logger.info("アフィリエイトリンク: %d件挿入", article.get("affiliate_count", 0))
    except Exception as aff_err:
        logger.warning("アフィリエイトリンク挿入をスキップ: %s", aff_err)

    # ステップ2.7: 記事JSONを再保存（SEOスコア・JSON-LD追加後）
    try:
        file_path = article.get("file_path")
        if file_path:
            save_data = {k: v for k, v in article.items() if k != "file_path"}
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            logger.info("記事を再保存しました: %s", file_path)
    except Exception as save_err:
        logger.warning("記事の再保存をスキップ: %s", save_err)

    # ステップ3: サイトビルド
    logger.info("ステップ3: サイトビルド")
    try:
        from site_generator import FluxSiteGenerator
        site_gen = FluxSiteGenerator(config)
        site_gen.build_site()
        logger.info("サイトビルド完了")
    except Exception as e:
        logger.error("サイトビルドに失敗: %s", e)
        sys.exit(1)

    # 完了
    duration = (datetime.now() - start_time).total_seconds()
    logger.info("=== 自動生成完了（%.1f秒） ===", duration)
    logger.info("  カテゴリ: %s", category)
    logger.info("  キーワード: %s", keyword)
    logger.info("  タイトル: %s", article.get("title", "不明"))
    logger.info("  SEOスコア: %d/100", article.get("seo_score", 0))


if __name__ == "__main__":
    # 直接実行時
    sys.path.insert(0, os.path.dirname(__file__))
    import config
    import prompts
    run(config, prompts)
