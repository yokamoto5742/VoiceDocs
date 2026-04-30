import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def minify_json_file(input_path: str) -> bool:
    try:
        with open(input_path, encoding='utf-8') as file:
            data = json.load(file)

        minified_json = json.dumps(data, separators=(',', ':'), ensure_ascii=False)

        p = Path(input_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = p.parent / f"{p.stem}_{timestamp}{p.suffix}"

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(minified_json)

        print(f"成功: {output_path} に保存しました")

    except FileNotFoundError:
        print(f"エラー: ファイル '{input_path}' が見つかりません", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"エラー: JSONファイルの解析に失敗しました - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"エラー: 処理中にエラーが発生しました - {e}", file=sys.stderr)
        return False

    return True


def get_file_path_interactive() -> str:
    while True:
        input_path = input("入力JSONファイルのパスを入力してください: ").strip()

        if not input_path:
            print("ファイルパスが入力されていません。もう一度入力してください。")
            continue

        if not input_path.lower().endswith('.json'):
            print("警告: ファイル拡張子が .json ではありません。続行しますか？ (y/n): ", end="")
            if input().strip().lower() not in ['y', 'yes', 'はい']:
                continue

        if not Path(input_path).exists():
            print(f"エラー: ファイル '{input_path}' が見つかりません。もう一度入力してください。")
            continue

        return input_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="JSONファイルを一行にまとめるスクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python json_minifier.py                 # 対話的にファイルパスを指定
  python json_minifier.py input.json     # コマンドライン引数で指定
        """
    )

    parser.add_argument(
        'input_file',
        nargs='?',
        help='入力JSONファイルのパス（省略可能）'
    )

    args = parser.parse_args()

    if args.input_file:
        input_path = args.input_file
        if not Path(input_path).exists():
            print(f"エラー: ファイル '{input_path}' が見つかりません", file=sys.stderr)
            sys.exit(1)
    else:
        print("=== JSONファイルMinifyツール ===")
        input_path = get_file_path_interactive()

    if not minify_json_file(input_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
