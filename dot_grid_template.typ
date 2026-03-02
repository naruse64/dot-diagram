// ===== レイアウト設定 =====
#let square-size = 9.2cm       // 正方形1辺の長さ(3×3適性)
// #let square-size = 7.0cm       // 正方形1辺の長さ(4×4適性)
#let border-pad = square-size / 6   // 辺とドットの間隔（比率1）
#let cell-size = square-size / 3    // ドット間の間隔（比率2）

// ===== デフォルトスタイル =====
#let default-line-width = 1mm    // 線の幅デフォルト
#let default-dot-radius = 2mm    // ドットの半径デフォルト
#let default-line-color = black  // 線の色デフォルト

// ===== ページ設定 =====
#set page(
  paper: "a4",
  flipped: true,
  margin: (x: 1cm, top: 1.5cm, bottom: 0.5cm)
)

// ===== ドットを中心座標で描画 =====
#let draw-dot-at(cx, cy, radius) = {
  place(
    dx: cx - radius,
    dy: cy - radius,
    circle(radius: radius, fill: black)
  )
}

// ===== 線分をドット中心同士で描画 =====
#let draw-line-between(cx1, cy1, cx2, cy2, color: black, width: 1.5pt) = {
  place(
    dx: cx1,
    dy: cy1,
    line(
      start: (0pt, 0pt),
      end: (cx2 - cx1, cy2 - cy1),
      stroke: stroke(paint: color, thickness: width)
    )
  )
}

// ===== グリッド描画（枠線あり） =====
#let draw-grid(size, with-lines: false, lines-data: (), line-color: black, line-width: 1.5pt, dot-radius: default-dot-radius) = {
  let inner = (size - 1) * cell-size
  let total = inner + border-pad * 2

  block(
    width: total,
    height: total,
    stroke: 1pt + black,
    inset: 0pt,
    {
      // 線分を先に描画（ドットの下に来るよう）
      if with-lines {
        for line-item in lines-data {
          let fx = line-item.from.at(0)
          let fy = line-item.from.at(1)
          let tx = line-item.to.at(0)
          let ty = line-item.to.at(1)
          let cx1 = border-pad + fx * cell-size
          let cy1 = border-pad + fy * cell-size
          let cx2 = border-pad + tx * cell-size
          let cy2 = border-pad + ty * cell-size
          draw-line-between(cx1, cy1, cx2, cy2, color: line-color, width: line-width)
        }
      }

      // ドットを描画
      for y in range(size) {
        for x in range(size) {
          let cx = border-pad + x * cell-size
          let cy = border-pad + y * cell-size
          draw-dot-at(cx, cy, dot-radius)
        }
      }
    }
  )
}

// ===== 1問分（お手本＋回答欄）を縦に並べる =====
#let problem-cell(problem) = {
  // styleセクションが存在するか確認
  let has-style = "style" in problem
  
  // 色の処理：文字列なら色名またはhexとして解釈、省略時はデフォルト
  let lc = if has-style and "line_color" in problem.style {
    let color-str = problem.style.line_color
    if color-str.starts-with("#") {
      rgb(color-str)
    } else if color-str == "black" {
      black
    } else if color-str == "white" {
      white
    } else if color-str == "red" {
      red
    } else if color-str == "blue" {
      blue
    } else if color-str == "green" {
      green
    } else {
      rgb(color-str)  // hex形式として試行
    }
  } else {
    default-line-color
  }
  
  let lw = if has-style and "line_width" in problem.style { problem.style.line_width * 1mm } else { default-line-width }
  let dr = if has-style and "dot_radius" in problem.style { problem.style.dot_radius * 1mm } else { default-dot-radius }
  let sz = problem.grid_size

  align(center,
    stack(
      dir: ttb,
      spacing: 0cm,
      draw-grid(sz, with-lines: true, lines-data: problem.lines, line-color: lc, line-width: lw, dot-radius: dr),
      draw-grid(sz, dot-radius: dr),
    )
  )
}

// ===== 3問を横に並べる =====
#let problem-row(problems) = {
  grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 0pt,
    align: center + horizon,
    ..problems.map(p => problem-cell(p))
  )
}

// ===== メイン =====
#let data = json("sample_problems.json")
#problem-row(data.problems)
