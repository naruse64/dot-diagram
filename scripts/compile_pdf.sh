#!/bin/bash
# PDF生成スクリプト
# 使用方法: ./compile_pdf.sh <問題JSONファイル> [出力PDFファイル]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATE="$PROJECT_ROOT/templates/dot_grid_template.typ"

# 引数チェック
if [ $# -eq 0 ]; then
    echo "使用方法: ./compile_pdf.sh <問題JSONファイル> [出力PDFファイル]"
    echo ""
    echo "例:"
    echo "  ./compile_pdf.sh problems/sample_problems.json"
    echo "  ./compile_pdf.sh problems/my_problems.json output.pdf"
    exit 1
fi

INPUT_JSON="$1"
OUTPUT_PDF="${2:-${INPUT_JSON%.json}.pdf}"

# ファイル存在チェック
if [ ! -f "$INPUT_JSON" ]; then
    echo "エラー: 入力ファイル '$INPUT_JSON' が見つかりません"
    exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
    echo "エラー: テンプレートファイル '$TEMPLATE' が見つかりません"
    exit 1
fi

# Typst実行可能か確認
if ! command -v typst &> /dev/null; then
    echo "エラー: typst コマンドが見つかりません"
    echo "Typstをインストールしてください: https://github.com/typst/typst"
    exit 1
fi

# JSONのバリデーション
echo "JSONファイルを検証中..."
if ! python3 -m json.tool "$INPUT_JSON" > /dev/null 2>&1; then
    echo "エラー: '$INPUT_JSON' は有効なJSONファイルではありません"
    exit 1
fi

# 絶対パスに変換
ABS_INPUT_JSON="$(cd "$(dirname "$INPUT_JSON")" && pwd)/$(basename "$INPUT_JSON")"
# OUTPUT_PDFの親ディレクトリが存在しない場合はカレントディレクトリに出力
ABS_OUTPUT_PDF="$(cd "$(dirname "$OUTPUT_PDF")" 2>/dev/null && pwd || pwd)/$(basename "$OUTPUT_PDF")"

# JSONをtemplates/直下に一時コピー
# （Typstはテンプレートファイルのディレクトリを起点にパスを解釈するため）
TEMPLATES_DIR="$(dirname "$TEMPLATE")"
TEMP_JSON="$TEMPLATES_DIR/.compile_tmp.json"
cp "$ABS_INPUT_JSON" "$TEMP_JSON"

# PDF生成
echo "PDFを生成中: $OUTPUT_PDF"
typst compile "$TEMPLATE" "$ABS_OUTPUT_PDF" --input json-file=".compile_tmp.json"

# 一時ファイル削除
rm -f "$TEMP_JSON"

# 結果確認
if [ -f "$ABS_OUTPUT_PDF" ]; then
    FILE_SIZE=$(du -h "$ABS_OUTPUT_PDF" | cut -f1)
    echo "✓ 生成完了: $OUTPUT_PDF (サイズ: $FILE_SIZE)"
else
    echo "エラー: PDFの生成に失敗しました"
    exit 1
fi
