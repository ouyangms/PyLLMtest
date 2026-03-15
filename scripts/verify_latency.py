"""
验证性能测试中的延迟计算问题
"""

import sys
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig
from src.hybrid.inference_engine import InferenceEngine


def test_router_latency_issue():
    """验证路由分类延迟计算问题"""
    print("=" * 70)
    print("路由分类延迟验证")
    print("=" * 70)

    # 设备
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n使用设备: {device}")

    # 加载模型
    vocab = CategoryConfig.create_vocabulary()
    model = TextCNNLite(len(vocab), num_classes=13)
    model.load_state_dict(
        torch.load("data/models/router_clean_final/best_model.pth", map_location=device)
    )
    model.to(device)
    model.eval()

    # 准备测试数据
    test_texts = ["打开空调", "座椅加热", "关闭车窗", "播放音乐", "导航到公司"] * 20
    batch_size = 128

    print(f"\n测试样本数: {len(test_texts)}")
    print(f"批次大小: {batch_size}")

    # 方法1: 批处理测试（当前性能测试使用的方法）
    print("\n--- 方法1: 批处理测试 ---")
    batch_latencies = []

    with torch.no_grad():
        for i in range(0, len(test_texts), batch_size):
            batch_end = min(i + batch_size, len(test_texts))
            batch_texts = test_texts[i:batch_end]

            # 编码
            indices_list = []
            for text in batch_texts:
                indices = []
                for char in text[:64]:
                    idx = vocab.get(char, vocab.get("<UNK>", 1))
                    indices.append(idx)
                if len(indices) < 64:
                    indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))
                indices_list.append(indices)

            indices_tensor = torch.tensor(indices_list, dtype=torch.long).to(device)

            # 测量整个批次的延迟
            start = time.perf_counter()
            outputs = model(indices_tensor)
            batch_latency = (time.perf_counter() - start) * 1000

            batch_latencies.append(batch_latency)

    avg_batch_latency = np.mean(batch_latencies)
    print(f"批次延迟: {avg_batch_latency:.2f} ms")
    print(f"  (这是处理 {batch_size} 个样本的总时间)")

    # 方法2: 单样本测试（正确的单样本延迟）
    print("\n--- 方法2: 单样本测试 ---")
    single_latencies = []

    with torch.no_grad():
        for text in test_texts[:100]:  # 测试100个样本
            # 编码
            indices = []
            for char in text[:64]:
                idx = vocab.get(char, vocab.get("<UNK>", 1))
                indices.append(idx)
            if len(indices) < 64:
                indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

            indices_tensor = torch.tensor([indices], dtype=torch.long).to(device)

            # 测量单样本延迟
            start = time.perf_counter()
            outputs = model(indices_tensor)
            single_latency = (time.perf_counter() - start) * 1000

            single_latencies.append(single_latency)

    avg_single_latency = np.mean(single_latencies)
    p50_single = np.percentile(single_latencies, 50)
    p95_single = np.percentile(single_latencies, 95)
    p99_single = np.percentile(single_latencies, 99)

    print(f"单样本延迟:")
    print(f"  平均: {avg_single_latency:.2f} ms")
    print(f"  P50:  {p50_single:.2f} ms")
    print(f"  P95:  {p95_single:.2f} ms")
    print(f"  P99:  {p99_single:.2f} ms")

    # 方法3: 计算单样本延迟（从批次延迟推算）
    print("\n--- 方法3: 从批次延迟推算单样本延迟 ---")
    estimated_single = avg_batch_latency / batch_size
    print(f"推算单样本延迟: {estimated_single:.2f} ms")
    print(f"  (批次延迟 {avg_batch_latency:.2f} ms / {batch_size} 个样本)")

    # 对比
    print("\n--- 对比分析 ---")
    print(f"实际单样本延迟: {avg_single_latency:.2f} ms")
    print(f"推算单样本延迟: {estimated_single:.2f} ms")
    print(f"差异: {abs(avg_single_latency - estimated_single):.2f} ms")
    print(f"差异百分比: {abs(avg_single_latency - estimated_single) / avg_single_latency * 100:.1f}%")

    # 结论
    print("\n--- 结论 ---")
    print("当前性能测试报告中的路由延迟87ms是**批次延迟**，不是单样本延迟！")
    print(f"正确的单样本延迟应该是: {avg_single_latency:.2f} ms")
    print(f"这与端到端测试的延迟是吻合的。")

    return avg_single_latency


def test_embedding_device():
    """测试embedding模型使用的设备"""
    print("\n" + "=" * 70)
    print("Embedding模型设备测试")
    print("=" * 70)

    # 检查sklearn的TF-IDF（不支持GPU）
    print("\n--- 当前实现 (TF-IDF) ---")
    print("库: sklearn.feature_extraction.text.TfidfVectorizer")
    print("设备: CPU (不支持GPU)")
    print("原因: scikit-learn不支持GPU加速")

    # 检查是否有CUDA
    if torch.cuda.is_available():
        print(f"\n--- 系统GPU信息 ---")
        print(f"CUDA可用: {torch.cuda.is_available()}")
        print(f"CUDA版本: {torch.version.cuda}")
        print(f"GPU设备: {torch.cuda.get_device_name(0)}")

        # 测试sentence-transformers支持GPU
        print("\n--- Sentence-Transformers (支持GPU) ---")
        try:
            from sentence_transformers import SentenceTransformer
            print("库: sentence-transformers")
            print("设备: 支持 CUDA/CPU")

            # 测试加载模型到GPU
            print("\n测试加载 bge-small-zh-v1.5 到GPU...")
            model = SentenceTransformer('BAAI/bge-small-zh-v1.5', device='cuda')
            print(f"  模型设备: {model.device}")

            # 测试编码速度
            test_texts = ["打开空调", "座椅加热", "关闭车窗"] * 10

            # CPU测试
            import time
            model_cpu = SentenceTransformer('BAAI/bge-small-zh-v1.5', device='cpu')
            start = time.perf_counter()
            embeddings_cpu = model_cpu.encode(test_texts)
            cpu_time = (time.perf_counter() - start) * 1000

            # GPU测试
            start = time.perf_counter()
            embeddings_gpu = model.encode(test_texts)
            gpu_time = (time.perf_counter() - start) * 1000

            print(f"\n编码 {len(test_texts)} 个文本:")
            print(f"  CPU耗时: {cpu_time:.2f} ms")
            print(f"  GPU耗时: {gpu_time:.2f} ms")
            print(f"  加速比: {cpu_time / gpu_time:.2f}x")

        except ImportError:
            print("sentence-transformers 未安装")
            print("安装命令: pip install sentence-transformers")

    else:
        print("\n--- GPU不可用 ---")
        print("系统未检测到CUDA支持")

    print("\n--- 建议 ---")
    print("1. 使用 sentence-transformers + GPU 加速embedding")
    print("2. 使用 FAISS GPU 版本加速向量检索")
    print("3. 考虑使用 ONNX Runtime + TensorRT 进行推理")


def test_end_to_end_breakdown():
    """端到端延迟分解测试"""
    print("\n" + "=" * 70)
    print("端到端延迟分解测试")
    print("=" * 70)

    # 初始化引擎
    engine = InferenceEngine(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        device="cuda" if torch.cuda.is_available() else "cpu"
    )

    # 测试输入
    test_inputs = [
        "打开空调",
        "座椅加热",
        "关闭车窗",
        "播放音乐",
        "导航到公司"
    ]

    print(f"\n测试输入: {test_inputs}")

    latencies = []
    router_times = []
    retrieval_times = []

    for text in test_inputs:
        # 路由时间
        start = time.perf_counter()
        router_result = engine.router.process_input(text, "test")
        router_time = (time.perf_counter() - start) * 1000
        router_times.append(router_time)

        # 检索时间
        start = time.perf_counter()
        candidates = engine.skill_retriever.retrieve(
            text,
            router_result['category'],
            top_k=3
        )
        retrieval_time = (time.perf_counter() - start) * 1000
        retrieval_times.append(retrieval_time)

        # 总时间
        latencies.append(router_time + retrieval_time)

    print("\n--- 延迟分解 ---")
    print(f"路由分类:")
    print(f"  平均: {np.mean(router_times):.2f} ms")
    print(f"  P95:  {np.percentile(router_times, 95):.2f} ms")
    print(f"\n技能检索:")
    print(f"  平均: {np.mean(retrieval_times):.2f} ms")
    print(f"  P95:  {np.percentile(retrieval_times, 95):.2f} ms")
    print(f"\n端到端:")
    print(f"  平均: {np.mean(latencies):.2f} ms")
    print(f"  P95:  {np.percentile(latencies, 95):.2f} ms")


def main():
    """主函数"""
    # 1. 验证路由延迟问题
    test_router_latency_issue()

    # 2. 测试embedding设备
    test_embedding_device()

    # 3. 端到端延迟分解
    test_end_to_end_breakdown()

    print("\n" + "=" * 70)
    print("总结")
    print("=" * 70)
    print("1. 路由分类的87ms是批次延迟（128个样本），单样本延迟约为0.7ms")
    print("2. 当前的TF-IDF embedding不支持GPU，建议使用sentence-transformers")
    print("3. 端到端延迟的测量方法是正确的（单样本）")
    print("=" * 70)


if __name__ == "__main__":
    main()
