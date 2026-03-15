"""
TextCNN 路由分类模型
轻量级字符级卷积神经网络，用于快速分类用户指令
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, List


class TextCNN(nn.Module):
    """
    TextCNN 模型

    架构:
    - 字符嵌入层
    - 多尺度卷积层 (2,3,4,5)
    - 最大池化层
    - 全连接层
    - Dropout 正则化
    """

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 128,
        num_filters: int = 256,
        filter_sizes: List[int] = [2, 3, 4, 5],
        num_classes: int = 13,
        dropout: float = 0.3,
        padding_idx: int = 0
    ):
        """
        初始化 TextCNN 模型

        Args:
            vocab_size: 词汇表大小
            embedding_dim: 嵌入维度
            num_filters: 每种卷积核的过滤器数量
            filter_sizes: 卷积核尺寸列表
            num_classes: 分类数量
            dropout: Dropout 比例
            padding_idx: 填充索引
        """
        super(TextCNN, self).__init__()

        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.num_filters = num_filters
        self.filter_sizes = filter_sizes
        self.num_classes = num_classes

        # 字符嵌入层
        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim,
            padding_idx=padding_idx
        )

        # 多尺度卷积层
        self.convs = nn.ModuleList([
            nn.Conv1d(
                embedding_dim,
                num_filters,
                kernel_size=fs,
                padding=fs // 2
            )
            for fs in filter_sizes
        ])

        # 批归一化
        self.batch_norms = nn.ModuleList([
            nn.BatchNorm1d(num_filters)
            for _ in filter_sizes
        ])

        # Dropout
        self.dropout = nn.Dropout(dropout)

        # 全连接层
        total_filters = num_filters * len(filter_sizes)
        self.fc1 = nn.Linear(total_filters, total_filters // 2)
        self.fc2 = nn.Linear(total_filters // 2, num_classes)

        # 初始化权重
        self._init_weights()

    def _init_weights(self):
        """初始化模型权重"""
        # 嵌入层
        nn.init.uniform_(self.embedding.weight, -0.1, 0.1)

        # 卷积层
        for conv in self.convs:
            nn.init.kaiming_normal_(conv.weight, mode='fan_out', nonlinearity='relu')
            if conv.bias is not None:
                nn.init.constant_(conv.bias, 0)

        # 批归一化层
        for bn in self.batch_norms:
            nn.init.constant_(bn.weight, 1)
            nn.init.constant_(bn.bias, 0)

        # 全连接层
        nn.init.xavier_uniform_(self.fc1.weight)
        nn.init.constant_(self.fc1.bias, 0)
        nn.init.xavier_uniform_(self.fc2.weight)
        nn.init.constant_(self.fc2.bias, 0)

    def forward(self, x: torch.Tensor, return_features: bool = False) -> torch.Tensor:
        """
        前向传播

        Args:
            x: 输入张量 [batch_size, seq_len]
            return_features: 是否返回中间特征

        Returns:
            输出 logits [batch_size, num_classes]
        """
        # 嵌入 [batch_size, seq_len, embedding_dim]
        embedded = self.embedding(x)

        # 转置以适应 Conv1d [batch_size, embedding_dim, seq_len]
        embedded = embedded.transpose(1, 2)

        # 多尺度卷积 + 激活 + 池化
        conv_outputs = []
        for i, (conv, bn) in enumerate(zip(self.convs, self.batch_norms)):
            # 卷积
            conv_out = conv(embedded)
            # 批归一化
            conv_out = bn(conv_out)
            # 激活
            conv_out = F.relu(conv_out)
            # 最大池化 (在序列维度上)
            pooled = F.max_pool1d(conv_out, conv_out.size(2))
            # 压缩维度 [batch_size, num_filters]
            conv_outputs.append(pooled.squeeze(2))

        # 拼接所有卷积输出 [batch_size, total_filters]
        features = torch.cat(conv_outputs, dim=1)

        # Dropout
        features = self.dropout(features)

        # 如果需要返回特征
        if return_features:
            return features

        # 全连接层
        out = self.fc1(features)
        out = F.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)

        return out

    def predict(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        预测分类

        Args:
            x: 输入张量 [batch_size, seq_len]

        Returns:
            (predictions, probabilities)
            - predictions: 预测类别 [batch_size]
            - probabilities: 类别概率 [batch_size, num_classes]
        """
        logits = self.forward(x)
        probs = F.softmax(logits, dim=1)
        preds = torch.argmax(probs, dim=1)
        return preds, probs

    def get_model_size(self) -> int:
        """
        获取模型大小（参数数量）

        Returns:
            参数数量
        """
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def get_model_info(self) -> dict:
        """
        获取模型信息

        Returns:
            模型信息字典
        """
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)

        return {
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "num_filters": self.num_filters,
            "filter_sizes": self.filter_sizes,
            "num_classes": self.num_classes,
            "total_params": total_params,
            "trainable_params": trainable_params,
            "model_size_mb": total_params * 4 / (1024 * 1024),  # float32
        }


class TextCNNLite(TextCNN):
    """
    TextCNN 轻量版

    更少的参数，适合端侧部署
    """

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 64,
        num_filters: int = 128,
        filter_sizes: List[int] = [2, 3, 4],
        num_classes: int = 13,
        dropout: float = 0.2,
        padding_idx: int = 0
    ):
        super().__init__(
            vocab_size=vocab_size,
            embedding_dim=embedding_dim,
            num_filters=num_filters,
            filter_sizes=filter_sizes,
            num_classes=num_classes,
            dropout=dropout,
            padding_idx=padding_idx
        )


def create_model(
    vocab_size: int,
    num_classes: int = 13,
    lite: bool = True,
    pretrained: str = None
) -> TextCNN:
    """
    创建 TextCNN 模型

    Args:
        vocab_size: 词汇表大小
        num_classes: 分类数量
        lite: 是否使用轻量版
        pretrained: 预训练权重路径

    Returns:
        TextCNN 模型
    """
    if lite:
        model = TextCNNLite(vocab_size, num_classes=num_classes)
    else:
        model = TextCNN(vocab_size, num_classes=num_classes)

    # 加载预训练权重
    if pretrained:
        state_dict = torch.load(pretrained, map_location='cpu')
        model.load_state_dict(state_dict)
        print(f"已加载预训练权重: {pretrained}")

    return model


def main():
    """测试模型"""
    from src.router.category_config import CategoryConfig

    # 创建词汇表
    vocab = CategoryConfig.create_vocabulary()
    vocab_size = len(vocab)
    num_classes = len(CategoryConfig.CATEGORIES)

    print("=" * 60)
    print("TextCNN 模型测试")
    print("=" * 60)

    # 创建模型
    model = TextCNN(vocab_size, num_classes=num_classes)

    # 打印模型信息
    info = model.get_model_info()
    print("\n模型信息:")
    for key, value in info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    # 测试前向传播
    batch_size = 4
    seq_len = 64
    x = torch.randint(0, vocab_size, (batch_size, seq_len))

    print(f"\n输入形状: {x.shape}")

    # 前向传播
    logits = model(x)
    print(f"输出形状: {logits.shape}")

    # 预测
    preds, probs = model.predict(x)
    print(f"预测结果: {preds}")
    print(f"概率分布:\n{probs[0]}")

    # 测试轻量版
    print("\n" + "=" * 60)
    print("TextCNN Lite 模型测试")
    print("=" * 60)

    lite_model = TextCNNLite(vocab_size, num_classes=num_classes)
    lite_info = lite_model.get_model_info()

    print("\n轻量版模型信息:")
    for key, value in lite_info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    print(f"\n参数减少: {(info['total_params'] - lite_info['total_params']) / info['total_params'] * 100:.1f}%")


if __name__ == "__main__":
    main()
