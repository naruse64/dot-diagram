#!/usr/bin/env python3
"""
点図形問題生成プログラム

【点図形問題の図形設計方針】
実際の点描写・点図形教材の分析に基づく設計原則:

1. 閉じた輪郭を持つ
   - 線分が繋がって閉じたポリゴンを形成している（三角形・四角形など）
   - バラバラな線の寄せ集めにならない

2. 意味のある形として認識できる
   - 三角形・四角形・家・矢印・星・L字など、名前を付けられる形
   - 子どもが「この形はなに？」と問いかけられる図形

3. 対称性を持つ（線対称・点対称）
   - 線対称：天才ドリルなど主要教材が重視する特徴
   - 整った形に見える・美しさがある

4. 斜め線を含む
   - 水平・垂直線だけでなく斜め線を組み合わせることで難易度と図形らしさが増す
   - 45度対角線が典型的

5. グリッド全体を適度に使う
   - 点が偏らず、グリッド内で広がりのある形
   - 小さく固まった形は避ける

使用方法:
    python generate_problems.py --output problems.json --count 3 --grid-size 3
    python generate_problems.py --template house
    python generate_problems.py --template random_shape
    python generate_problems.py --template mixed
    python generate_problems.py --config config.json
"""

import json
import random
import argparse
from typing import List, Dict, Tuple


# ============================================================
# 型エイリアス
# ============================================================
Point = Tuple[int, int]
Segment = Dict[str, List[int]]


def seg(x1: int, y1: int, x2: int, y2: int) -> Segment:
    """線分を辞書形式で生成するヘルパー"""
    return {"from": [x1, y1], "to": [x2, y2]}


def polygon(points: List[Point]) -> List[Segment]:
    """点列を閉じたポリゴンの線分リストに変換"""
    return [seg(points[i][0], points[i][1],
                points[(i + 1) % len(points)][0], points[(i + 1) % len(points)][1])
            for i in range(len(points))]


def polyline(points: List[Point]) -> List[Segment]:
    """点列を開いたポリラインの線分リストに変換"""
    return [seg(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
            for i in range(len(points) - 1)]


# ============================================================
# 3×3 グリッド用図形ライブラリ
# ============================================================
SHAPES_3x3 = {
    # ---- 基本多角形 ----
    "square": lambda: polygon([(0,0),(2,0),(2,2),(0,2)]),
    "triangle_up": lambda: polygon([(1,0),(2,2),(0,2)]),
    "triangle_right": lambda: polygon([(0,0),(2,1),(0,2)]),
    "triangle_left": lambda: polygon([(2,0),(2,2),(0,1)]),
    "diamond": lambda: polygon([(1,0),(2,1),(1,2),(0,1)]),
    "parallelogram": lambda: polygon([(1,0),(2,0),(1,2),(0,2)]),
    "right_triangle": lambda: polygon([(0,0),(2,0),(0,2)]),
    "right_triangle_flip": lambda: polygon([(2,0),(2,2),(0,2)]),

    # ---- 家・矢印・記号系 ----
    "house": lambda: polygon([(0,1),(1,0),(2,1),(2,2),(0,2)]),
    "house_small": lambda: polygon([(0,2),(0,1),(1,0),(2,1),(2,2)]),
    "arrow_right": lambda: polygon([(0,1),(1,0),(1,1),(2,1),(1,2),(1,1),(0,1)]),  # 矢印（単純化）
    "arrow_right_simple": lambda: polyline([(0,1),(2,1)]) + polyline([(1,0),(2,1),(1,2)]),
    "flag": lambda: polygon([(0,0),(2,0),(2,1),(0,2)]),

    # ---- 線対称な複合形 ----
    "hourglass": lambda: polygon([(0,0),(2,0),(0,2),(2,2)]),  # 砂時計（交差四角形）
    "bowtie": lambda: polygon([(0,0),(2,0),(0,2),(2,2)]),
    "chevron_up": lambda: polyline([(0,2),(1,0),(2,2)]),
    "chevron_down": lambda: polyline([(0,0),(1,2),(2,0)]),
    "v_shape": lambda: polyline([(0,0),(1,2),(2,0)]),
    "caret": lambda: polyline([(0,2),(1,0),(2,2)]),

    # ---- L字・Z字・段差系 ----
    "l_shape": lambda: polyline([(0,0),(0,2),(2,2)]),
    "l_shape_closed": lambda: polygon([(0,0),(1,0),(1,1),(2,1),(2,2),(0,2)]),
    "z_shape": lambda: polyline([(0,0),(2,0),(0,2),(2,2)]),
    "s_shape": lambda: polyline([(2,0),(0,0),(0,1),(2,1),(2,2),(0,2)]),
    "step": lambda: polyline([(0,2),(0,1),(1,1),(1,0),(2,0)]),

    # ---- プラス・クロス系 ----
    "cross": lambda: [seg(1,0,1,2), seg(0,1,2,1)],
    "x_shape": lambda: [seg(0,0,2,2), seg(2,0,0,2)],
    "star_cross": lambda: [seg(1,0,1,2), seg(0,1,2,1), seg(0,0,2,2), seg(2,0,0,2)],

    # ---- 台形・五角形 ----
    "trapezoid": lambda: polygon([(0,2),(2,2),(2,1),(1,0),(0,1)]),
    "trapezoid_simple": lambda: polygon([(0,2),(2,2),(1,0)]) + [seg(0,2,1,0)],  # 三角をベースに
    "trapezoid_wide": lambda: polygon([(0,1),(1,0),(2,0),(2,1),(1,2),(0,2)]),   # 六角形っぽく
    "pentagon": lambda: polygon([(1,0),(2,1),(2,2),(0,2),(0,1)]),
    "hexagon_flat": lambda: polygon([(0,1),(1,0),(2,0),(2,2),(1,2),(0,2)]),

    # ---- 非対称・複雑系（難易度高め） ----
    "irregular_quad": lambda: polygon([(0,0),(2,0),(2,1),(0,2)]),
    "kite": lambda: polygon([(1,0),(2,1),(1,2),(0,1)]),  # 凧形（=diamond）
    "bent_line": lambda: polyline([(0,0),(1,0),(1,1),(2,1),(2,2)]),
    "zigzag": lambda: polyline([(0,0),(1,1),(0,2)]) + polyline([(1,1),(2,1)]),
}

# ============================================================
# 4×4 グリッド用図形ライブラリ
# ============================================================
SHAPES_4x4 = {
    "square": lambda: polygon([(0,0),(3,0),(3,3),(0,3)]),
    "diamond": lambda: polygon([(1,0),(3,1),(2,3),(0,2)]),
    "triangle_up": lambda: polygon([(1,0),(3,3),(0,3)]),
    "right_triangle": lambda: polygon([(0,0),(3,0),(0,3)]),
    "house": lambda: polygon([(0,2),(1,0),(3,2),(3,3),(0,3)]),
    "trapezoid": lambda: polygon([(1,0),(2,0),(3,2),(0,2)]),
    "cross": lambda: [seg(1,0,1,3), seg(0,1,3,1), seg(2,0,2,3), seg(0,2,3,2)],
    "x_shape": lambda: [seg(0,0,3,3), seg(3,0,0,3)],
    "parallelogram": lambda: polygon([(1,0),(3,0),(2,3),(0,3)]),
    "arrow": lambda: polyline([(0,1),(3,1)]) + polyline([(1,0),(3,1),(1,2)]),
    "l_shape": lambda: polygon([(0,0),(1,0),(1,2),(3,2),(3,3),(0,3)]),
    "z_shape": lambda: polyline([(0,0),(3,0),(0,3),(3,3)]),
    "pentagon": lambda: polygon([(1,0),(3,1),(3,3),(0,3),(0,1)]),
    "hexagon": lambda: polygon([(1,0),(2,0),(3,1),(3,2),(2,3),(1,3),(0,2),(0,1)]),
    "hourglass": lambda: polygon([(0,0),(3,0),(0,3),(3,3)]),
    "chevron": lambda: polyline([(0,3),(1,0),(2,0),(3,3)]),
    "irregular_quad": lambda: polygon([(0,0),(3,1),(2,3),(0,2)]),
    "kite": lambda: polygon([(1,0),(3,1),(1,3),(0,1)]),
    "bent": lambda: polyline([(0,0),(2,0),(2,1),(3,1),(3,3)]),
}


class DotGridProblemGenerator:
    """点図形問題を生成するクラス"""

    def __init__(self, grid_size: int = 3):
        self.grid_size = grid_size
        self.shapes = SHAPES_3x3 if grid_size == 3 else SHAPES_4x4

    # ----------------------------------------------------------
    # 既存テンプレート（後方互換）
    # ----------------------------------------------------------
    def generate_shape_square(self) -> List[Segment]:
        return self.shapes["square"]()

    def generate_shape_diamond(self) -> List[Segment]:
        return self.shapes["diamond"]()

    def generate_shape_cross(self) -> List[Segment]:
        return self.shapes["cross"]()

    def generate_shape_x(self) -> List[Segment]:
        return self.shapes["x_shape"]()

    def generate_shape_triangle(self) -> List[Segment]:
        return self.shapes["triangle_up"]()

    # ----------------------------------------------------------
    # 新規: 意味のある形のランダム生成
    # ----------------------------------------------------------
    def generate_random_shape(self) -> List[Segment]:
        """
        形のライブラリからランダムに1つ選んで返す。
        閉じた図形・意味のある形を優先。
        """
        name = random.choice(list(self.shapes.keys()))
        return self.shapes[name]()

    def generate_random_shape_with_variation(self) -> List[Segment]:
        """
        ランダムな形に、ランダムな装飾線（内部線）を1〜2本加えることがある。
        より複雑な問題を生成したい場合に使用。
        """
        base = self.generate_random_shape()
        # 30%の確率で内部対角線を1本追加
        if random.random() < 0.3:
            m = self.grid_size - 1
            diagonals = [
                seg(0, 0, m, m),
                seg(m, 0, 0, m),
                seg(0, 0, m // 2, m),
                seg(m, 0, m // 2, m),
            ]
            extra = random.choice(diagonals)
            # 既に同じ線がなければ追加
            existing = {(tuple(s["from"]), tuple(s["to"])) for s in base}
            existing |= {(tuple(s["to"]), tuple(s["from"])) for s in base}
            key = (tuple(extra["from"]), tuple(extra["to"]))
            if key not in existing:
                base = base + [extra]
        return base

    # ----------------------------------------------------------
    # ランダム線分（旧来の実装・廃止予定だが互換のため残す）
    # ----------------------------------------------------------
    def generate_random_lines(self, min_lines: int = 3, max_lines: int = 8) -> List[Segment]:
        """
        ランダムな線分を生成（旧来の実装）。
        generate_random_shape() の使用を推奨。
        """
        num_lines = random.randint(min_lines, max_lines)
        lines = []
        used_segments = set()
        max_attempts = num_lines * 10

        attempts = 0
        while len(lines) < num_lines and attempts < max_attempts:
            attempts += 1
            x1 = random.randint(0, self.grid_size - 1)
            y1 = random.randint(0, self.grid_size - 1)
            x2 = random.randint(0, self.grid_size - 1)
            y2 = random.randint(0, self.grid_size - 1)

            if (x1, y1) == (x2, y2):
                continue
            segment = tuple(sorted([(x1, y1), (x2, y2)]))
            if segment in used_segments:
                continue

            used_segments.add(segment)
            lines.append(seg(x1, y1, x2, y2))

        return lines

    # ----------------------------------------------------------
    # 問題生成
    # ----------------------------------------------------------
    def generate_problem(self, shape_type: str = "random_shape", style: Dict = None) -> Dict:
        """1つの問題を生成"""
        shape_map = {
            # 新規（推奨）
            "random_shape":           self.generate_random_shape,
            "random_shape_decorated": self.generate_random_shape_with_variation,
            # 個別指定
            **{name: fn for name, fn in self.shapes.items()},
            # 後方互換
            "random":   self.generate_random_lines,
            "square":   self.generate_shape_square,
            "diamond":  self.generate_shape_diamond,
            "cross":    self.generate_shape_cross,
            "x":        self.generate_shape_x,
            "triangle": self.generate_shape_triangle,
        }

        generate_fn = shape_map.get(shape_type, self.generate_random_shape)
        lines = generate_fn()

        problem: Dict = {"grid_size": self.grid_size, "lines": lines}
        if style:
            problem["style"] = style

        return problem


# ============================================================
# 設定ファイルからの生成
# ============================================================
def generate_problems_from_config(config_path: str) -> Dict:
    """設定ファイルから問題を生成"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    problems = []
    for prob_config in config.get("problems", []):
        grid_size = prob_config.get("grid_size", 3)
        shape_type = prob_config.get("shape", "random_shape")
        style = prob_config.get("style", {})

        generator = DotGridProblemGenerator(grid_size)
        problem = generator.generate_problem(shape_type, style)
        problems.append(problem)

    return {"problems": problems}


# ============================================================
# CLI
# ============================================================
def main():
    # 利用可能なテンプレート一覧を動的に構築
    all_shapes = (
        list(SHAPES_3x3.keys()) +
        ["random_shape", "random_shape_decorated", "random", "mixed",
         "square", "diamond", "cross", "x", "triangle"]
    )

    parser = argparse.ArgumentParser(
        description="点図形問題生成プログラム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
テンプレート例:
  random_shape           : ライブラリからランダムに1形状を選択（推奨）
  random_shape_decorated : ランダム形状＋装飾線
  mixed                  : 全テンプレートをローテーション
  house                  : 家の形
  triangle_up            : 上向き三角形
  diamond                : 菱形
  hourglass              : 砂時計
  l_shape_closed         : 閉じたL字
  pentagon               : 五角形
  (その他多数)
        """
    )
    parser.add_argument("--output", "-o", default="problems.json", help="出力JSONファイル名")
    parser.add_argument("--count", "-n", type=int, default=3, help="生成する問題数")
    parser.add_argument("--grid-size", "-g", type=int, default=3, choices=[3, 4], help="グリッドサイズ")
    parser.add_argument("--template", "-t", default="random_shape", help="図形テンプレート名")
    parser.add_argument("--config", "-c", help="設定ファイルから生成")
    parser.add_argument("--line-color", default="black", help="線の色")
    parser.add_argument("--line-width", type=float, default=1, help="線の幅(mm)")
    parser.add_argument("--dot-radius", type=float, default=2, help="ドットの半径(mm)")
    parser.add_argument("--list-shapes", action="store_true", help="利用可能な図形名を一覧表示して終了")

    args = parser.parse_args()

    if args.list_shapes:
        print("=== 3×3 グリッド用図形 ===")
        for name in sorted(SHAPES_3x3.keys()):
            print(f"  {name}")
        print("\n=== 4×4 グリッド用図形 ===")
        for name in sorted(SHAPES_4x4.keys()):
            print(f"  {name}")
        print("\n=== 共通テンプレート ===")
        for name in ["random_shape", "random_shape_decorated", "mixed"]:
            print(f"  {name}")
        return

    if args.config:
        if args.template != "random_shape":
            print("警告: --config 指定時は --template は無視されます")
        result = generate_problems_from_config(args.config)
    else:
        generator = DotGridProblemGenerator(args.grid_size)
        style = {
            "line_color": args.line_color,
            "line_width": args.line_width,
            "dot_radius": args.dot_radius,
        }

        # mixed: 3x3ライブラリの全形状をローテーション
        if args.template == "mixed":
            shape_names = list(SHAPES_3x3.keys() if args.grid_size == 3 else SHAPES_4x4.keys())
            random.shuffle(shape_names)
            problems = [
                generator.generate_problem(shape_names[i % len(shape_names)], style)
                for i in range(args.count)
            ]
        else:
            problems = [
                generator.generate_problem(args.template, style)
                for _ in range(args.count)
            ]

        result = {"problems": problems}

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✓ {len(result['problems'])}個の問題を生成しました: {args.output}")


if __name__ == "__main__":
    main()
