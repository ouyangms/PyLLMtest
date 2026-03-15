"""
嵌入模型接口
集成 bge-small-zh-v1.5 等中文嵌入模型
"""

import os
from pathlib import Path
from typing import List, Union

import numpy as np


class TextEmbedder:
    """文本嵌入器基类"""

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        编码文本为向量

        Args:
            texts: 单个文本或文本列表

        Returns:
            嵌入向量
        """
        raise NotImplementedError


class DummyEmbedder(TextEmbedder):
    """
    临时使用的伪嵌入器
    用于在没有 sentence-transformers 时进行测试
    """

    def __init__(self, dim: int = 384):
        """
        初始化伪嵌入器

        Args:
            dim: 向量维度
        """
        self.dim = dim
        print("警告: 使用伪嵌入器，向量是随机的，仅用于测试!")

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        生成随机嵌入向量

        Args:
            texts: 文本或文本列表

        Returns:
            嵌入向量 [n, dim]
        """
        single_input = isinstance(texts, str)
        if single_input:
            texts = [texts]

        # 基于文本长度生成伪随机向量
        vectors = []
        for text in texts:
            np.random.seed(hash(text) % (2 ** 32))
            vec = np.random.randn(self.dim).astype(np.float32)
            # L2 归一化
            vec = vec / np.linalg.norm(vec)
            vectors.append(vec)

        result = np.stack(vectors)
        return result[0] if single_input else result


class SentenceTransformerEmbedder(TextEmbedder):
    """
    SentenceTransformer 嵌入器
    支持 bge-small-zh-v1.5 等模型
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-zh-v1.5",
        device: str = "cpu",
        cache_dir: str = None
    ):
        """
        初始化嵌入器

        Args:
            model_name: 模型名称
            device: 设备 (cuda/cpu)
            cache_dir: 缓存目录
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "需要安装 sentence-transformers: pip install sentence-transformers"
            )

        self.model_name = model_name
        self.device = device

        # 设置缓存目录
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent.parent / "data" / "models" / "embeddings"
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)

        print(f"加载嵌入模型: {model_name}")
        print(f"设备: {device}")
        print(f"缓存目录: {cache_dir}")

        self.model = SentenceTransformer(
            model_name,
            device=device,
            cache_folder=str(cache_dir)
        )

        self.dim = self.model.get_sentence_embedding_dimension()
        print(f"向量维度: {self.dim}")

    def encode(
        self,
        texts: Union[str, List[str]],
        normalize: bool = True,
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """
        编码文本为向量

        Args:
            texts: 文本或文本列表
            normalize: 是否 L2 归一化
            batch_size: 批大小
            show_progress: 是否显示进度

        Returns:
            嵌入向量 [n, dim]
        """
        single_input = isinstance(texts, str)
        if single_input:
            texts = [texts]

        # 编码
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=normalize,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )

        return embeddings[0] if single_input else embeddings


class BGESmallEmbedder(SentenceTransformerEmbedder):
    """
    bge-small-zh-v1.5 专用嵌入器

    特点:
    - 中文专用
    - 384 维
    - 约 30MB
    - 速度较快，适合端侧
    """

    def __init__(self, device: str = "cpu"):
        super().__init__(
            model_name="BAAI/bge-small-zh-v1.5",
            device=device
        )


class BGEBaseEmbedder(SentenceTransformerEmbedder):
    """
    bge-base-zh-v1.5 嵌入器

    特点:
    - 中文专用
    - 768 维
    - 约 100MB
    - 精度更高
    """

    def __init__(self, device: str = "cpu"):
        super().__init__(
            model_name="BAAI/bge-base-zh-v1.5",
            device=device
        )


def create_embedder(
    model_type: str = "auto",
    device: str = "cpu"
) -> TextEmbedder:
    """
    创建嵌入器

    Args:
        model_type: 模型类型 (auto, bge-small, bge-base, dummy)
        device: 设备 (cuda/cpu)

    Returns:
        嵌入器实例
    """
    # 检测 CUDA
    if device == "cuda":
        try:
            import torch
            if not torch.cuda.is_available():
                print("CUDA 不可用，使用 CPU")
                device = "cpu"
        except ImportError:
            print("PyTorch 未安装，使用 CPU")
            device = "cpu"

    if model_type == "auto":
        # 尝试导入 sentence-transformers
        try:
            import sentence_transformers
            model_type = "bge-small"
        except ImportError:
            print("未安装 sentence-transformers，使用伪嵌入器")
            model_type = "dummy"

    if model_type == "bge-small":
        return BGESmallEmbedder(device=device)
    elif model_type == "bge-base":
        return BGEBaseEmbedder(device=device)
    elif model_type == "dummy":
        return DummyEmbedder()
    else:
        raise ValueError(f"未知的模型类型: {model_type}")


def main():
    """测试嵌入器"""
    import argparse

    parser = argparse.ArgumentParser(description="文本嵌入器测试")
    parser.add_argument(
        "--model",
        type=str,
        default="auto",
        choices=["auto", "bge-small", "bge-base", "dummy"],
        help="模型类型"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if __import__("torch").cuda.is_available() else "cpu",
        help="设备"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("文本嵌入器测试")
    print("=" * 60)

    # 创建嵌入器
    embedder = create_embedder(args.model, args.device)

    # 测试文本
    test_texts = [
        "打开空调",
        "座椅加热",
        "车窗开一点",
        "我想透透气",
        "车里太热了",
    ]

    print("\n测试文本:")
    for text in test_texts:
        print(f"  - {text}")

    # 编码
    print("\n编码中...")
    embeddings = embedder.encode(test_texts)

    print(f"\n向量形状: {embeddings.shape}")
    print(f"向量维度: {embeddings.shape[1]}")
    print(f"数据类型: {embeddings.dtype}")

    # 计算相似度
    print("\n相似度矩阵 (余弦):")
    print("-" * 60)

    for i, text1 in enumerate(test_texts):
        print(f"\n'{text1}' 与其他文本的相似度:")
        for j, text2 in enumerate(test_texts):
            if i != j:
                # 余弦相似度 (已归一化，直接点积)
                sim = np.dot(embeddings[i], embeddings[j])
                print(f"  '{text2}': {sim:.4f}")

    # 测试单个文本
    print("\n" + "=" * 60)
    print("单个文本测试")
    print("=" * 60)

    single_text = "打开主驾空调"
    single_embedding = embedder.encode(single_text)

    print(f"文本: {single_text}")
    print(f"向量形状: {single_embedding.shape}")
    print(f"向量前10维: {single_embedding[:10]}")

    print("\n测试完成!")


if __name__ == "__main__":
    main()
