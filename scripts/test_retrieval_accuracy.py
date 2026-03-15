"""
检索器准确率对比测试
对比原始检索器 vs 增强检索器
"""

import sys
import time
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.skill_retriever import SkillRetriever
from src.hybrid.skill_retriever_enhanced import SkillRetrieverEnhanced


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
            # 检查候选技能名称是否包含预期关键词
            for candidate in candidates[:3]:
                if expected_keyword in candidate['name'] or expected_keyword in candidate.get('description', ''):
                    is_correct = True
                    break

        if is_correct:
            correct += 1

    accuracy = correct / total if total > 0 else 0

    print(f"  总样本: {total}")
    print(f"  正确数: {correct}")
    print(f"  准确率: {accuracy*100:.2f}%")
    print(f"  平均延迟: {sum(latencies)/len(latencies):.2f} ms")

    return {
        'name': name,
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'latency': sum(latencies) / len(latencies)
    }


def main():
    """主函数"""
    print("=" * 70)
    print("检索器准确率对比测试")
    print("=" * 70)

    skills_dir = Path("E:/ai/py/whisperModel/vc/skills")

    # 测试用例（更全面）
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
        ("加热座椅", "seat_control", "Heat"),

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

    # 初始化检索器
    print("\n初始化检索器...")

    print("\n1. 原始检索器 (关键词匹配)")
    retriever_original = SkillRetriever(skills_dir, use_vector=False)

    print("\n2. 增强检索器 (同义词+jieba)")
    retriever_enhanced = SkillRetrieverEnhanced(skills_dir)

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

    # 对比总结
    print("\n" + "=" * 70)
    print("对比总结")
    print("=" * 70)

    print(f"\n{'检索器':<15} {'准确率':<12} {'正确/总数':<15} {'平均延迟':<12} {'改进':<10}")
    print("-" * 70)

    original_result = results[0]
    enhanced_result = results[1]

    print(f"{original_result['name']:<15} "
          f"{original_result['accuracy']*100:>10.2f}% "
          f"{original_result['correct']:>4}/{original_result['total']:<4} "
          f"{original_result['latency']:>10.2f} ms "
          f"{'基准':<10}")

    # 计算改进
    acc_improvement = (enhanced_result['accuracy'] - original_result['accuracy']) * 100
    latency_change = ((enhanced_result['latency'] - original_result['latency']) / original_result['latency']) * 100

    improvement_str = f"+{acc_improvement:.1f}%" if acc_improvement > 0 else f"{acc_improvement:.1f}%"

    print(f"{enhanced_result['name']:<15} "
          f"{enhanced_result['accuracy']*100:>10.2f}% "
          f"{enhanced_result['correct']:>4}/{enhanced_result['total']:<4} "
          f"{enhanced_result['latency']:>10.2f} ms "
          f"{improvement_str:<10}")

    print("\n" + "=" * 70)
    print("详细分析")
    print("=" * 70)

    print(f"\n准确率改进: {acc_improvement:+.2f}个百分点")
    print(f"延迟变化: {latency_change:+.2f}%")

    if acc_improvement > 0:
        print(f"\n[OK] 增强检索器准确率提升了 {acc_improvement:.2f} 个百分点")
    else:
        print(f"\n[!] 增强检索器准确率没有提升")

    if abs(latency_change) < 10:
        print(f"[OK] 延迟变化不大 ({latency_change:+.2f}%)")
    elif latency_change > 0:
        print(f"[!] 延迟增加了 {latency_change:.2f}%")
    else:
        print(f"[OK] 延迟减少了 ({latency_change:.2f}%)")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
