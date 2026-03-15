"""
比较 TextCNN 和 BERT 模型性能
"""

import time
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router.classifier import RouterClassifier
from src.router.bert_classifier import BERTRouter


def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_section(text):
    print("\n" + "-" * 60)
    print(text)
    print("-" * 60)


def benchmark_model(model, model_name, test_queries, num_iterations=100):
    """测试模型性能"""
    latencies = []

    # 预热
    for query in test_queries[:3]:
        try:
            model.predict(query)
        except:
            pass

    # 测试延迟
    for _ in range(num_iterations):
        query = test_queries[_ % len(test_queries)]

        start = time.time()
        try:
            model.predict(query)
            latency = (time.time() - start) * 1000
            latencies.append(latency)
        except Exception as e:
            print(f"  [错误] {query}: {e}")
            latencies.append(0)

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


def test_accuracy(model, model_name, test_data):
    """测试准确率"""
    correct = 0
    total = len(test_data)

    for item in test_data:
        query = item["text"]
        expected_id = item["category_id"]

        try:
            predicted = model.predict(query)

            # 获取预测的类别 ID
            from src.router.category_config import CategoryConfig
            predicted_id = CategoryConfig.get_category_id(predicted)

            if predicted_id == expected_id:
                correct += 1
        except Exception as e:
            print(f"  [错误] {query}: {e}")

    accuracy = correct / total if total > 0 else 0
    return accuracy


def load_test_data(data_file="data/processed/test_data.json"):
    """加载测试数据"""
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="比较 TextCNN 和 BERT 性能")
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="设备 (cuda/cpu)"
    )
    parser.add_argument(
        "--bert-model",
        type=str,
        default="bert-base-chinese",
        help="BERT 模型名称"
    )
    parser.add_argument(
        "--skip-benchmark",
        action="store_true",
        help="跳过性能基准测试"
    )

    args = parser.parse_args()

    print_header("TextCNN vs BERT 性能比较")

    # 测试查询
    test_queries = [
        "打开空调",
        "关闭车窗",
        "座椅加热",
        "调节音量",
        "车里太热了",
        "我想透透气",
        "有点冷",
        "天太暗了",
        "开条缝",
        "透透气",
    ]

    # 加载测试数据
    print_section("加载测试数据")
    test_data = load_test_data()
    print(f"测试样本数: {len(test_data)}")

    results = {}

    # ========== TextCNN ==========
    print_section("TextCNN 模型")

    try:
        print("\n加载 TextCNN 模型...")
        textcnn_model = RouterClassifier(device=args.device)
        textcnn_info = {
            "name": "TextCNN",
            "parameters": sum(p.numel() for p in textcnn_model.model.parameters()),
            "device": args.device
        }
        print(f"参数量: {textcnn_info['parameters']:,}")

        # 准确率测试
        print("\n测试准确率...")
        textcnn_accuracy = test_accuracy(textcnn_model, "TextCNN", test_data)
        print(f"准确率: {textcnn_accuracy*100:.2f}%")

        # 延迟测试
        if not args.skip_benchmark:
            print("\n测试延迟 (100 次迭代)...")
            textcnn_latency = benchmark_model(textcnn_model, "TextCNN", test_queries, num_iterations=100)
            print(f"平均延迟: {textcnn_latency['mean']:.2f}ms")
            print(f"P50: {textcnn_latency['p50']:.2f}ms")
            print(f"P95: {textcnn_latency['p95']:.2f}ms")
            print(f"P99: {textcnn_latency['p99']:.2f}ms")
        else:
            textcnn_latency = {"mean": 0}

        results["textcnn"] = {
            "accuracy": textcnn_accuracy,
            "latency": textcnn_latency,
            "info": textcnn_info
        }

    except Exception as e:
        print(f"\n[错误] TextCNN 加载失败: {e}")
        results["textcnn"] = None

    # ========== BERT ==========
    print_section("BERT 模型")

    try:
        print(f"\n加载 BERT 模型: {args.bert_model}")
        bert_model = BERTRouter(model_name=args.bert_model, device=args.device)
        bert_info = bert_model.get_model_info()
        print(f"参数量: {bert_info['total_parameters']:,}")

        # 准确率测试
        print("\n测试准确率...")
        bert_accuracy = test_accuracy(bert_model, "BERT", test_data)
        print(f"准确率: {bert_accuracy*100:.2f}%")

        # 延迟测试
        if not args.skip_benchmark:
            print("\n测试延迟 (100 次迭代)...")
            bert_latency = benchmark_model(bert_model, "BERT", test_queries, num_iterations=100)
            print(f"平均延迟: {bert_latency['mean']:.2f}ms")
            print(f"P50: {bert_latency['p50']:.2f}ms")
            print(f"P95: {bert_latency['p95']:.2f}ms")
            print(f"P99: {bert_latency['p99']:.2f}ms")
        else:
            bert_latency = {"mean": 0}

        results["bert"] = {
            "accuracy": bert_accuracy,
            "latency": bert_latency,
            "info": bert_info
        }

    except Exception as e:
        print(f"\n[错误] BERT 加载失败: {e}")
        import traceback
        traceback.print_exc()
        results["bert"] = None

    # ========== 总结 ==========
    print_header("性能比较总结")

    if results.get("textcnn") and results.get("bert"):
        tcnn = results["textcnn"]
        bert = results["bert"]

        print(f"\n{'指标':<20} {'TextCNN':<20} {'BERT':<20} {'差异'}")
        print("-" * 80)

        # 准确率
        acc_diff = (bert["accuracy"] - tcnn["accuracy"]) * 100
        print(f"{'准确率':<20} {tcnn['accuracy']*100:>6.2f}%{' ':13} {bert['accuracy']*100:>6.2f}%{' ':13} {acc_diff:+.2f}%")

        # 参数量
        param_ratio = bert["info"]["total_parameters"] / tcnn["info"]["parameters"]
        print(f"{'参数量':<20} {tcnn['info']['parameters']:>12,.0f}{' ':8} {bert['info']['total_parameters']:>12,.0f}{' ':8} {param_ratio:.1f}x")

        # 平均延迟
        if not args.skip_benchmark:
            lat_diff = bert["latency"]["mean"] - tcnn["latency"]["mean"]
            lat_ratio = bert["latency"]["mean"] / tcnn["latency"]["mean"] if tcnn["latency"]["mean"] > 0 else 0
            print(f"{'平均延迟':<20} {tcnn['latency']['mean']:>8.2f}ms{' ':12} {bert['latency']['mean']:>8.2f}ms{' ':12} {lat_ratio:.1f}x")

            print(f"\n延迟分布:")
            print(f"{'  P50':<18} {tcnn['latency']['p50']:>8.2f}ms{' ':12} {bert['latency']['p50']:>8.2f}ms")
            print(f"{'  P95':<18} {tcnn['latency']['p95']:>8.2f}ms{' ':12} {bert['latency']['p95']:>8.2f}ms")
            print(f"{'  P99':<18} {tcnn['latency']['p99']:>8.2f}ms{' ':12} {bert['latency']['p99']:>8.2f}ms")

        # 结论
        print("\n" + "=" * 60)
        print("结论")
        print("=" * 60)

        if bert["accuracy"] > tcnn["accuracy"]:
            print(f"BERT 准确率更高 (+{(bert['accuracy'] - tcnn['accuracy'])*100:.2f}%)")
        else:
            print(f"TextCNN 准确率更高 (+{(tcnn['accuracy'] - bert['accuracy'])*100:.2f}%)")

        if not args.skip_benchmark:
            if tcnn["latency"]["mean"] < bert["latency"]["mean"]:
                print(f"TextCNN 延迟更低 ({bert['latency']['mean']/tcnn['latency']['mean']:.1f}x)")
            else:
                print(f"BERT 延迟更低 ({tcnn['latency']['mean']/bert['latency']['mean']:.1f}x)")

        # 推荐建议
        print("\n推荐:")
        if tcnn["latency"]["mean"] < 50 and tcnn["accuracy"] > 0.7:
            print("  [推荐] TextCNN - 延迟低且准确率满足需求")
        elif bert["accuracy"] > tcnn["accuracy"] + 0.05:
            print("  [推荐] BERT - 准确率显著更高")
        elif tcnn["latency"]["mean"] < 100:
            print("  [推荐] TextCNN - 满足实时性要求")
        else:
            print("  [分析] 根据具体需求选择")


if __name__ == "__main__":
    main()
