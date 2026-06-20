#!/usr/bin/env python3

from pathlib import Path
from collections.abc import Callable
from typing import Any
import copy
import yaml
from loguru import logger
from .constants import DEFAULT_FPS, DEFAULT_CODEC, DEFAULT_IMAGE_QUALITY

type Config = dict[str, Any]


# ----------------------------
# Config Loader
# ----------------------------
def load_config(config_file_path: str) -> Config:
    """
    YAML形式の設定ファイルをロード
    Args:
        config_file_path: 設定ファイルのパス
    Returns:
        ロードされた設定データ
    """
    config_path = Path(config_file_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    try:
        with open(config_file_path, encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"YAML parse error: {e}")
        raise
    except Exception:
        logger.exception("Unexpected error while reading config")
        raise

    if not isinstance(config_data, dict):
        raise ValueError("Config file must contain a YAML dictionary")

    validated_config = _validate_and_apply_defaults(copy.deepcopy(config_data))

    logger.info("Configuration loaded: {}", config_file_path)
    logger.debug("Config content: {}", validated_config)

    return validated_config


# ----------------------------
# Default Application + Validation
# ----------------------------
def _validate_and_apply_defaults(config_data: Config | None) -> Config:
    if config_data is None:
        config_data = {}

    # 画像設定
    image_config = config_data.get("image_settings") or config_data.get("image") or {}
    image_config.setdefault("quality", DEFAULT_IMAGE_QUALITY)
    config_data["image_settings"] = image_config

    # 動画設定
    video_config = config_data.get("video_settings") or config_data.get("video") or {}
    video_config.setdefault("fps", DEFAULT_FPS)
    video_config.setdefault("codec", DEFAULT_CODEC)
    config_data["video_settings"] = video_config

    # バリデーション
    for prefix, cfg in [("video", video_config), ("image", image_config)]:
        for key, validator in _EFFECT_VALIDATORS.items():
            _validate_effect(cfg, key, prefix, validator)

    return config_data


# ----------------------------
# Common Enabled Checker
# ----------------------------
def _validate_effect(
    config: Config,
    key: str,
    prefix: str = "",
    validator: Callable[[Config, str], None] | None = None,
) -> None:
    effect = config.get(key, {})
    if not effect.get("enabled", True):
        return
    if validator:
        validator(effect, prefix)


# ----------------------------
# Individual Validators
# ----------------------------
def _validate_crop(effect: Config, prefix: str) -> None:
    coords = effect.get("coordinates")
    if coords is None:
        return
    if not isinstance(coords, list) or len(coords) != 4:
        raise ValueError(f"{prefix}: Crop coordinates must be [left, top, right, bottom]")
    left, top, right, bottom = coords
    if not all(isinstance(c, int) and c >= 0 for c in coords):
        raise ValueError(f"{prefix}: Crop coordinates must be non-negative integers")
    if left >= right or top >= bottom:
        raise ValueError(f"{prefix}: Crop coordinates must satisfy left < right and top < bottom")


def _validate_resize(effect: Config, prefix: str) -> None:
    size = effect.get("output_size")
    if size is None:
        return
    if not isinstance(size, list) or len(size) != 2:
        raise ValueError(f"{prefix}: Resize output_size must be [width, height]")
    width, height = size
    if not (isinstance(width, int) and isinstance(height, int) and width > 0 and height > 0):
        raise ValueError(f"{prefix}: Resize output_size must be positive integers")


def _validate_brightness(effect: Config, prefix: str) -> None:
    factor = effect.get("factor")
    if factor is None:
        return
    if not isinstance(factor, (int, float)) or factor <= 0:
        raise ValueError(f"{prefix}: Brightness factor must be positive")


def _validate_saturation(effect: Config, prefix: str) -> None:
    factor = effect.get("factor")
    if factor is None:
        return
    if not isinstance(factor, (int, float)) or factor <= 0:
        raise ValueError(f"{prefix}: Saturation factor must be positive")


def _validate_rotate(effect: Config, prefix: str) -> None:
    angle = effect.get("angle")
    if angle is None:
        return
    if not isinstance(angle, int) or not (0 <= angle <= 3):
        raise ValueError(f"{prefix}: Rotate angle must be 0~3 (90度単位)")


def _validate_flip(effect: Config, prefix: str) -> None:
    option = effect.get("options")
    if option is None:
        return
    if option not in ("vertically", "horizontally"):
        raise ValueError(f"{prefix}: Flip options must be 'vertically' or 'horizontally'")


# effect名 → validator のマッピング（_validate_and_apply_defaults で使用）
_EFFECT_VALIDATORS: dict[str, Callable[[Config, str], None]] = {
    "crop":       _validate_crop,
    "resize":     _validate_resize,
    "brightness": _validate_brightness,
    "saturation": _validate_saturation,
    "rotate":     _validate_rotate,
    "flip":       _validate_flip,
}
