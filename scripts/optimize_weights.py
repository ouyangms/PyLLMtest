"""
权重优化 - 寻找最佳的关键词/向量权重组合
目标：准确率 >80%, P95延迟 <10ms
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.hybrid_retriever import HybridRetriever


def evaluate_with_weights(
    retriever: HybridRetriever,
    test_cases: List[tuple],
    keyword_weight: float,
    vector_weight: float
) -> Dict:
    """评估特定权重组合的性能"""
    total = len(test_cases)
    correct = 0
    latencies = []

    for query, expected_category, expected_keyword in test_cases:
        start = time.perf_counter()
        candidates = retriever.retrieve(
            query,
            expected_category,
            top_k=3,
            keyword_weight=keyword_weight,
            vector_weight=vector_weight
        )
        latency = (time.perf_counter() - start) * 1000
        latencies.append(latency)

        # 检查是否正确
        is_correct = False
        if candidates and candidates[0]['similarity'] > 0:
            for candidate in candidates[:3]:
                name_lower = candidate['name'].lower()
                if expected_keyword.lower() in name_lower:
                    is_correct = True
                    break

        if is_correct:
            correct += 1

    accuracy = correct / total if total > 0 else 0
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]

    return {
        'accuracy': accuracy,
        'p95_latency': p95_latency,
        'avg_latency': sum(latencies) / len(latencies),
        'correct': correct,
        'total': total
    }


def main():
    """主函数"""
    print("=" * 70)
    print("混合检索器权重优化")
    print("=" * 70)

    skills_dir = Path("E:/ai/py/whisperModel/vc/skills")

    # 测试用例
    test_cases = [
        # 空调相关
        ("打开空调", "climate_control", "AirCondition"),
        ("温度24度", "climate_control", "Temperature"),
        ("设置温度", "climate_control", "Temperature"),
        ("空调风量", "climate_control", "Wind"),
        ("除霜", "climate_control", "Defrost"),

        # 座椅相关
        ("座椅加热", "seat_control", "SeatHeat"),
        ("座椅通风", "seat_control", "Ventilation"),
        ("按摩座椅", "seat_control", "Massage"),

        # 车窗相关
        ("打开车窗", "window_control", "Window"),
        ("关闭车窗", "window_control", "Window"),
        ("天窗", "window_control", "Sunroof"),

        # 灯光相关
        ("打开大灯", "light_control", "Light"),
        ("近光灯", "light_control", "Beam"),
        ("远光灯", "light_control", "Beam"),
        ("阅读灯", "light_control", "Reading"),

        # 音乐相关
        ("播放音乐", "music_media", "Music"),
        ("调节音量", "music_media", "Volume"),
        ("调大音量", "music_media", "Volume"),
        ("上一首", "music_media", "Previous"),
        ("下一首", "music_media", "Next"),

        # 导航相关
        ("导航到公司", "navigation", "Navigation"),
        ("开始导航", "navigation", "Navigation"),
        ("回家", "navigation", "Home"),

        # 电话相关
        ("打电话", "phone_call", "Phone"),
        ("拨打", "phone_call", "Dial"),
        ("接听电话", "phone_call", "Answer"),

        # 后视镜
        ("后视镜加热", "mirror_control", "Mirror"),
        ("折叠后视镜", "mirror_control", "Fold"),

        # 车门/后备箱
        ("打开后备箱", "door_control", "Trunk"),
        ("解锁车门", "door_control", "Lock"),
    ]

    print(f"\n测试用例数: {len(test_cases)}")

    # 初始化混合检索器
    print("\n初始化混合检索器...")
    retriever = HybridRetriever(
        skills_dir,
        use_embedding=True,
        device="cuda"
    )

    # 测试不同的权重组合
    print("\n" + "=" * 70)
    print("测试不同权重组合")
    print("=" * 70)

    # 权重组合
    weight_combinations = [
        (0.2, 0.8),  # 向量为主
        (0.3, 0.7),
        (0.4, 0.6),  # 默认
        (0.5, 0.5),
        (0.6, 0.4),
        (0.7, 0.3),
        (0.8, 0.2),  # 关键词为主
    ]

    results = []

    for kw_weight, vec_weight in weight_combinations:
        print(f"\n测试权重: 关键词={kw_weight}, 向量={vec_weight}")

        result = evaluate_with_weights(
            retriever,
            test_cases,
            kw_weight,
            vec_weight
        )

        result['keyword_weight'] = kw_weight
        result['vector_weight'] = vec_weight
        results.append(result)

        print(f"  准确率: {result['accuracy']*100:.2f}%")
        print(f"  P95延迟: {result['p95_latency']:.2f} ms")

        # 检查是否满足目标
        if result['accuracy'] >= 0.80 and result['p95_latency'] < 10:
            print(f"  [OK] 满足目标！")
        elif result['accuracy'] >= 0.80:
            print(f"  [!] 准确率达标，但延迟超标")
        elif result['p95_latency'] < 10:
            gap = (0.80 - result['accuracy']) * 100
            print(f"  [!] 延迟达标，准确率还差 {gap:.2f} 个百分点")

    # 找出最佳组合
    print("\n" + "=" * 70)
    print("最佳权重组合分析")
    print("=" * 70)

    # 按准确率排序
    results_by_acc = sorted(results, key=lambda x: x['accuracy'], reverse=True)

    print(f"\n按准确率排序:")
    print(f"{'关键词权重':<12} {'向量权重':<12} {'准确率':<12} {'P95延迟':<12} {'状态':<10}")
    print("-" * 70)

    for r in results_by_acc[:5]:  # 显示前5名
        status = ""
        if r['accuracy'] >= 0.80 and r['p95_latency'] < 10:
            status = "[OK] 完美"
        elif r['accuracy'] >= 0.80:
            status = "[!] 延迟高"
        elif r['p95_latency'] < 10:
            gap = (0.80 - r['accuracy']) * 100
            status = f"[!] 差{gap:.1f}%"

        print(f"{r['keyword_weight']:<12.2f} {r['vector_weight']:<12.2f} "
              f"{r['accuracy']*100:>10.2f}% {r['p95_latency']:>10.2f} ms {status:<10}")

    # 找出满足条件的最佳组合
    qualified = [r for r in results if r['accuracy'] >= 0.80 and r['p95_latency'] < 10]

    if qualified:
        best = qualified[0]
        print(f"\n[OK] 找到满足目标的权重组合:")
        print(f"  关键词权重: {best['keyword_weight']}")
        print(f"  向量权重: {best['vector_weight']}")
        print(f"  准确率: {best['accuracy']*100:.2f}%")
        print(f"  P95延迟: {best['p95_latency']:.2f} ms")
    else:
        # 找出最接近目标的组合
        print(f"\n[!] 没有完全满足目标的组合")

        # 按综合评分排序
        for r in results:
            # 评分：准确率优先，延迟作为次要因素
            score = r['accuracy'] * 100 - (r['p95_latency'] / 10)
            r['score'] = score

        results_by_score = sorted(results, key=lambda x: x['score'], reverse=True)
        best = results_by_score[0]

        acc_gap = (0.80 - best['accuracy']) * 100
        print(f"\n推荐最佳组合:")
        print(f"  关键词权重: {best['keyword_weight']}")
        print(f"  向量权重: {best['vector_weight']}")
        print(f"  准确率: {best['accuracy']*100:.2f}% (还差 {acc_gap:.2f} 个百分点)")
        print(f"  P95延迟: {best['p95_latency']:.2f} ms")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
