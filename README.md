# 点図形問題生成システム

## ファイル構成

1. **dot_grid_template.typ** - Typstテンプレートファイル
2. **sample_problems.json** - サンプル問題データ

## 使用方法

### Typstのインストール

```bash
# macOS (Homebrew)
brew install typst

# Windows / Linux
# https://github.com/typst/typst/releases から最新版をダウンロード
```

### PDF生成

```bash
typst compile dot_grid_template.typ output.pdf
```

## JSON形式の説明

```json
{
  "problems": [
    {
      "grid_size": 3,           // グリッドサイズ（3×3）
      "lines": [                // 線分のリスト
        // 始点 [x, y], 終点 [x, y] の配列
        {"from": [0, 0], "to": [2, 0]},
        {"from": [0, 0], "to": [1, 2]},
        {"from": [2, 0], "to": [1, 2]}
      ],
      "style": {                 // style指定（省略可）
        "line_color": "black",   // 線の色（省略可、デフォルト"black"）
        "line_width": 1,         // 線の太さ（mm単位、省略可、デフォルト1mm）
        "dot_radius": 2          // ドットの半径（mm単位、省略可、デフォルト2mm）
      }
    }
  ]
}
```

## 座標系

- 左上を原点(0, 0)とする
- 横方向(x)が右に増加
- 縦方向(y)が下に増加
- 3×3グリッドの場合、座標は0〜2の範囲

## レイアウト設計

### 正方形のサイズ計算

`dot_grid_template.typ` の冒頭で正方形1辺の長さを指定：

```typst
#let square-size = 9.2cm  // この値を変更するだけ
```

正方形内のドット配置は自動計算されます：
- 辺とドットの間隔：ドット間隔 = 1:2（固定比率）
- `border-pad = square-size / 6`
- `cell-size = square-size / 3`

### デフォルトスタイル

テンプレートファイルで設定：

```typst
#let default-line-width = 1mm    // 線の幅
#let default-dot-radius = 2mm    // ドットの半径
#let default-line-color = black  // 線の色
```

## カスタマイズ

### 線の色を変更する例

色名（black, white, red, blue, green）または16進数カラーコード（#RRGGBB）が使用できます：

```json
"style": {
  "line_color": "#0000ff",  // 青色（hex形式）
  "line_width": 1.5,        // 1.5mm
  "dot_radius": 2           // 2mm
}
```

または

```json
"style": {
  "line_color": "red",      // 赤色（色名）
  "line_width": 1,
  "dot_radius": 2
}
```

### ドットサイズを変更する例

```json
"style": {
  "line_color": "black",
  "line_width": 1,
  "dot_radius": 3           // 大きめのドット（3mm）
}
```

### スタイルの省略

`style` の各項目は省略可能です。省略した場合はデフォルト値が使用されます：

```json
"style": {
  "line_color": "black"
  // line_width と dot_radius はデフォルト値を使用
}
```

または、`style`セクション全体を省略することも可能です：

```json
{
  "grid_size": 3,
  "lines": [
    {"from": [0, 0], "to": [2, 2]}
  ]
  // style省略 → すべてデフォルト値を使用
}
```

### 4×4グリッドへの拡張

JSONの`grid_size`を4に変更するだけで対応可能です：

```json
{
  "grid_size": 4,
  "lines": [
    {"from": [0, 0], "to": [3, 3]}
  ],
  "style": {
    "line_color": "black",
    "line_width": 1,
    "dot_radius": 2
  }
}
```

## トラブルシューティング

- エラーが出る場合：JSONの構文が正しいか確認してください
- レイアウトの調整：`dot_grid_template.typ`の`square-size`を変更してください
- 正方形がページに収まらない：`square-size`を小さくするか、ページマージンを調整してください

## 今後の改善予定
- 正方形の重なり防止
- 問題自動生成
- bashスクリプト作成
