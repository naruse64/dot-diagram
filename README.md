# 点図形問題生成システム

## フォルダ構成

```
dot-grid-problem/
├── README.md
├── generators/
│   └── generate_problems.py     # Python問題生成プログラム
├── problems/
│   ├── sample_problems.json     # サンプル問題データ
│   └── problem_config_example.json  # 問題設定ファイル例
├── scripts/
│   ├── generate.sh              # 問題生成スクリプト
│   ├── compile_pdf.sh           # PDF生成スクリプト
│   └── workflow.sh              # ワンステップ実行スクリプト
└── templates/
    └── dot_grid_template.typ    # Typstテンプレート
```

## クイックスタート

```bash
# 実行権限を付与
chmod +x scripts/*.sh

# ランダムな問題を3つ生成してPDF作成
./scripts/workflow.sh

# カスタマイズ例
./scripts/workflow.sh -n 5 -t mixed -o my_worksheet.pdf
./scripts/workflow.sh -g 4 -t square -o 4x4_problems.pdf
./scripts/workflow.sh -c problems/problem_config_example.json -o custom.pdf
```

## 詳細な使用方法

### ワンステップ実行 (workflow.sh)

```bash
./scripts/workflow.sh [オプション]

オプション:
    -n, --count NUM         問題数 (デフォルト: 3)
    -g, --grid-size SIZE    グリッドサイズ (デフォルト: 3)
    -t, --template TYPE     図形テンプレート (後述)
    -c, --config FILE       設定ファイルから生成
    -o, --output FILE       出力PDFファイル名 (デフォルト: output.pdf)
```

### 問題生成のみ (generate.sh)

```bash
./scripts/generate.sh -o problems/my_problems.json -n 5 -t mixed
```

### PDFコンパイルのみ (compile_pdf.sh)

```bash
./scripts/compile_pdf.sh problems/my_problems.json output.pdf
```

### Python直接実行

```bash
python3 generators/generate_problems.py --output problems/test.json --count 5 --template mixed
python3 generators/generate_problems.py --config problems/problem_config_example.json
```

## 図形テンプレート

| テンプレート名 | 内容 |
|---|---|
| `random`   | ランダムな線分 |
| `square`   | 正方形 |
| `diamond`  | 菱形（3×3専用） |
| `cross`    | 十字 |
| `x`        | X字（対角線2本） |
| `triangle` | 三角形 |
| `mixed`    | 上記をローテーション |

## JSON形式

```json
{
  "problems": [
    {
      "grid_size": 3,
      "lines": [
        {"from": [0, 0], "to": [2, 2]}
      ],
      "style": {
        "line_color": "black",   // 色名 or "#RRGGBB"（省略可）
        "line_width": 1,         // mm単位（省略可）
        "dot_radius": 2          // mm単位（省略可）
      }
    }
  ]
}
```

## 座標系

- 左上を原点 `(0, 0)` とする
- x が右方向、y が下方向に増加
- 3×3グリッドの場合、座標は `0〜2` の範囲

## 必要な環境

- **Python 3.6+** — 問題生成に必要
- **Typst 0.11+** — PDF生成に必要
  - macOS: `brew install typst`
  - その他: https://github.com/typst/typst

## カスタマイズ

### レイアウト調整

`templates/dot_grid_template.typ` の冒頭で変更：

```typst
#let square-size = 9.2cm   // 3×3向け
// #let square-size = 7.0cm   // 4×4向け
```

### デフォルトスタイル変更

```typst
#let default-line-width = 1mm
#let default-dot-radius = 2mm
#let default-line-color = black
```
## 今後の改善予定
- 生成される問題の精度向上
