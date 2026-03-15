"""
FAISS 向量索引构建器
为每个分类建立独立的向量索引
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, List, Any

import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("警告: FAISS 未安装，将使用替代方案")


from ..retrieval.embedder import TextEmbedder, create_embedder
from ..router.category_config import CategoryConfig


class IndexBuilder:
    """索引构建器"""

    def __init__(
        self,
        embedder: TextEmbedder = None,
        index_type: str = "flat",
        output_dir: str = None
    ):
        """
        初始化索引构建器

        Args:
            embedder: 嵌入器
            index_type: 索引类型 (flat, ivf, pq)
            output_dir: 输出目录
        """
        if not FAISS_AVAILABLE:
            raise ImportError("需要安装 FAISS: pip install faiss-cpu")

        self.embedder = embedder or create_embedder()
        self.index_type = index_type

        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "data" / "indexes"
        else:
            output_dir = Path(output_dir)

        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_index(
        self,
        vectors: np.ndarray,
        index_type: str = None
    ) -> faiss.Index:
        """
        创建 FAISS 索引

        Args:
            vectors: 向量数组 [n, dim]
            index_type: 索引类型

        Returns:
            FAISS 索引
        """
        index_type = index_type or self.index_type
        dim = vectors.shape[1]

        if index_type == "flat":
            # 精确搜索，内积
            index = faiss.IndexFlatIP(dim)
        elif index_type == "ivf":
            # IVF 索引，需要训练
            nlist = min(100, vectors.shape[0] // 10)  # 聚类中心数
            quantizer = faiss.IndexFlatIP(dim)
            index = faiss.IndexIVFFlat(quantizer, dim, nlist)
            index.train(vectors)
        elif index_type == "pq":
            # 乘积量化
            nbits = 8  # 每个子向量的位数
            index = faiss.IndexFlatIP(dim)
        else:
            raise ValueError(f"未知的索引类型: {index_type}")

        # 添加向量
        index.add(vectors)

        return index

    def build_category_index(
        self,
        category: str,
        data: List[Dict],
        save: bool = True
    ) -> faiss.Index:
        """
        为单个分类构建索引

        Args:
            category: 分类名称
            data: 数据列表，每项包含 {text, skill_id, skill_name}
            save: 是否保存索引

        Returns:
            FAISS 索引
        """
        if not data:
            print(f"警告: 分类 {category} 没有数据")
            return None

        print(f"构建分类索引: {category} ({len(data)} 条)")

        # 提取文本
        texts = [item["text"] for item in data]

        # 编码
        print(f"  编码向量...")
        vectors = self.embedder.encode(texts, show_progress=False)

        # 确保归一化 (用于内积)
        faiss.normalize_L2(vectors)

        # 创建索引
        print(f"  创建索引...")
        index = self.create_index(vectors, self.index_type)

        # 保存映射
        mapping = {
            "category": category,
            "items": data,
            "size": len(data),
        }

        if save:
            # 保存索引
            index_path = self.output_dir / f"{category}.faiss"
            faiss.write_index(index, str(index_path))

            # 保存映射
            mapping_path = self.output_dir / f"{category}_mapping.pkl"
            with open(mapping_path, 'wb') as f:
                pickle.dump(mapping, f)

            print(f"  已保存: {index_path}")

        return index

    def build_all_indexes(
        self,
        retrieval_data: Dict[str, List[Dict]],
        save: bool = True
    ) -> Dict[str, faiss.Index]:
        """
        为所有分类构建索引

        Args:
            retrieval_data: 按分类组织的数据
            save: 是否保存索引

        Returns:
            索引字典 {category: index}
        """
        print("=" * 60)
        print("构建向量索引")
        print("=" * 60)
        print(f"分类数量: {len(retrieval_data)}")
        print(f"索引类型: {self.index_type}")

        indexes = {}

        for category, data in sorted(retrieval_data.items()):
            try:
                index = self.build_category_index(category, data, save)
                if index is not None:
                    indexes[category] = index
            except Exception as e:
                print(f"错误: 构建 {category} 索引失败: {e}")

        print("=" * 60)
        print(f"完成! 构建了 {len(indexes)} 个索引")

        return indexes

    def load_index(self, category: str) -> tuple:
        """
        加载单个分类的索引

        Args:
            category: 分类名称

        Returns:
            (index, mapping)
        """
        index_path = self.output_dir / f"{category}.faiss"
        mapping_path = self.output_dir / f"{category}_mapping.pkl"

        if not index_path.exists() or not mapping_path.exists():
            raise FileNotFoundError(f"索引文件不存在: {category}")

        # 加载索引
        index = faiss.read_index(str(index_path))

        # 加载映射
        with open(mapping_path, 'rb') as f:
            mapping = pickle.load(f)

        return index, mapping


def load_retrieval_data(data_path: str = None) -> Dict[str, List[Dict]]:
    """
    加载检索数据

    Args:
        data_path: 数据文件路径

    Returns:
        按分类组织的数据
    """
    if data_path is None:
        data_path = Path(__file__).parent.parent.parent / "data" / "processed" / "retrieval_data_by_category.json"
    else:
        data_path = Path(data_path)

    print(f"加载数据: {data_path}")

    if not data_path.exists():
        print(f"错误: 数据文件不存在: {data_path}")
        return {}

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 统计
    total = sum(len(items) for items in data.values())
    print(f"加载了 {len(data)} 个分类，共 {total} 条数据")

    return data


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="构建 FAISS 向量索引")
    parser.add_argument(
        "--data",
        type=str,
        default="data/processed/retrieval_data_by_category.json",
        help="检索数据文件路径"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/indexes",
        help="输出目录"
    )
    parser.add_argument(
        "--index-type",
        type=str,
        default="flat",
        choices=["flat", "ivf", "pq"],
        help="索引类型"
    )
    parser.add_argument(
        "--embedder",
        type=str,
        default="auto",
        choices=["auto", "bge-small", "bge-base", "dummy"],
        help="嵌入器类型"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if __import__("torch").cuda.is_available() else "cpu",
        help="设备"
    )

    args = parser.parse_args()

    # 加载数据
    retrieval_data = load_retrieval_data(args.data)

    if not retrieval_data:
        print("错误: 没有加载数据")
        return

    # 创建嵌入器
    print("\n创建嵌入器...")
    embedder = create_embedder(args.embedder, args.device)

    # 创建索引构建器
    builder = IndexBuilder(
        embedder=embedder,
        index_type=args.index_type,
        output_dir=args.output_dir
    )

    # 构建所有索引
    indexes = builder.build_all_indexes(retrieval_data, save=True)

    # 打印统计
    print("\n索引统计:")
    for category, index in sorted(indexes.items()):
        print(f"  {category}: {index.ntotal} 条")

    print(f"\n索引已保存到: {args.output_dir}")


if __name__ == "__main__":
    main()
