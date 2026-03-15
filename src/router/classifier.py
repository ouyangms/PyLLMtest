"""
路由分类器推理接口
加载训练好的模型进行推理预测
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union

import torch
import torch.nn.functional as F

from .textcnn_model import TextCNN, TextCNNLite
from ..router.category_config import CategoryConfig


class RouterClassifier:
    """路由分类器"""

    def __init__(
        self,
        model_path: str = None,
        vocab: Dict[str, int] = None,
        device: str = "cpu",
        max_len: int = 64
    ):
        """
        初始化分类器

        Args:
            model_path: 模型权重路径
            vocab: 词汇表
            device: 设备 (cuda/cpu)
            max_len: 最大序列长度
        """
        self.device = device
        self.max_len = max_len

        # 加载词汇表
        if vocab is None:
            self.vocab = CategoryConfig.create_vocabulary()
        else:
            self.vocab = vocab

        # 加载模型
        if model_path is None:
            # 默认路径
            model_path = Path(__file__).parent.parent.parent / "data" / "models" / "router" / "best_model.pth"
        else:
            model_path = Path(model_path)

        # 推断模型类型
        is_lite = True  # 默认使用轻量版

        # 创建模型
        vocab_size = len(self.vocab)
        num_classes = len(CategoryConfig.CATEGORIES)

        if is_lite:
            self.model = TextCNNLite(vocab_size, num_classes=num_classes)
        else:
            self.model = TextCNN(vocab_size, num_classes=num_classes)

        # 加载权重
        if model_path.exists():
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            print(f"已加载模型: {model_path}")
        else:
            print(f"警告: 模型文件不存在: {model_path}")
            print("使用未训练的模型")

        self.model.to(self.device)
        self.model.eval()

    def encode_text(self, text: str) -> torch.Tensor:
        """
        将文本编码为索引序列

        Args:
            text: 输入文本

        Returns:
            索引张量 [1, seq_len]
        """
        indices = []
        for char in text[:self.max_len]:
            idx = self.vocab.get(char, self.vocab.get("<UNK>", 1))
            indices.append(idx)

        # 填充
        if len(indices) < self.max_len:
            indices.extend([self.vocab.get("<PAD>", 0)] * (self.max_len - len(indices)))

        return torch.tensor([indices], dtype=torch.long).to(self.device)

    def predict(
        self,
        text: str,
        return_probs: bool = False
    ) -> Union[str, Tuple[str, Dict[str, float]]]:
        """
        预测单个文本

        Args:
            text: 输入文本
            return_probs: 是否返回概率

        Returns:
            预测分类名称，或 (分类名称, 概率字典)
        """
        # 编码
        indices = self.encode_text(text)

        # 预测
        with torch.no_grad():
            logits = self.model(indices)
            probs = F.softmax(logits, dim=1)

            # 获取预测结果
            prob, pred = torch.max(probs, 1)
            category_id = pred.item()
            confidence = prob.item()

        # 转换为分类名称
        category_name = CategoryConfig.get_category_name(category_id)

        if return_probs:
            # 返回所有分类的概率
            prob_dict = {}
            for i, cat_name in enumerate(CategoryConfig.CATEGORIES):
                prob_dict[cat_name] = probs[0][i].item()

            return category_name, prob_dict
        else:
            return category_name

    def predict_batch(
        self,
        texts: List[str],
        return_probs: bool = False
    ) -> List[Union[str, Tuple[str, Dict[str, float]]]]:
        """
        批量预测

        Args:
            texts: 输入文本列表
            return_probs: 是否返回概率

        Returns:
            预测结果列表
        """
        results = []

        for text in texts:
            result = self.predict(text, return_probs=return_probs)
            results.append(result)

        return results

    def predict_top_k(
        self,
        text: str,
        k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        预测 Top-K 分类

        Args:
            text: 输入文本
            k: 返回前 k 个分类

        Returns:
            [(分类名称, 概率), ...] 列表
        """
        # 编码
        indices = self.encode_text(text)

        # 预测
        with torch.no_grad():
            logits = self.model(indices)
            probs = F.softmax(logits, dim=1)

            # 获取 Top-K
            top_probs, top_indices = torch.topk(probs, k, dim=1)

        # 转换结果
        results = []
        for i in range(k):
            category_id = top_indices[0][i].item()
            prob = top_probs[0][i].item()
            category_name = CategoryConfig.get_category_name(category_id)
            results.append((category_name, prob))

        return results

    def get_category_info(self, category: str) -> Dict:
        """
        获取分类信息

        Args:
            category: 分类名称

        Returns:
            分类信息字典
        """
        return {
            "name": category,
            "id": CategoryConfig.get_category_id(category),
            "domain": CategoryConfig.get_domain(category),
        }


def main():
    """测试分类器"""
    import argparse

    parser = argparse.ArgumentParser(description="路由分类器推理")
    parser.add_argument(
        "--model",
        type=str,
        default="data/models/router/best_model.pth",
        help="模型路径"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="设备"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="交互模式"
    )

    args = parser.parse_args()

    # 创建分类器
    print("=" * 60)
    print("路由分类器")
    print("=" * 60)

    classifier = RouterClassifier(
        model_path=args.model,
        device=args.device
    )

    # 测试样本
    test_queries = [
        "打开空调",
        "座椅加热",
        "车窗开一点",
        "打开阅读灯",
        "折叠后视镜",
        "查询胎压",
        "播放音乐",
        "开启导航",
    ]

    print("\n" + "=" * 60)
    print("测试预测")
    print("=" * 60)

    for query in test_queries:
        result = classifier.predict(query, return_probs=True)

        if isinstance(result, tuple):
            category, probs = result
            print(f"\n查询: {query}")
            print(f"预测: {category}")

            # 显示 Top-3
            sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
            print("Top-3:")
            for cat, prob in sorted_probs[:3]:
                print(f"  {cat}: {prob:.4f}")
        else:
            print(f"\n查询: {query}")
            print(f"预测: {result}")

    # 交互模式
    if args.interactive:
        print("\n" + "=" * 60)
        print("交互模式 (输入 'quit' 退出)")
        print("=" * 60)

        while True:
            try:
                text = input("\n请输入指令: ").strip()

                if not text:
                    continue

                if text.lower() in ['quit', 'exit', 'q']:
                    print("再见!")
                    break

                # 预测
                result = classifier.predict_top_k(text, k=3)

                print(f"\n预测结果 (Top-3):")
                for i, (category, prob) in enumerate(result, 1):
                    info = classifier.get_category_info(category)
                    print(f"  {i}. {category} ({info['domain']}) - {prob:.4f}")

            except KeyboardInterrupt:
                print("\n\n再见!")
                break
            except Exception as e:
                print(f"错误: {e}")


if __name__ == "__main__":
    main()
