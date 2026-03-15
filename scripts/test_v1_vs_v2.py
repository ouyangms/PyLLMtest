"""
V1 vs V2 完整性能对比测试
对比原始检索器和混合检索器的端到端性能
"""

import sys
import time
import numpy as np
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.inference_engine import InferenceEngine
from src.hybrid.inference_engine_v2 import InferenceEngineV2


def test_engine(engine, name: str, test_data: List[Dict]) -> Dict:
    """测试引擎性能"""
    print(f"\n测试 {name}...")
    print("-" * 70)

    latencies = []
    category_stats = {}
    path_stats = {}

    for item in test_data:
        start = time.perf_counter()
        result = engine.process(item["text"], user_id="test")
        latency = (time.perf_counter() - start) * 1000

        latencies.append(latency)

        # 统计类别准确率
        true_category = item.get("category_name", item.get("category", ""))
        if result.category == true_category:
            category_stats[true_category] = category_stats.get(true_category, 0) + 1

        # 统计处理路径
        path = result.processing_path.value
        path_stats[path] = path_stats.get(path, 0) + 1

    # 计算指标
    latencies = np.array(latencies)

    total_correct = sum(category_stats.values())
    total_samples = len(test_data)
    accuracy = total_correct / total_samples if total_samples > 0 else 0

    return {
        'name': name,
        'accuracy': accuracy,
        'avg_latency': float(np.mean(latencies)),
        'p50_latency': float(np.percentile(latencies, 50)),
        'p95_latency': float(np.percentile(latencies, 95)),
        'p99_latency': float(np.percentile(latencies, 99)),
        'correct': total_correct,
        'total': total_samples,
        'path_stats': path_stats
    }


def main():
    """主函数"""
    print("=" * 70)
    print("V1 vs V2 完整性能对比测试")
    print("=" * 70)

    # 加载测试数据
    test_data_path = "data/processed/test_data_clean.json"
    print(f"\n加载测试数据: {test_data_path}")

    import json
    with open(test_data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    print(f"测试样本数: {len(test_data)}")

    # 限制测试数量（加快测试速度）
    test_samples = test_data[:100]

    # 初始化V1引擎
    print("\n" + "=" * 70)
    print("初始化 V1 引擎 (原始检索器)")
    print("=" * 70)

    engine_v1 = InferenceEngine(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        device="cuda"
    )

    # 初始化V2引擎
    print("\n" + "=" * 70)
    print("初始化 V2 引擎 (混合检索器)")
    print("=" * 70)

    engine_v2 = InferenceEngineV2(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        use_embedding=True,
        retriever_device="cuda",
        device="cuda"
    )

    # 测试两个引擎
    results = []

    results.append(test_engine(
        engine_v1,
        "V1 (原始检索器)",
        test_samples
    ))

    results.append(test_engine(
        engine_v2,
        "V2 (混合检索器)",
        test_samples
    ))

    # 对比总结
    print("\n" + "=" * 70)
    print("性能对比总结")
    print("=" * 70)

    print(f"\n{'引擎版本':<20} {'准确率':<12} {'平均延迟':<12} {'P95延迟':<12} {'改进':<10}")
    print("-" * 70)

    baseline = results[0]
    print(f"{baseline['name']:<20} "
          f"{baseline['accuracy']*100:>10.2f}% "
          f"{baseline['avg_latency']:>10.2f} ms "
          f"{baseline['p95_latency']:>10.2f} ms "
          f"{'基准':<10}")

    for result in results[1:]:
        acc_improvement = (result['accuracy'] - baseline['accuracy']) * 100
        latency_change = ((result['avg_latency'] - baseline['avg_latency']) / baseline['avg_latency']) * 100

        acc_str = f"+{acc_improvement:.1f}%" if acc_improvement > 0 else f"{acc_improvement:.1f}%"
        lat_str = f"+{latency_change:.0f}%" if latency_change > 0 else f"{latency_change:.0f}%"

        print(f"{result['name']:<20} "
              f"{result['accuracy']*100:>10.2f}% "
              f"{result['avg_latency']:>10.2f} ms "
              f"{result['p95_latency']:>10.2f} ms "
              f"{acc_str:<10}")

    # 处理路径对比
    print("\n" + "=" * 70)
    print("处理路径分布对比")
    print("=" * 70)

    for result in results:
        print(f"\n{result['name']}:")
        for path, count in sorted(result['path_stats'].items(), key=lambda x: x[1], reverse=True):
            pct = count / sum(result['path_stats'].values()) * 100
            print(f"  {path:<20} {count:4d} ({pct:>5.1f}%)")

    # 详细分析
    print("\n" + "=" * 70)
    print("详细分析")
    print("=" * 70)

    v1_result = results[0]
    v2_result = results[1]

    print(f"\n准确率:")
    acc_diff = (v2_result['accuracy'] - v1_result['accuracy']) * 100
    print(f"  V1: {v1_result['accuracy']*100:.2f}%")
    print(f"  V2: {v2_result['accuracy']*100:.2f}%")
    print(f"  改进: {acc_diff:+.2f} 个百分点")

    print(f"\n延迟:")
    print(f"  V1 平均: {v1_result['avg_latency']:.2f} ms")
    print(f"  V2 平均: {v2_result['avg_latency']:.2f} ms")
    lat_diff = v2_result['avg_latency'] - v1_result['avg_latency']
    print(f"  差异: {lat_diff:+.2f} ms")

    print(f"\n  V1 P95: {v1_result['p95_latency']:.2f} ms")
    print(f"  V2 P95: {v2_result['p95_latency']:.2f} ms")

    # 结论
    print("\n" + "=" * 70)
    print("结论")
    print("=" * 70)

    if acc_diff > 0:
        print(f"\n[OK] V2 准确率提升了 {acc_diff:.2f} 个百分点")
    else:
        print(f"\n[!] V2 准确率下降了 {abs(acc_diff):.2f} 个百分点")

    if abs(lat_diff) < 5:
        print(f"[OK] 延迟基本持平 ({lat_diff:+.2f} ms)")
    elif lat_diff > 0:
        print(f"[!] V2 延迟增加了 {lat_diff:.2f} ms")
    else:
        print(f"[OK] V2 延迟减少了 {abs(lat_diff):.2f} ms")

    # 检查是否满足目标
    print("\n" + "=" * 70)
    print("目标达成情况")
    print("=" * 70)

    target_accuracy = 0.80
    target_latency_p95 = 10.0

    for result in results:
        acc_met = result['accuracy'] >= target_accuracy
        lat_met = result['p95_latency'] <= target_latency_p95

        print(f"\n{result['name']}:")
        print(f"  准确率: {result['accuracy']*100:.2f}% {'[OK]' if acc_met else '[!]'} "
              f"(目标: ≥{target_accuracy*100:.0f}%)")
        print(f"  P95延迟: {result['p95_latency']:.2f} ms {'[OK]' if lat_met else '[!]'} "
              f"(目标: <{target_latency_p95:.0f} ms)")

        if acc_met and lat_met:
            print(f"  状态: [OK] 完全满足目标")
        elif acc_met:
            print(f"  状态: [!] 准确率达标，延迟超标")
        elif lat_met:
            gap = (target_accuracy - result['accuracy']) * 100
            print(f"  状态: [!] 延迟达标，准确率还差 {gap:.2f} 个百分点")
        else:
            print(f"  状态: [!] 两项均未达标")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
