"""Flux AI画像生成ラボ - プロンプト定義

Black Forest Labs Flux特化ブログ用のプロンプトを一元管理する。
JSON-LD構造化データ（BlogPosting / FAQPage / BreadcrumbList）対応。
"""

# ペルソナ設定
PERSONA = (
    "あなたはAI画像生成の日本語エキスパートです。"
    "Black Forest Labs Fluxシリーズ（Flux.1 Pro/Dev/Schnell、Flux 2等）に精通し、"
    "Stable Diffusion・Midjourney・DALL-E 3との比較も客観的に行えるプロのテックライターです。"
    "ComfyUI・Replicate・fal.aiなどのツール連携に詳しく、"
    "初心者からクリエイターまで幅広い読者に実践的なプロンプトテクニックと活用法を届けます。"
    "DSLRレベルのフォトリアリズムを実現するFluxの強みを最大限に伝えることを重視します。"
)

# 記事フォーマット指示
ARTICLE_FORMAT = """
【記事構成（必ずこの順序で書くこと）】

## この記事でわかること
- ポイント1（具体的なベネフィット）
- ポイント2
- ポイント3

## 結論（先に結論を述べる）
（読者が最も知りたい答えを最初に提示）

## 本題（H2で3〜5セクション）
（具体的な手順・解説。プロンプト例はコードブロックで明示）

## プロンプトテクニック
（Flux特有のプロンプト構文・パラメータ設定のコツ）

## 他のAI画像生成ツールとの比較
（Midjourney / DALL-E 3 / Stable Diffusion との違いを表形式で整理）

## よくある質問（FAQ）
### Q1: （よくある質問1）
A1: （回答1）

### Q2: （よくある質問2）
A2: （回答2）

### Q3: （よくある質問3）
A3: （回答3）

## まとめ
（要点整理と次のアクション提案）
"""

# カテゴリ別SEOキーワードヒント
CATEGORY_PROMPTS = {
    "Flux 使い方": "Flux 使い方、Flux 始め方、Flux AI 画像生成、Flux 初心者、Flux.1 使い方、Black Forest Labs",
    "Flux 料金・プラン": "Flux 料金、Flux Pro 料金、Flux 無料 有料 違い、Flux API 料金、Flux クレジット",
    "Flux vs Midjourney": "Flux Midjourney 比較、Flux Midjourney 違い、AI画像生成 比較 2026、Flux DALL-E 比較",
    "Flux 最新ニュース": "Flux アップデート、Flux 2 新機能、Black Forest Labs 最新、Flux リリース",
    "Flux プロンプト術": "Flux プロンプト、Flux プロンプト 書き方、Flux プロンプト テクニック、DSLR風 プロンプト",
    "AI画像生成テクニック": "AI画像生成 テクニック、Flux ControlNet、Flux img2img、Flux インペイント、Flux LoRA",
    "Flux API": "Flux API、Flux API 使い方、Replicate Flux、fal.ai Flux、ComfyUI Flux",
    "Flux 活用事例": "Flux 商用利用、Flux ビジネス活用、Flux クリエイター、Flux 写真レベル、AI画像 仕事",
}

# ニュースソース
NEWS_SOURCES = [
    "Black Forest Labs Blog (https://blackforestlabs.ai/blog/)",
    "Replicate Blog (https://replicate.com/blog)",
    "Hugging Face (https://huggingface.co/black-forest-labs)",
    "TechCrunch AI (https://techcrunch.com/category/artificial-intelligence/)",
    "The Verge AI (https://www.theverge.com/ai-artificial-intelligence)",
]

# FAQ構造化データの有効化
FAQ_SCHEMA_ENABLED = True

# キーワード選定用の追加プロンプト
KEYWORD_PROMPT_EXTRA = (
    "Black Forest Labs Flux（AI画像生成）に関するキーワードを選んでください。\n"
    "日本のユーザーが検索しそうな実用的なキーワードを意識してください。\n"
    "「Flux 使い方」「Flux 料金」「Flux vs Midjourney」「Flux プロンプト」のような、\n"
    "検索ボリュームが見込めるキーワードを優先してください。"
)


def build_keyword_prompt(config):
    """キーワード選定プロンプトを構築する"""
    categories_text = "\n".join(f"- {cat}" for cat in config.TARGET_CATEGORIES)
    category_hints = "\n".join(
        f"- {cat}: {hints}" for cat, hints in CATEGORY_PROMPTS.items()
    )
    return (
        f"{PERSONA}\n\n"
        "Flux AI画像生成ラボ用のキーワードを選定してください。\n\n"
        f"{KEYWORD_PROMPT_EXTRA}\n\n"
        f"カテゴリ一覧:\n{categories_text}\n\n"
        f"カテゴリ別キーワードヒント:\n{category_hints}\n\n"
        "以下の形式でJSON形式のみで回答してください（説明不要）:\n"
        '{"category": "カテゴリ名", "keyword": "キーワード"}'
    )


def build_article_prompt(keyword, category, config):
    """Flux特化記事生成プロンプトを構築する"""
    category_hints = CATEGORY_PROMPTS.get(category, "")
    news_sources_text = "\n".join(f"- {src}" for src in NEWS_SOURCES)

    return f"""{PERSONA}

以下のキーワードに関する記事を、Flux AI画像生成の専門サイト向けに執筆してください。

【基本条件】
- ブログ名: {config.BLOG_NAME}
- キーワード: {keyword}
- カテゴリ: {category}
- カテゴリ関連キーワード: {category_hints}
- 言語: 日本語
- 文字数: {config.MAX_ARTICLE_LENGTH}文字程度

{ARTICLE_FORMAT}

【SEO要件】
1. タイトルにキーワード「{keyword}」を必ず含めること
2. タイトルは32文字以内で魅力的に（数字や年号を含めると効果的）
3. H2、H3の見出し構造を適切に使用すること
4. キーワード密度は{config.MIN_KEYWORD_DENSITY}%〜{config.MAX_KEYWORD_DENSITY}%を目安に
5. メタディスクリプションは{config.META_DESCRIPTION_LENGTH}文字以内
6. FAQ（よくある質問）を3つ以上含めること（FAQPage構造化データ対応）

【内部リンク】
- 内部リンクのプレースホルダーを2〜3箇所に配置（{{{{internal_link:関連トピック}}}}の形式）

【参考情報源】
{news_sources_text}

【条件】
- {config.MAX_ARTICLE_LENGTH}文字程度
- 2026年最新の情報を反映すること
- 具体的なプロンプト例やパラメータ設定を含める
- ComfyUI / Replicate / fal.ai などのツール連携方法を含める
- Midjourney / DALL-E 3 / Stable Diffusion との客観的な比較を含める
- 初心者にもわかりやすく、専門用語には補足説明を付ける
- DSLRレベルのフォトリアリズムがFluxの強みであることを随所で伝える

【出力形式】
以下のJSON形式で出力してください。JSONブロック以外のテキストは出力しないでください。

```json
{{
  "title": "SEO最適化されたタイトル",
  "content": "# タイトル\\n\\n本文（Markdown形式）...",
  "meta_description": "120文字以内のメタディスクリプション",
  "tags": ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"],
  "slug": "url-friendly-slug",
  "faq": [
    {{"question": "質問1", "answer": "回答1"}},
    {{"question": "質問2", "answer": "回答2"}},
    {{"question": "質問3", "answer": "回答3"}}
  ]
}}
```

【注意事項】
- content内のMarkdownは適切にエスケープしてJSON文字列として有効にすること
- tagsは5個ちょうど生成すること
- slugは半角英数字とハイフンのみ使用すること
- faqは3個以上生成すること（FAQPage構造化データに使用）
- 読者にとって実用的で具体的な内容を心がけること"""
