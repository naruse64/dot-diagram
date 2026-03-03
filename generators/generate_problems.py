#!/usr/bin/env python3
"""
点図形問題生成プログラム

使用方法:
    python generate_problems.py --output problems.json --count 3 --grid-size 3
    python generate_problems.py --output problems.json --template random
    python generate_problems.py --config config.json
"""

import json
import random
import argparse
from typing import List, Dict


class DotGridProblemGenerator:
    """点図形問題を生成するクラス"""

    def __init__(self, grid_size: int = 3):
        self.grid_size = grid_size

    def generate_random_lines(self, min_lines: int = 3, max_lines: int = 8) -> List[Dict]:
        """ランダムな線分を生成"""
        num_lines = random.randint(min_lines, max_lines)
        lines = []
        used_segments = set()
        max_attempts = num_lines * 10  # 無限ループ防止

        attempts = 0
        while len(lines) < num_lines and attempts < max_attempts:
            attempts += 1

            x1, y1 = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            x2, y2 = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)

            # 同じ点は無効
            if (x1, y1) == (x2, y2):
                continue

            # 重複線分は無効
            segment = tuple(sorted([(x1, y1), (x2, y2)]))
            if segment in used_segments:
                continue

            used_segments.add(segment)
            lines.append({"from": [x1, y1], "to": [x2, y2]})

        return lines

    def generate_shape_square(self) -> List[Dict]:
        """正方形を生成"""
        m = self.grid_size - 1
        return [
            {"from": [0, 0], "to": [m, 0]},
            {"from": [m, 0], "to": [m, m]},
            {"from": [m, m], "to": [0, m]},
            {"from": [0, m], "to": [0, 0]},
        ]

    def generate_shape_diamond(self) -> List[Dict]:
        """菱形を生成（3x3専用、他サイズは正方形にフォールバック）"""
        if self.grid_size != 3:
            return self.generate_shape_square()
        return [
            {"from": [1, 0], "to": [0, 1]},
            {"from": [0, 1], "to": [1, 2]},
            {"from": [1, 2], "to": [2, 1]},
            {"from": [2, 1], "to": [1, 0]},
        ]

    def generate_shape_cross(self) -> List[Dict]:
        """十字を生成"""
        mid = self.grid_size // 2
        m = self.grid_size - 1
        return [
            {"from": [mid, 0], "to": [mid, m]},
            {"from": [0, mid], "to": [m, mid]},
        ]

    def generate_shape_x(self) -> List[Dict]:
        """X字を生成（対角線2本）"""
        m = self.grid_size - 1
        return [
            {"from": [0, 0], "to": [m, m]},
            {"from": [m, 0], "to": [0, m]},
        ]

    def generate_shape_triangle(self) -> List[Dict]:
        """三角形を生成"""
        m = self.grid_size - 1
        mid = self.grid_size // 2
        return [
            {"from": [mid, 0], "to": [0, m]},
            {"from": [0, m], "to": [m, m]},
            {"from": [m, m], "to": [mid, 0]},
        ]

    def generate_problem(self, shape_type: str = "random", style: Dict = None) -> Dict:
        """1つの問題を生成"""
        shape_map = {
            "random":   self.generate_random_lines,
            "square":   self.generate_shape_square,
            "diamond":  self.generate_shape_diamond,
            "cross":    self.generate_shape_cross,
            "x":        self.generate_shape_x,
            "triangle": self.generate_shape_triangle,
        }
        generate_fn = shape_map.get(shape_type, self.generate_random_lines)
        lines = generate_fn()

        problem = {
            "grid_size": self.grid_size,
            "lines": lines,
        }
        if style:
            problem["style"] = style

        return problem


def generate_problems_from_config(config_path: str) -> Dict:
    """設定ファイルから問題を生成"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    problems = []
    for prob_config in config.get("problems", []):
        grid_size = prob_config.get("grid_size", 3)
        shape_type = prob_config.get("shape", "random")
        style = prob_config.get("style", {})

        generator = DotGridProblemGenerator(grid_size)
        problem = generator.generate_problem(shape_type, style)
        problems.append(problem)

    return {"problems": problems}


def main():
    parser = argparse.ArgumentParser(description="点図形問題生成プログラム")
    parser.add_argument("--output", "-o", default="problems.json", help="出力JSONファイル名")
    parser.add_argument("--count", "-n", type=int, default=3, help="生成する問題数")
    parser.add_argument("--grid-size", "-g", type=int, default=3, help="グリッドサイズ")
    parser.add_argument(
        "--template", "-t",
        choices=["random", "square", "diamond", "cross", "x", "triangle", "mixed"],
        default="random",
        help="図形テンプレート",
    )
    parser.add_argument("--config", "-c", help="設定ファイルから生成")
    parser.add_argument("--line-color", default="black", help="線の色")
    parser.add_argument("--line-width", type=float, default=1, help="線の幅(mm)")
    parser.add_argument("--dot-radius", type=float, default=2, help="ドットの半径(mm)")

    args = parser.parse_args()

    if args.config:
        # --config と --template を同時指定した場合は警告
        if args.template != "random":
            print("警告: --config 指定時は --template は無視されます")
        result = generate_problems_from_config(args.config)
    else:
        generator = DotGridProblemGenerator(args.grid_size)
        style = {
            "line_color": args.line_color,
            "line_width": args.line_width,
            "dot_radius": args.dot_radius,
        }

        templates = ["square", "diamond", "cross", "x", "triangle", "random"]
        problems = []
        for i in range(args.count):
            shape_type = templates[i % len(templates)] if args.template == "mixed" else args.template
            problems.append(generator.generate_problem(shape_type, style))

        result = {"problems": problems}

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✓ {len(result['problems'])}個の問題を生成しました: {args.output}")


if __name__ == "__main__":
    main()
