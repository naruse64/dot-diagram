#!/bin/bash
# ワンステップ実行スクリプト: 問題生成 → PDF作成
# 使用方法: ./workflow.sh [オプション]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATE="$SCRIPT_DIR/generate.sh"
COMPILE="$SCRIPT_DIR/compile_pdf.sh"

TEMP_JSON="/tmp/dot_grid_problems_$$.json"
OUTPUT_PDF="output/output.pdf"

# ヘルプ表示
show_help() {
    cat << EOF
ワンステップ実行スクリプト: 問題生成 → PDF作成

使用方法:
    ./workflow.sh [オプション]

オプション:
    -n, --count NUM         問題数 (デフォルト: 3)
    -g, --grid-size SIZE    グリッドサイズ (デフォルト: 3)
    -t, --template TYPE     図形テンプレート (random/square/diamond/cross/x/triangle/mixed)
    -c, --config FILE       設定ファイルから生成
    -o, --output FILE       出力PDFファイル名 (デフォルト: output/output.pdf)
    -h, --help              このヘルプを表示

例:
    ./workflow.sh -n 5 -t mixed -o output/worksheet.pdf
    ./workflow.sh -c problems/problem_config_example.json -o output/my_worksheet.pdf
    ./workflow.sh -g 4 -t square -o output/4x4_problems.pdf
EOF
}

# 一時ファイルのクリーンアップ（終了時に必ず実行）
cleanup() {
    rm -f "$TEMP_JSON"
}
trap cleanup EXIT

# 引数解析
GEN_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output) OUTPUT_PDF="$2"; shift 2 ;;
        -h|--help)   show_help; exit 0 ;;
        *)           GEN_ARGS+=("$1"); shift ;;
    esac
done

# スクリプト存在確認
if [ ! -f "$GENERATE" ] || [ ! -f "$COMPILE" ]; then
    echo "エラー: generate.sh または compile_pdf.sh が見つかりません"
    echo "  期待パス: $SCRIPT_DIR/"
    exit 1
fi

# 実行権限付与
chmod +x "$GENERATE" "$COMPILE" 2>/dev/null || true

echo "============================================"
echo "ステップ1: 問題を生成"
echo "============================================"
"$GENERATE" "${GEN_ARGS[@]}" -o "$TEMP_JSON"

echo ""
echo "============================================"
echo "ステップ2: PDFをコンパイル"
echo "============================================"
"$COMPILE" "$TEMP_JSON" "$OUTPUT_PDF"

echo ""
echo "============================================"
echo "完了!"
echo "出力: $OUTPUT_PDF"
echo "============================================"
