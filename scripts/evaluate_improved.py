"""
评估改进后的模型性能
"""

import json
import time
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
from src.router.textcnn_model import TextCNN, TextCNNLite
from src.router.train_router import TextDataset
from src.router.textcnn_enhanced import TextCNNEnhanced
from src.router.category_config import CategoryConfig


def load_test_data(suffix=""):
    """加载测试数据"""
    data_dir = Path("data/processed")
    test_file = f"test_data{suffix}.json" if suffix else "test_data.json"

    with open(data_dir / test_file, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_model(model, test_data, vocab, device="cuda", max_len=64):
    """评估模型"""
    model.eval()
    model.to(device)

    # 创建数据集
    dataset = TextDataset(test_data, vocab, max_len=max_len)

    # 批量预测
    correct = 0
    total = len(test_data)

    # 按批次处理
    batch_size = 128
    with torch.no_grad():
        for i in range(0, len(test_data), batch_size):
            batch_end = min(i + batch_size, len(test_data))
            batch_data = test_data[i:batch_end]

            # 编码
            texts = [item["text"] for item in batch_data]
            labels = [item["category_id"] for item in batch_data]

            # 转换为张量
            indices_list = []
            for text in texts:
                indices = []
                for char in text[:max_len]:
                    idx = vocab.get(char, vocab.get("<UNK>", 1))
                    indices.append(idx)

                if len(indices) < max_len:
                    indices.extend([vocab.get("<PAD>", 0)] * (max_len - len(indices)))

                indices_list.append(indices)

            indices_tensor = torch.tensor(indices_list, dtype=torch.long).to(device)
            labels_tensor = torch.tensor(labels, dtype=torch.long).to(device)

            # 预测
            outputs = model(indices_tensor)
            _, predicted = torch.max(outputs, 1)

            correct += (predicted == labels_tensor).sum().item()

    accuracy = correct / total
    return accuracy


def benchmark_latency(model, vocab, device="cuda", num_iterations=100):
    """测试延迟"""
    test_queries = [
        "打开空调", "关闭车窗", "座椅加热", "调节音量",
        "车里太热了", "我想透透气", "有点冷", "天太暗了",
        "开条缝", "透透气"
    ]

    model.eval()
    model.to(device)

    # 预热
    for query in test_queries[:3]:
        indices = []
        for char in query[:64]:
            idx = vocab.get(char, vocab.get("<UNK>", 1))
            indices.append(idx)

        if len(indices) < 64:
            indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

        indices_tensor = torch.tensor([indices], dtype=torch.long).to(device)

        with torch.no_grad():
            _ = model(indices_tensor)

    # 测试延迟
    latencies = []
    for _ in range(num_iterations):
        query = test_queries[_ % len(test_queries)]

        indices = []
        for char in query[:64]:
            idx = vocab.get(char, vocab.get("<UNK>", 1))
            indices.append(idx)

        if len(indices) < 64:
            indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

        indices_tensor = torch.tensor([indices], dtype=torch.long).to(device)

        start = time.time()
        with torch.no_grad():
            _ = model(indices_tensor)
        latency = (time.time() - start) * 1000
        latencies.append(latency)

    latencies = np.array(latencies)
    return {
        "mean": float(np.mean(latencies)),
        "std": float(np.std(latencies)),
        "min": float(np.min(latencies)),
        "max": float(np.max(latencies)),
        "p50": float(np.percentile(latencies, 50)),
        "p95": float(np.percentile(latencies, 95)),
        "p99": float(np.percentile(latencies, 99)),
    }


def main():
    print("=" * 70)
    print("模型性能评估")
    print("=" * 70)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    vocab = CategoryConfig.create_vocabulary()
    vocab_size = len(vocab)
    num_classes = len(CategoryConfig.CATEGORIES)

    # 加载原始数据测试集
    print("\n[原始数据]")
    test_data_original = load_test_data("")
    print(f"测试样本: {len(test_data_original)}")

    # 加载增强数据测试集
    print("\n[增强数据]")
    test_data_augmented = load_test_data("_augmented")
    print(f"测试样本: {len(test_data_augmented)}")

    results = {}

    # ========== 1. 原始 TextCNN (原始数据) ==========
    print("\n" + "=" * 70)
    print("模型1: 原始 TextCNN (在原始数据上训练)")
    print("=" * 70)

    try:
        model1 = TextCNNLite(vocab_size, num_classes=num_classes)
        model1_path = Path("data/models/router/best_model.pth")
        if model1_path.exists():
            model1.load_state_dict(torch.load(model1_path, map_location=device))

            # 测试准确率
            acc1_original = evaluate_model(model1, test_data_original, vocab, device)
            print(f"原始数据集准确率: {acc1_original*100:.2f}%")

            # 测试延迟
            lat1 = benchmark_latency(model1, vocab, device, num_iterations=100)
            print(f"平均延迟: {lat1['mean']:.2f}ms")

            # 获取模型信息
            info1 = model1.get_model_info()
            print(f"参数量: {info1['total_params']:,}")

            results["textcnn_original"] = {
                "accuracy_original": acc1_original,
                "latency": lat1,
                "params": info1['total_params']
            }
        else:
            print("模型文件不存在")
    except Exception as e:
        print(f"错误: {e}")

    # ========== 2. 增强版 TextCNN (增强数据) ==========
    print("\n" + "=" * 70)
    print("模型2: 增强版 TextCNN (在增强数据上训练)")
    print("=" * 70)

    try:
        model2 = TextCNNEnhanced(vocab_size, num_classes=num_classes)
        model2_path = Path("data/models/router_enhanced/best_model.pth")
        if model2_path.exists():
            model2.load_state_dict(torch.load(model2_path, map_location=device))

            # 测试准确率
            acc2_augmented = evaluate_model(model2, test_data_augmented, vocab, device)
            print(f"增强数据集准确率: {acc2_augmented*100:.2f}%")

            # 在原始数据上测试
            acc2_original = evaluate_model(model2, test_data_original, vocab, device)
            print(f"原始数据集准确率: {acc2_original*100:.2f}%")

            # 测试延迟
            lat2 = benchmark_latency(model2, vocab, device, num_iterations=100)
            print(f"平均延迟: {lat2['mean']:.2f}ms")

            # 获取模型信息
            info2 = model2.get_model_info()
            print(f"参数量: {info2['total_params']:,}")

            results["enhanced_augmented"] = {
                "accuracy_augmented": acc2_augmented,
                "accuracy_original": acc2_original,
                "latency": lat2,
                "params": info2['total_params']
            }
        else:
            print("模型文件不存在")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

    # ========== 总结 ==========
    print("\n" + "=" * 70)
    print("性能对比总结")
    print("=" * 70)

    if "textcnn_original" in results and "enhanced_augmented" in results:
        r1 = results["textcnn_original"]
        r2 = results["enhanced_augmented"]

        print(f"\n{'指标':<25} {'TextCNN':<20} {'TextCNN-Enhanced':<20} {'差异'}")
        print("-" * 85)

        # 准确率
        acc_diff = (r2["accuracy_original"] - r1["accuracy_original"]) * 100
        print(f"{'准确率 (原始数据)':<25} {r1['accuracy_original']*100:>6.2f}%{' ':14} {r2['accuracy_original']*100:>6.2f}%{' ':14} {acc_diff:+.2f}%")

        # 延迟
        lat_diff = r2["latency"]["mean"] - r1["latency"]["mean"]
        lat_ratio = r2["latency"]["mean"] / r1["latency"]["mean"] if r1["latency"]["mean"] > 0 else 0
        print(f"{'平均延迟':<25} {r1['latency']['mean']:>8.2f}ms{' ':12} {r2['latency']['mean']:>8.2f}ms{' ':12} {lat_ratio:.1f}x")

        # 参数量
        param_ratio = r2["params"] / r1["params"]
        print(f"{'参数量':<25} {r1['params']:>12,.0f}{' ':8} {r2['params']:>12,.0f}{' ':8} {param_ratio:.1f}x")

        # 结论
        print("\n" + "=" * 70)
        print("结论")
        print("=" * 70)

        if r2["accuracy_original"] > r1["accuracy_original"]:
            print(f"✓ 增强版准确率更高 (+{acc_diff:.2f}%)")
        else:
            print(f"✗ 原始版准确率更高 ({-acc_diff:.2f}%)")

        if r2["latency"]["mean"] < r1["latency"]["mean"]:
            print(f"✓ 增强版延迟更低 ({lat_ratio:.1f}x)")
        else:
            print(f"✗ 原始版延迟更低 ({1/lat_ratio:.1f}x)")


if __name__ == "__main__":
    main()
