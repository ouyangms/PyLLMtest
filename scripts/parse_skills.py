"""
解析技能文件脚本
运行: python scripts/parse_skills.py
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.skill_parser import SkillParser
from src.router.category_config import classify_skills


def main():
    print("=" * 60)
    print("解析技能文件")
    print("=" * 60)

    # 创建解析器
    parser = SkillParser()

    # 解析所有技能
    skills = parser.parse_all_skills()

    if not skills:
        print("没有解析到任何技能")
        return

    # 合并元数据
    skills = parser.merge_with_metadata()

    # 自动分类
    skills = classify_skills(skills)

    # 保存结果
    output_path = parser.save_to_json()

    # 打印统计
    print("\n" + "=" * 60)
    print("统计信息")
    print("=" * 60)

    stats = parser.get_statistics()
    print(f"总技能数: {stats['total_skills']}")
    print(f"有示例的技能: {stats['with_examples']}")
    print(f"无示例的技能: {stats['without_examples']}")
    print(f"平均示例数: {stats['avg_examples']:.2f}")

    # 分类统计
    from collections import Counter
    category_counts = Counter(s.get("category", "unknown") for s in skills)

    print("\n分类分布:")
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count}")

    print("=" * 60)
    print(f"完成! 结果已保存到: {output_path}")


if __name__ == "__main__":
    main()
