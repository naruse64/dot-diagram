#!/bin/bash
# 問題生成スクリプト
# 使用方法: ./generate.sh [オプション]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GENERATOR="$PROJECT_ROOT/generators/generate_problems.py"

# デフォルト値
OUTPUT="problems.json"
COUNT=3
GRID_SIZE=3
TEMPLATE="random"
LINE_COLOR="black"
LINE_WIDTH=1
DOT_RADIUS=2
CONFIG=""

# ヘルプ表示
show_help() {
    cat << EOF
点図形問題生成スクリプト

使用方法:
    ./generate.sh [オプション]

オプション:
    -o, --output FILE       出力ファイル名 (デフォルト: problems.json)
    -n, --count NUM         問題数 (デフォルト: 3)
    -g, --grid-size SIZE    グリッドサイズ (デフォルト: 3)
    -t, --template TYPE     図形テンプレート (random/square/diamond/cross/x/triangle/mixed)
    -c, --config FILE       設定ファイルから生成
    --line-color COLOR      線の色 (デフォルト: black)
    --line-width WIDTH      線の幅(mm) (デフォルト: 1)
    --dot-radius RADIUS     ドットの半径(mm) (デフォルト: 2)
    -h, --help              このヘルプを表示

例:
    ./generate.sh -o my_problems.json -n 5 -t mixed
    ./generate.sh -c problems/problem_config_example.json
    ./generate.sh -g 4 -t square --line-width 1.5
EOF
}

# 引数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)    OUTPUT="$2";     shift 2 ;;
        -n|--count)     COUNT="$2";      shift 2 ;;
        -g|--grid-size) GRID_SIZE="$2";  shift 2 ;;
        -t|--template)  TEMPLATE="$2";   shift 2 ;;
        -c|--config)    CONFIG="$2";     shift 2 ;;
        --line-color)   LINE_COLOR="$2"; shift 2 ;;
        --line-width)   LINE_WIDTH="$2"; shift 2 ;;
        --dot-radius)   DOT_RADIUS="$2"; shift 2 ;;
        -h|--help)      show_help; exit 0 ;;
        *)
            echo "エラー: 不明なオプション $1"
            show_help
            exit 1
            ;;
    esac
done

# Pythonスクリプトの確認
if [ ! -f "$GENERATOR" ]; then
    echo "エラー: generate_problems.py が見つかりません ($GENERATOR)"
    exit 1
fi

# Python実行
echo "問題を生成中..."
if [ -n "$CONFIG" ]; then
    python3 "$GENERATOR" --output "$OUTPUT" --config "$CONFIG"
else
    python3 "$GENERATOR" \
        --output "$OUTPUT" \
        --count "$COUNT" \
        --grid-size "$GRID_SIZE" \
        --template "$TEMPLATE" \
        --line-color "$LINE_COLOR" \
        --line-width "$LINE_WIDTH" \
        --dot-radius "$DOT_RADIUS"
fi

echo "完了: $OUTPUT"
