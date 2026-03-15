"""
构建向量索引脚本
运行: python scripts/build_indexes.py
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.retrieval.build_index import load_retrieval_data, IndexBuilder, create_embedder


def main():
    print("=" * 60)
    print("构建向量索引")
    print("=" * 60)

    # 加载数据
    retrieval_data = load_retrieval_data()

    if not retrieval_data:
        print("错误: 没有加载到检索数据")
        print("提示: 按顺序运行以下脚本:")
        print("  1. python scripts/parse_skills.py")
        print("  2. python scripts/generate_queries.py")
        print("  3. python scripts/process_data.py")
        return

    # 创建嵌入器
    print("\n创建嵌入器...")
    device = "cuda" if __import__("torch").cuda.is_available() else "cpu"
    embedder = create_embedder(device=device)

    # 创建索引构建器
    builder = IndexBuilder(embedder=embedder)

    # 构建所有索引
    indexes = builder.build_all_indexes(retrieval_data, save=True)

    # 打印统计
    print("\n索引统计:")
    for category, index in sorted(indexes.items()):
        print(f"  {category}: {index.ntotal} 条")

    print("\n" + "=" * 60)
    print("索引构建完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
