# 点図形問題生成システム

## フォルダ構成

```
dot-grid-problem/
├── README.md
├── generators/
│   └── generate_problems.py        # Python問題生成プログラム
├── output/                         # デフォルトのPDF出力先
├── problems/
│   ├── sample_problems.json        # サンプル問題データ
│   └── problem_config_example.json # 問題設定ファイル例
├── scripts/
│   ├── generate.sh                 # 問題生成スクリプト
│   ├── compile_pdf.sh              # PDF生成スクリプト
│   └── workflow.sh                 # ワンステップ実行スクリプト
└── templates/
    └── dot_grid_template.typ       # Typstテンプレート
```

## クイックスタート

```bash
# 実行権限を付与
chmod +x scripts/*.sh

# ランダムな図形で3問生成してPDF作成（推奨）
./scripts/workflow.sh

# カスタマイズ例
./scripts/workflow.sh -n 5 -t mixed -o output/my_worksheet.pdf
./scripts/workflow.sh -t house -o output/house.pdf
./scripts/workflow.sh -g 4 -t diamond -o output/4x4_problems.pdf
./scripts/workflow.sh -c problems/problem_config_example.json -o output/custom.pdf
```

## 詳細な使用方法

### ワンステップ実行 (workflow.sh)

```bash
./scripts/workflow.sh [オプション]

オプション:
    -n, --count NUM         問題数 (デフォルト: 3)
    -g, --grid-size SIZE    グリッドサイズ・3 or 4 (デフォルト: 3)
    -t, --template TYPE     図形テンプレート (後述)
    -c, --config FILE       設定ファイルから生成
    -o, --output FILE       出力PDFファイル名 (デフォルト: output/output.pdf)
```

### 問題生成のみ (generate.sh)

```bash
./scripts/generate.sh -o problems/my_problems.json -n 5 -t mixed
```

### PDFコンパイルのみ (compile_pdf.sh)

```bash
./scripts/compile_pdf.sh problems/my_problems.json output/output.pdf
```

### Python直接実行

```bash
python3 generators/generate_problems.py -n 3 -t random_shape
python3 generators/generate_problems.py -n 6 -t mixed
python3 generators/generate_problems.py --config problems/problem_config_example.json
python3 generators/generate_problems.py --list-shapes   # 図形一覧を表示
```

## 図形テンプレート

### 共通テンプレート

| テンプレート名 | 内容 |
|---|---|
| `random_shape` | ライブラリからランダムに1形状を選択（**推奨**） |
| `random_shape_decorated` | ランダム形状＋装飾線を追加（難易度高め） |
| `mixed` | ライブラリ全形状をシャッフルしてローテーション |

### 3×3 グリッド用図形一覧

| テンプレート名 | 説明 |
|---|---|
| `square` | 正方形 |
| `right_triangle` | 直角三角形（左上直角） |
| `right_triangle_flip` | 直角三角形（右下直角） |
| `triangle_up` | 二等辺三角形（上向き） |
| `triangle_right` | 三角形（右向き） |
| `triangle_left` | 三角形（左向き） |
| `diamond` | 菱形 |
| `kite` | 凧形 |
| `parallelogram` | 平行四辺形 |
| `trapezoid` | 台形 |
| `trapezoid_simple` | 台形（シンプル） |
| `trapezoid_wide` | 台形（幅広） |
| `pentagon` | 五角形 |
| `hexagon_flat` | 六角形 |
| `house` | 家 |
| `house_small` | 家（小） |
| `hourglass` | 砂時計 |
| `bowtie` | 蝶ネクタイ |
| `cross` | 十字 |
| `x_shape` | X字 |
| `star_cross` | 米字 |
| `arrow_right` | 右矢印 |
| `arrow_right_simple` | 右矢印（シンプル） |
| `flag` | 旗 |
| `l_shape` | L字（開いた） |
| `l_shape_closed` | L字（閉じた） |
| `z_shape` | Z字 |
| `s_shape` | S字 |
| `step` | 階段 |
| `bent_line` | 折れ線 |
| `chevron_up` | 山形（上） |
| `chevron_down` | 山形（下） |
| `v_shape` | V字 |
| `caret` | キャレット |
| `zigzag` | ジグザグ |
| `irregular_quad` | 不規則四角形 |

### 4×4 グリッド用図形一覧

| テンプレート名 | 説明 |
|---|---|
| `square` | 正方形 |
| `right_triangle` | 直角三角形 |
| `triangle_up` | 三角形 |
| `diamond` | 菱形 |
| `kite` | 凧形 |
| `parallelogram` | 平行四辺形 |
| `trapezoid` | 台形 |
| `pentagon` | 五角形 |
| `hexagon` | 六角形 |
| `house` | 家 |
| `hourglass` | 砂時計 |
| `cross` | 十字 |
| `x_shape` | X字 |
| `arrow` | 矢印 |
| `l_shape` | L字 |
| `z_shape` | Z字 |
| `chevron` | 山形 |
| `bent` | 折れ線 |
| `irregular_quad` | 不規則四角形 |

> 利用可能な形状は `python3 generators/generate_problems.py --list-shapes` でいつでも確認できます。

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

`style` セクションおよび各フィールドは省略可能で、省略時はテンプレートのデフォルト値が使用されます。

## 座標系

- 左上を原点 `(0, 0)` とする
- x が右方向、y が下方向に増加
- 3×3グリッドの場合、座標は `0〜2` の範囲
- 4×4グリッドの場合、座標は `0〜3` の範囲

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