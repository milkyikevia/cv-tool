#!/usr/bin/env python3

from pathlib import Path
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, cast
import argparse

from loguru import logger

from app import __version__
from config.loader import load_config
from config.constants import TYPE_ALIASES
from utils.log import setup_logging

# ----------------------------
# Argument / Type Helpers
# ----------------------------
def normalize_type(value: str) -> str:
    """コマンドライン引数のタイプを正規化（alias対応）"""
    key = value.lower()
    if key not in TYPE_ALIASES:
        raise argparse.ArgumentTypeError(
            f"Invalid type: {value}. Use 'image(i)' or 'video(v)'"
        )
    return TYPE_ALIASES[key]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="画像・動画前処理ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-t", "--type",   type=normalize_type, default="image",               help="データタイプ: 'image(i)' または 'video(v)' (デフォルト: image)")
    parser.add_argument("-p", "--path",   type=Path,           default=Path("./assets"),      help="入力パス (デフォルト: ./assets)")
    parser.add_argument("-c", "--config", type=Path,           default=Path("./config.yaml"), help="設定ファイルパス (デフォルト: ./config.yaml)")
    parser.add_argument("-o", "--output", type=Path,           default=Path("./result"),      help="出力ディレクトリ (デフォルト: ./result)")
    parser.add_argument("--interactive",  action="store_true",                                help="インタラクティブモードを有効化")
    return parser


# ----------------------------
# Run Args Protocol + Session State
# ----------------------------
@runtime_checkable
class RunArgs(Protocol):
    type:   str
    path:   Path
    config: Path
    output: Path


@dataclass
class SessionState:
    type:   str  = "image"
    path:   Path = Path("./assets")
    config: Path = Path("./config.yaml")
    output: Path = Path("./result")


# ----------------------------
# Core
# ----------------------------
def run(args: RunArgs) -> None:
    """
    前処理の実行
    # TODO: processor 実装後、進捗表示（tqdm等）を追加する
    """
    if not args.path.exists():
        raise FileNotFoundError(f"Input path not found: {args.path}")
    
    if not args.config.exists():
        raise FileNotFoundError(f"Config file not found: {args.config}")

    args.output.mkdir(parents=True, exist_ok=True)

    config = load_config(str(args.config))

    logger.info(f"Running {args.type} preprocessing")
    logger.debug(f"Config: {config}")
    logger.info(f"Input: {args.path}  Output: {args.output}")

    try:
        # TODO: process実装
        # process_files(args.path, args.type, config, args.output)
        logger.info("Preprocessing completed successfully")
    except Exception:
        logger.exception("Error during preprocessing")
        raise


# ----------------------------
# Interactive Mode
# ----------------------------
def handle_help() -> None:
    print("コマンド:")
    print("  set type <image|video|i|v>")
    print("  set path <path>")
    print("  set config <path>")
    print("  set output <path>")
    print("  show / run / exit")


def handle_set(parts: list[str], state: SessionState) -> None:
    if len(parts) < 3:
        print("使用法: set <option> <value>")
        return

    option = parts[1].lower()
    value  = " ".join(parts[2:])

    if option == "type":
        try:
            state.type = normalize_type(value)
            print(f"type → {state.type}")
        except argparse.ArgumentTypeError as e:
            print(e)

    elif option in ("path", "config"):
        p = Path(value)
        if not p.exists():
            print(f"存在しません: {p}")
            return
        setattr(state, option, p)
        print(f"{option} → {p}")

    elif option == "output":
        state.output = Path(value)
        print(f"output → {state.output}")

    else:
        print(f"不明なオプション: {option}")


def handle_show(state: SessionState) -> None:
    print(f"  type   : {state.type}")
    print(f"  path   : {state.path}")
    print(f"  config : {state.config}")
    print(f"  output : {state.output}")


def interactive_main() -> None:
    # TODO: readline でコマンド履歴・補完を実装する
    logger.info("インタラクティブモード開始 ('help' でコマンド一覧)")
    state = SessionState()

    while True:
        try:
            command = input(f"cv-tool({state.type})> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd   = parts[0].lower()

            if   cmd == "exit": logger.info("終了します"); break
            elif cmd == "help": handle_help()
            elif cmd == "set":  handle_set(parts, state)
            elif cmd == "show": handle_show(state)
            elif cmd == "run":
                try:
                    run(state)
                except Exception as e:
                    logger.error(f"実行に失敗しました: {e}")
            else:
                print(f"不明なコマンド: {cmd}")

        except KeyboardInterrupt:
            logger.info("中断されました")
            break
        except Exception as e:
            logger.error(f"エラー: {e}")


# ----------------------------
# Entrypoint
# ----------------------------
def cli_main() -> None:
    setup_logging(log_dir="logs", console_level="INFO", file_level="DEBUG",
                  rotation="10 MB", retention="7 days")

    logger.info(f"cv-tool v{__version__}")

    parser = create_parser()
    args   = parser.parse_args()

    if args.interactive:
        interactive_main()
    else:
        try:
            run(cast(RunArgs, args))
        except FileNotFoundError as e:
            logger.error(e)
            raise SystemExit(2)
        except Exception:
            logger.exception("Unexpected error")
            raise SystemExit(1)
        else:
            logger.info("Processing completed successfully.")


if __name__ == "__main__":
    cli_main()