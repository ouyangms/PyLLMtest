"""
生成训练样本脚本
运行: python scripts/generate_queries.py [--with-api]
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.query_generator import QueryGenerator


def main():
    import argparse

    parser = argparse.ArgumentParser(description="生成训练样本")
    parser.add_argument(
        "--input",
        type=str,
        default="data/processed/skills_database.json",
        help="输入技能文件"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/skills_with_queries.json",
        help="输出文件"
    )
    parser.add_argument(
        "--target-count",
        type=int,
        default=8,
        help="每个技能的目标样本数"
    )
    parser.add_argument(
        "--with-api",
        action="store_true",
        help="使用LLM API生成（需要配置OPENAI_API_KEY）"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("生成训练样本")
    print("=" * 60)

    # 加载数据
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        print("提示: 先运行 python scripts/parse_skills.py")
        return

    import json
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        skills = json.load(f)

    print(f"加载了 {len(skills)} 个技能")

    # 创建生成器
    generator = QueryGenerator()

    if args.with_api:
        print("使用LLM API生成样本")
    else:
        print("使用规则生成样本（推荐配置API以获得更好效果）")
        print("提示: 使用 --with-api 参数启用LLM生成")

    # 批量生成
    skills = generator.generate_batch(
        skills,
        target_count=args.target_count
    )

    # 保存结果
    output_path = generator.save_queries(skills, args.output)

    # 打印统计
    print("\n" + "=" * 60)
    print("生成统计")
    print("=" * 60)

    stats = generator.get_statistics(skills)
    print(f"总技能数: {stats['total_skills']}")
    print(f"总样本数: {stats['total_queries']}")
    print(f"平均样本数: {stats['avg_queries']:.2f}")
    print(f"达标技能数 (≥{args.target_count}条): {stats['skills_with_enough']}")

    print("=" * 60)
    print(f"完成! 结果已保存到: {output_path}")


if __name__ == "__main__":
    main()
