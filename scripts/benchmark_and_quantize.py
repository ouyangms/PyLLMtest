"""
模型量化和性能优化
评估当前模型，并进行FP16/INT8量化
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
import torch.nn as nn
from torch.quantization import quantize_dynamic
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig


def benchmark_model(model, test_data, vocab, device="cuda", num_iterations=100):
    """基准测试模型性能"""
    model.eval()
    model.to(device)

    # 预热
    for _ in range(10):
        text = "打开空调"
        indices = []
        for char in text[:64]:
            idx = vocab.get(char, vocab.get("<UNK>", 1))
            indices.append(idx)
        if len(indices) < 64:
            indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

        indices_tensor = torch.tensor([indices], dtype=torch.long).to(device)
        with torch.no_grad():
            _ = model(indices_tensor)

    # 测试推理速度
    latencies = []
    with torch.no_grad():
        for _ in range(num_iterations):
            text = test_data[_ % len(test_data)]["text"]

            indices = []
            for char in text[:64]:
                idx = vocab.get(char, vocab.get("<UNK>", 1))
                indices.append(idx)

            if len(indices) < 64:
                indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

            indices_tensor = torch.tensor([indices], dtype=torch.long).to(device)

            start = time.perf_counter()
            outputs = model(indices_tensor)
            latency = (time.perf_counter() - start) * 1000
            latencies.append(latency)

    # 计算统计数据
    import numpy as np
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


def evaluate_model(model, test_data, vocab, device="cuda"):
    """评估模型准确率"""
    model.eval()
    model.to(device)

    correct = 0
    batch_size = 128

    with torch.no_grad():
        for i in range(0, len(test_data), batch_size):
            batch_end = min(i + batch_size, len(test_data))
            batch_data = test_data[i:batch_end]

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

            outputs = model(indices_tensor)
            _, predicted = torch.max(outputs, 1)

            correct += (predicted == labels_tensor).sum().item()

    accuracy = correct / len(test_data)
    return accuracy


def quantize_model_fp16(model):
    """FP16量化"""
    return model.half()


def quantize_model_int8(model):
    """INT8动态量化"""
    return quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)


def get_model_size(model):
    """获取模型大小（参数数量）"""
    param_size = 0
    for param in model.parameters():
        param_size += param.numel() * param.element_size()
    buffer_size = 0
    for buffer in model.buffers():
        buffer_size += buffer.numel() * buffer.element_size()

    size_mb = (param_size + buffer_size) / (1024 * 1024)
    return size_mb


def main():
    print("=" * 70)
    print("模型量化和性能优化")
    print("=" * 70)

    # 加载测试数据
    data_dir = Path("data/processed")
    with open(data_dir / "test_data_clean.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    print(f"\n测试数据: {len(test_data)} 个样本")

    vocab = CategoryConfig.create_vocabulary()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 加载原始模型
    print(f"\n使用设备: {device}")
    print(f"\n加载原始模型...")
    model_fp32 = TextCNNLite(len(vocab), num_classes=13)
    model_fp32.load_state_dict(torch.load("data/models/router_clean_final/best_model.pth", map_location=device))

    # 评估FP32模型
    print(f"\n评估 FP32 模型...")
    acc_fp32 = evaluate_model(model_fp32, test_data[:100], vocab, device)  # 使用部分数据加速
    size_fp32 = get_model_size(model_fp32)
    latency_fp32 = benchmark_model(model_fp32, test_data, vocab, device, num_iterations=50)

    print(f"\nFP32 模型:")
    print(f"  准确率: {acc_fp32*100:.2f}%")
    print(f"  模型大小: {size_fp32:.2f} MB")
    print(f"  平均延迟: {latency_fp32['mean']:.2f} ms")
    print(f"  P95 延迟: {latency_fp32['p95']:.2f} ms")

    # FP16量化
    print(f"\n执行 FP16 量化...")
    model_fp16 = TextCNNLite(len(vocab), num_classes=13)
    model_fp16.load_state_dict(torch.load("data/models/router_clean_final/best_model.pth", map_location=device))
    model_fp16 = quantize_model_fp16(model_fp16)

    acc_fp16 = evaluate_model(model_fp16, test_data[:100], vocab, device)
    size_fp16 = get_model_size(model_fp16)
    latency_fp16 = benchmark_model(model_fp16, test_data, vocab, device, num_iterations=50)

    print(f"\nFP16 模型:")
    print(f"  准确率: {acc_fp16*100:.2f}%")
    print(f"  模型大小: {size_fp16:.2f} MB")
    print(f"  平均延迟: {latency_fp16['mean']:.2f} ms")
    print(f"  P95 延迟: {latency_fp16['p95']:.2f} ms")

    # INT8量化（仅CPU）
    print(f"\n执行 INT8 量化（CPU）...")
    device_int8 = "cpu"
    model_int8 = TextCNNLite(len(vocab), num_classes=13)
    model_int8.load_state_dict(torch.load("data/models/router_clean_final/best_model.pth", map_location=device_int8))
    model_int8 = quantize_model_int8(model_int8)

    acc_int8 = evaluate_model(model_int8, test_data[:100], vocab, device_int8)
    size_int8 = get_model_size(model_int8)
    latency_int8 = benchmark_model(model_int8, test_data, vocab, device_int8, num_iterations=50)

    print(f"\nINT8 模型 (CPU):")
    print(f"  准确率: {acc_int8*100:.2f}%")
    print(f"  模型大小: {size_int8:.2f} MB")
    print(f"  平均延迟: {latency_int8['mean']:.2f} ms")
    print(f"  P95 延迟: {latency_int8['p95']:.2f} ms")

    # 总结对比
    print("\n" + "=" * 70)
    print("性能对比总结")
    print("=" * 70)

    print(f"\n{'模型':<10} {'准确率':<12} {'大小':<12} {'平均延迟':<12} {'P95延迟':<12}")
    print("-" * 60)
    print(f"{'FP32':<10} {acc_fp32*100:>10.2f}% {size_fp32:>10.2f} MB {latency_fp32['mean']:>10.2f} ms {latency_fp32['p95']:>10.2f} ms")
    print(f"{'FP16':<10} {acc_fp16*100:>10.2f}% {size_fp16:>10.2f} MB {latency_fp16['mean']:>10.2f} ms {latency_fp16['p95']:>10.2f} ms")
    print(f"{'INT8':<10} {acc_int8*100:>10.2f}% {size_int8:>10.2f} MB {latency_int8['mean']:>10.2f} ms {latency_int8['p95']:>10.2f} ms")

    print(f"\n相比 FP32:")
    print(f"  FP16: 大小减少 {(1-size_fp16/size_fp32)*100:.1f}%, 延迟变化 {(latency_fp16['mean']/latency_fp32['mean']-1)*100:+.1f}%")
    print(f"  INT8: 大小减少 {(1-size_int8/size_fp32)*100:.1f}%, 延迟变化 {(latency_int8['mean']/latency_fp32['mean']-1)*100:+.1f}%")


if __name__ == "__main__":
    main()
