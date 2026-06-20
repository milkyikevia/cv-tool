#!/usr/bin/env python3

# タイプエイリアス（normalize_type で使用）
TYPE_ALIASES: dict[str, str] = {
    "image": "image",
    "i":     "image",
    "video": "video",
    "v":     "video",
}

# サポートされる拡張子（先頭にドットを含む）
IMAGE_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
VIDEO_EXTENSIONS: list[str] = [".mp4", ".mov", ".avi", ".mkv", ".wmv"]

# デフォルト値
DEFAULT_FPS:           float = 30.0
DEFAULT_CODEC:         str   = "mp4v"
DEFAULT_IMAGE_QUALITY: int   = 95
