"""Flux AI画像生成ラボ - ブログ固有設定"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

BLOG_NAME = "Flux AI画像生成ラボ"
BLOG_DESCRIPTION = "Black Forest Labs Fluxの使い方・最新モデル・Midjourney比較を毎日更新。DSLRレベルのリアリズムを実現するAI画像生成を完全解説。"
BLOG_URL = "https://musclelove-777.github.io/flux-ai-lab"
BLOG_TAGLINE = "Fluxで実現するDSLRレベルのAI画像生成を完全ガイド"
BLOG_LANGUAGE = "ja"

GITHUB_REPO = "MuscleLove-777/flux-ai-lab"
GITHUB_BRANCH = "gh-pages"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

OUTPUT_DIR = BASE_DIR / "output"
ARTICLES_DIR = OUTPUT_DIR / "articles"
SITE_DIR = OUTPUT_DIR / "site"
TOPICS_DIR = OUTPUT_DIR / "topics"

TARGET_CATEGORIES = [
    "Flux 使い方",
    "Flux 料金・プラン",
    "Flux vs Midjourney",
    "Flux 最新ニュース",
    "Flux プロンプト術",
    "AI画像生成テクニック",
    "Flux API",
    "Flux 活用事例",
]

THEME = {
    "primary": "#ff6600",
    "accent": "#ff9900",
    "gradient_start": "#ff6600",
    "gradient_end": "#ff9900",
    "dark_bg": "#1a0f00",
    "dark_surface": "#2d1a00",
    "light_bg": "#fff8f0",
    "light_surface": "#ffffff",
}

MAX_ARTICLE_LENGTH = 4000
ARTICLES_PER_DAY = 1
SCHEDULE_HOURS = [12]

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

ENABLE_SEO_OPTIMIZATION = True
MIN_SEO_SCORE = 75
MIN_KEYWORD_DENSITY = 1.0
MAX_KEYWORD_DENSITY = 3.0
META_DESCRIPTION_LENGTH = 120
ENABLE_INTERNAL_LINKS = True

AFFILIATE_LINKS = {
    "Flux Pro": [
        {"service": "Flux Pro", "url": "https://blackforestlabs.ai", "description": "Flux Proに登録する"},
    ],
    "Replicate": [
        {"service": "Replicate", "url": "https://replicate.com", "description": "ReplicateでFluxを使う"},
    ],
    "fal.ai": [
        {"service": "fal.ai", "url": "https://fal.ai", "description": "fal.aiでFlux APIを使う"},
    ],
    "オンライン講座": [
        {"service": "Udemy", "url": "https://www.udemy.com", "description": "UdemyでAI画像生成講座を探す"},
    ],
    "書籍": [
        {"service": "Amazon", "url": "https://www.amazon.co.jp", "description": "AmazonでAI画像生成関連書籍を探す"},
        {"service": "楽天ブックス", "url": "https://www.rakuten.co.jp", "description": "楽天でAI画像生成関連書籍を探す"},
    ],
}
AFFILIATE_TAG = "musclelove07-22"

ADSENSE_CLIENT_ID = os.environ.get("ADSENSE_CLIENT_ID", "")
ADSENSE_ENABLED = bool(ADSENSE_CLIENT_ID)
DASHBOARD_PORT = 8101

# Google Analytics (GA4)
GOOGLE_ANALYTICS_ID = "G-CSFVD34MKK"

# Google Search Console 認証ファイル
SITE_VERIFICATION_FILES = {
    "googlea31edabcec879415.html": "google-site-verification: googlea31edabcec879415.html",
}
