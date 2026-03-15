"""
混合检索器准确率测试
对比原始、增强、混合三种检索器
"""

import sys
import time
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.skill_retriever import SkillRetriever
from src.hybrid.skill_retriever_enhanced import SkillRetrieverEnhanced
from src.hybrid.hybrid_retriever import HybridRetriever


def evaluate_retriever(retriever, name: str, test_cases: List[tuple]) -> Dict:
    """评估检索器性能"""
    print(f"\n评估 {name}...")
    print("-" * 70)

    total = len(test_cases)
    correct = 0
    latencies = []

    for query, expected_category, expected_keyword in test_cases:
        start = time.perf_counter()
        candidates = retriever.retrieve(query, expected_category, top_k=3)
        latency = (time.perf_counter() - start) * 1000
        latencies.append(latency)

        # 检查是否正确
        is_correct = False
        if candidates and candidates[0]['similarity'] > 0:
            for candidate in candidates[:3]:
                name_lower = candidate['name'].lower()
                desc_lower = candidate.get('description', '').lower()
                if expected_keyword.lower() in name_lower or expected_keyword.lower() in desc_lower:
                    is_correct = True
                    break

        if is_correct:
            correct += 1

    accuracy = correct / total if total > 0 else 0

    print(f"  总样本: {total}")
    print(f"  正确数: {correct}")
    print(f"  准确率: {accuracy*100:.2f}%")
    print(f"  平均延迟: {sum(latencies)/len(latencies):.2f} ms")
    print(f"  P95延迟: {sorted(latencies)[int(len(latencies)*0.95)]:.2f} ms")

    return {
        'name': name,
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'latency': sum(latencies) / len(latencies),
        'p95_latency': sorted(latencies)[int(len(latencies)*0.95)]
    }


def main():
    """主函数"""
    print("=" * 70)
    print("混合检索器准确率对比测试")
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
        ("制冷", "climate_control", "Cool"),
        ("制热", "climate_control", "Heat"),

        # 座椅相关
        ("座椅加热", "seat_control", "SeatHeat"),
        ("座椅通风", "seat_control", "Ventilation"),
        ("按摩座椅", "seat_control", "Massage"),
        ("加热座椅", "seat_control", "Heat"),
        ("座椅制冷", "seat_control", "Cool"),

        # 车窗相关
        ("打开车窗", "window_control", "Window"),
        ("关闭车窗", "window_control", "Window"),
        ("开窗", "window_control", "Window"),
        ("天窗", "window_control", "Sunroof"),

        # 灯光相关
        ("打开大灯", "light_control", "Light"),
        ("近光灯", "light_control", "Beam"),
        ("远光灯", "light_control", "Beam"),
        ("阅读灯", "light_control", "Reading"),
        ("氛围灯", "light_control", "Ambient"),

        # 音乐相关
        ("播放音乐", "music_media", "Music"),
        ("调节音量", "music_media", "Volume"),
        ("调大音量", "music_media", "Volume"),
        ("上一首", "music_media", "Previous"),
        ("下一首", "music_media", "Next"),
        ("暂停音乐", "music_media", "Pause"),

        # 导航相关
        ("导航到公司", "navigation", "Navigation"),
        ("开始导航", "navigation", "Navigation"),
        ("回家", "navigation", "Home"),
        ("去天安门", "navigation", "Destination"),

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

    # 初始化检索器
    print("\n初始化检索器...")

    print("\n1. 原始检索器 (关键词匹配)")
    retriever_original = SkillRetriever(skills_dir, use_vector=False)

    print("\n2. 增强检索器 (同义词+jieba)")
    retriever_enhanced = SkillRetrieverEnhanced(skills_dir)

    print("\n3. 混合检索器 (关键词+向量)")
    retriever_hybrid = HybridRetriever(
        skills_dir,
        use_embedding=True,
        device="cuda"
    )

    # 评估
    results = []

    results.append(evaluate_retriever(
        retriever_original,
        "原始检索器",
        test_cases
    ))

    results.append(evaluate_retriever(
        retriever_enhanced,
        "增强检索器",
        test_cases
    ))

    results.append(evaluate_retriever(
        retriever_hybrid,
        "混合检索器",
        test_cases
    ))

    # 对比总结
    print("\n" + "=" * 70)
    print("对比总结")
    print("=" * 70)

    print(f"\n{'检索器':<15} {'准确率':<12} {'P95延迟':<12} {'改进':<10}")
    print("-" * 70)

    baseline = results[0]
    print(f"{baseline['name']:<15} "
          f"{baseline['accuracy']*100:>10.2f}% "
          f"{baseline['p95_latency']:>10.2f} ms "
          f"{'基准':<10}")

    for result in results[1:]:
        acc_improvement = (result['accuracy'] - baseline['accuracy']) * 100
        latency_change = ((result['p95_latency'] - baseline['p95_latency']) / baseline['p95_latency']) * 100

        acc_str = f"+{acc_improvement:.1f}%" if acc_improvement > 0 else f"{acc_improvement:.1f}%"
        lat_str = f"+{latency_change:.0f}%" if latency_change > 0 else f"{latency_change:.0f}%"

        print(f"{result['name']:<15} "
              f"{result['accuracy']*100:>10.2f}% "
              f"{result['p95_latency']:>10.2f} ms "
              f"{acc_str:<10}")

    # 最佳方案
    print("\n" + "=" * 70)
    print("最佳方案分析")
    print("=" * 70)

    # 找出准确率最高且延迟满足要求的
    candidates = [r for r in results if r['p95_latency'] < 10]  # 延迟<10ms

    if candidates:
        best = max(candidates, key=lambda x: x['accuracy'])
        print(f"\n推荐方案: {best['name']}")
        print(f"  准确率: {best['accuracy']*100:.2f}%")
        print(f"  P95延迟: {best['p95_latency']:.2f} ms")

        # 与目标对比
        acc_target = 80
        acc_diff = best['accuracy'] * 100 - acc_target

        if best['accuracy'] * 100 >= acc_target:
            print(f"\n[OK] 已达到准确率目标 (>{acc_target}%)")
        else:
            print(f"\n[!] 距离准确率目标还差 {abs(acc_diff):.2f} 个百分点")
    else:
        print("\n[!] 没有检索器满足延迟要求 (<10ms)")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
