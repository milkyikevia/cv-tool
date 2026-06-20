#!/usr/bin/env python3

import sys
from pathlib import Path

from loguru import logger


def setup_logging(
    log_dir: str | Path = "logs",
    console_level: str = "INFO",
    file_level: str = "DEBUG",
    rotation: str = "1 week",
    retention: str = "1 month",
) -> None:
    """
    ログシステムの初期化設定

    Args:
        log_dir:       ログファイルが保存されるディレクトリパス
        console_level: コンソール出力のログレベル
        file_level:    ファイル出力のログレベル
        rotation:      ログファイルのローテーション間隔
        retention:     ログファイルの保持期間
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.remove()

    # コンソールハンドラー
    logger.add(
        sys.stderr,
        level=console_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}:{function}:{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # ファイルハンドラー
    logger.add(
        str(log_dir / "debug_{time}.log"),
        level=file_level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level} | "
            "{name}:{function}:{line} - "
            "{message}"
        ),
        rotation=rotation,
        retention=retention,
    )
