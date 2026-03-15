"""
向量存储接口
管理 FAISS 索引，提供 Top-K 检索功能
"""

import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


from ..retrieval.embedder import TextEmbedder, create_embedder


class VectorStore:
    """向量存储"""

    def __init__(
        self,
        index_dir: str = None,
        embedder: TextEmbedder = None
    ):
        """
        初始化向量存储

        Args:
            index_dir: 索引目录
            embedder: 嵌入器
        """
        if not FAISS_AVAILABLE:
            raise ImportError("需要安装 FAISS: pip install faiss-cpu")

        if index_dir is None:
            index_dir = Path(__file__).parent.parent.parent / "data" / "indexes"
        else:
            index_dir = Path(index_dir)

        self.index_dir = index_dir
        self.embedder = embedder or create_embedder()

        # 索引缓存
        self.indexes: Dict[str, Any] = {}
        self.mappings: Dict[str, Dict] = {}

        # 加载所有索引
        self._load_all_indexes()

    def _load_all_indexes(self):
        """加载所有索引"""
        if not self.index_dir.exists():
            print(f"警告: 索引目录不存在: {self.index_dir}")
            return

        print(f"加载索引目录: {self.index_dir}")

        # 查找所有 .faiss 文件
        index_files = list(self.index_dir.glob("*.faiss"))

        if not index_files:
            print(f"警告: 没有找到索引文件")
            return

        for index_file in index_files:
            category = index_file.stem  # 去掉 .faiss 后缀

            try:
                index, mapping = self._load_index(category)
                self.indexes[category] = index
                self.mappings[category] = mapping
                print(f"  [OK] {category}: {index.ntotal} 条")
            except Exception as e:
                print(f"  [FAIL] {category}: 加载失败 - {e}")

        print(f"共加载 {len(self.indexes)} 个索引")

    def _load_index(self, category: str) -> Tuple[Any, Dict]:
        """
        加载单个索引

        Args:
            category: 分类名称

        Returns:
            (index, mapping)
        """
        index_path = self.index_dir / f"{category}.faiss"
        mapping_path = self.index_dir / f"{category}_mapping.pkl"

        if not index_path.exists():
            raise FileNotFoundError(f"索引文件不存在: {index_path}")
        if not mapping_path.exists():
            raise FileNotFoundError(f"映射文件不存在: {mapping_path}")

        # 加载索引
        index = faiss.read_index(str(index_path))

        # 加载映射
        with open(mapping_path, 'rb') as f:
            mapping = pickle.load(f)

        return index, mapping

    def search(
        self,
        query: str,
        category: str = None,
        k: int = 5,
        return_scores: bool = True
    ) -> List[Dict]:
        """
        向量检索

        Args:
            query: 查询文本
            category: 分类名称 (None 表示搜索所有分类)
            k: 返回 Top-K 结果
            return_scores: 是否返回相似度分数

        Returns:
            检索结果列表
        """
        if not self.indexes:
            return []

        # 编码查询
        query_vector = self.embedder.encode(query)
        query_vector = query_vector.reshape(1, -1).astype('float32')

        # 归一化
        faiss.normalize_L2(query_vector)

        # 搜索
        if category:
            # 单分类搜索
            return self._search_category(query_vector, category, k, return_scores)
        else:
            # 多分类搜索
            return self._search_all(query_vector, k, return_scores)

    def _search_category(
        self,
        query_vector: np.ndarray,
        category: str,
        k: int,
        return_scores: bool
    ) -> List[Dict]:
        """
        在单个分类中搜索

        Args:
            query_vector: 查询向量
            category: 分类名称
            k: 返回数量
            return_scores: 是否返回分数

        Returns:
            检索结果
        """
        if category not in self.indexes:
            return []

        index = self.indexes[category]
        mapping = self.mappings[category]

        # 搜索
        scores, indices = index.search(query_vector, k)

        # 组装结果
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:  # FAISS 可能返回 -1
                continue

            item = mapping["items"][idx].copy()
            if return_scores:
                item["score"] = float(score)
            results.append(item)

        return results

    def _search_all(
        self,
        query_vector: np.ndarray,
        k: int,
        return_scores: bool
    ) -> List[Dict]:
        """
        在所有分类中搜索

        Args:
            query_vector: 查询向量
            k: 每个分类返回数量
            return_scores: 是否返回分数

        Returns:
            检索结果
        """
        all_results = []

        for category, index in self.indexes.items():
            scores, indices = index.search(query_vector, k)
            mapping = self.mappings[category]

            for score, idx in zip(scores[0], indices[0]):
                if idx < 0:
                    continue

                item = mapping["items"][idx].copy()
                item["category"] = category
                if return_scores:
                    item["score"] = float(score)
                all_results.append(item)

        # 按分数排序
        if return_scores:
            all_results.sort(key=lambda x: x["score"], reverse=True)

        return all_results

    def get_categories(self) -> List[str]:
        """
        获取所有可用分类

        Returns:
            分类列表
        """
        return list(self.indexes.keys())

    def get_category_info(self, category: str) -> Dict:
        """
        获取分类信息

        Args:
            category: 分类名称

        Returns:
            分类信息
        """
        if category not in self.mappings:
            return {}

        mapping = self.mappings[category]
        return {
            "category": category,
            "size": mapping["size"],
            "index_size": self.indexes[category].ntotal,
        }

    def batch_search(
        self,
        queries: List[str],
        category: str = None,
        k: int = 5
    ) -> List[List[Dict]]:
        """
        批量检索

        Args:
            queries: 查询列表
            category: 分类名称
            k: 返回数量

        Returns:
            检索结果列表
        """
        results = []

        for query in queries:
            result = self.search(query, category=category, k=k)
            results.append(result)

        return results


def main():
    """测试向量存储"""
    import argparse

    parser = argparse.ArgumentParser(description="向量存储测试")
    parser.add_argument(
        "--index-dir",
        type=str,
        default="data/indexes",
        help="索引目录"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="交互模式"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("向量存储测试")
    print("=" * 60)

    # 创建向量存储
    try:
        store = VectorStore(index_dir=args.index_dir)
    except Exception as e:
        print(f"错误: {e}")
        return

    # 打印分类信息
    print("\n可用分类:")
    categories = store.get_categories()
    for cat in categories:
        info = store.get_category_info(cat)
        print(f"  {cat}: {info['size']} 条")

    # 测试查询
    test_queries = [
        "打开空调",
        "座椅加热",
        "车里太热了",
        "我想透透气",
    ]

    print("\n" + "=" * 60)
    print("测试检索")
    print("=" * 60)

    for query in test_queries:
        print(f"\n查询: {query}")

        # 全局搜索
        results = store.search(query, k=3)

        print(f"Top-3 结果:")
        for i, item in enumerate(results[:3], 1):
            print(f"  {i}. [{item.get('category', 'N/A')}] {item.get('text', 'N/A')}")
            print(f"      技能: {item.get('skill_name', 'N/A')} (分数: {item.get('score', 0):.4f})")

    # 交互模式
    if args.interactive:
        print("\n" + "=" * 60)
        print("交互模式 (输入 'quit' 退出)")
        print("=" * 60)

        while True:
            try:
                text = input("\n请输入查询: ").strip()

                if not text:
                    continue

                if text.lower() in ['quit', 'exit', 'q']:
                    print("再见!")
                    break

                # 搜索
                results = store.search(text, k=5)

                print(f"\n找到 {len(results)} 条结果:")
                for i, item in enumerate(results[:5], 1):
                    print(f"\n  {i}. [{item.get('category', 'N/A')}] {item.get('text', 'N/A')}")
                    print(f"     技能: {item.get('skill_name', 'N/A')}")
                    print(f"     分数: {item.get('score', 0):.4f}")

            except KeyboardInterrupt:
                print("\n\n再见!")
                break
            except Exception as e:
                print(f"错误: {e}")


if __name__ == "__main__":
    main()
