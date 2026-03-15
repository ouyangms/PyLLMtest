"""
比较原始模型和千问增强模型的性能
"""

import json
import sys
sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.train_router import TextDataset
from src.router.category_config import CategoryConfig


def evaluate_model(model_path, test_data_path, device="cuda"):
    """评估模型"""
    # 加载测试数据
    with open(test_data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # 创建词汇表
    vocab = CategoryConfig.create_vocabulary()

    # 创建数据集
    dataset = TextDataset(test_data, vocab, max_len=64)

    # 加载模型
    model = TextCNNLite(len(vocab), num_classes=13)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    # 评估
    correct = 0
    batch_size = 128

    with torch.no_grad():
        for i in range(0, len(test_data), batch_size):
            batch_end = min(i + batch_size, len(test_data))
            batch_data = test_data[i:batch_end]

            # 编码
            indices_list = []
            for item in batch_data:
                indices = []
                for char in item["text"][:64]:
                    idx = vocab.get(char, vocab.get("<UNK>", 1))
                    indices.append(idx)

                if len(indices) < 64:
                    indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

                indices_list.append(indices)

            indices_tensor = torch.tensor(indices_list, dtype=torch.long).to(device)
            labels_tensor = torch.tensor([item["category_id"] for item in batch_data], dtype=torch.long).to(device)

            # 预测
            outputs = model(indices_tensor)
            _, predicted = torch.max(outputs, 1)

            correct += (predicted == labels_tensor).sum().item()

    accuracy = correct / len(test_data)
    return accuracy, len(test_data)


print("=" * 70)
print("模型性能对比")
print("=" * 70)

device = "cuda" if torch.cuda.is_available() else "cpu"

# 原始模型（原始数据训练）
print("\n[1] 原始 TextCNN (原始数据训练)")
acc1, n1 = evaluate_model(
    "data/models/router/best_model.pth",
    "data/processed/test_data.json",
    device
)
print(f"  测试准确率: {acc1*100:.2f}%")
print(f"  测试样本数: {n1}")

# 千问增强模型（千问数据训练）
print("\n[2] TextCNN (千问增强数据训练)")
acc2, n2 = evaluate_model(
    "data/models/router_qwen/best_model.pth",
    "data/processed/test_data_qwen.json",
    device
)
print(f"  测试准确率: {acc2*100:.2f}%")
print(f"  测试样本数: {n2}")

# 千问增强模型（在原始数据上测试）
print("\n[3] TextCNN (千问增强数据训练) - 在原始数据上测试")
acc3, n3 = evaluate_model(
    "data/models/router_qwen/best_model.pth",
    "data/processed/test_data.json",
    device
)
print(f"  测试准确率: {acc3*100:.2f}%")
print(f"  测试样本数: {n3}")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)
print(f"原始 TextCNN (原始数据):           {acc1*100:.2f}%")
print(f"TextCNN (千问数据):                 {acc2*100:.2f}% (千问测试集)")
print(f"TextCNN (千问数据):                 {acc3*100:.2f}% (原始测试集)")

print(f"\n提升: {(acc3-acc1)*100:+.2f}% (在原始测试集上)")
