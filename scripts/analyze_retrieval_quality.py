"""
深入分析：V1 vs V2 检索质量对比
专注于检索阶段的质量分析
"""

import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.hybrid.inference_engine import InferenceEngine
from src.hybrid.inference_engine_v2 import InferenceEngineV2


def analyze_retrieval_quality(engine, name: str, test_cases: List[Dict]) -> Dict:
    """分析检索质量"""
    print(f"\n分析 {name} 的检索质量...")
    print("-" * 70)

    stats = {
        'total': len(test_cases),
        'retrieval_success': 0,
        'llm_fallback': 0,
        'high_confidence': 0,  # 置信度 > 0.7
        'medium_confidence': 0,  # 0.5 < 置信度 <= 0.7
        'low_confidence': 0,     # 置信度 <= 0.5
        'avg_confidence': 0,
        'retrieval_candidates': []
    }

    confidences = []

    for item in test_cases:
        result = engine.process(item["text"], "test")

        # 统计处理路径
        if result.processing_path.value == "retrieval":
            stats['retrieval_success'] += 1
            confidences.append(result.confidence)

            if result.confidence > 0.7:
                stats['high_confidence'] += 1
            elif result.confidence > 0.5:
                stats['medium_confidence'] += 1
            else:
                stats['low_confidence'] += 1

            # 记录候选技能信息
            if 'candidates' in result.metadata:
                stats['retrieval_candidates'].append({
                    'query': item["text"],
                    'category': item.get("category_name", ""),
                    'skill_id': result.skill_id,
                    'skill_name': result.skill_name,
                    'confidence': result.confidence,
                    'keyword_score': result.metadata.get('keyword_score', 0),
                    'vector_score': result.metadata.get('vector_score', 0)
                })

        elif result.processing_path.value == "llm_fallback":
            stats['llm_fallback'] += 1

    # 计算平均置信度
    if confidences:
        stats['avg_confidence'] = sum(confidences) / len(confidences)

    # 打印结果
    print(f"  总样本: {stats['total']}")
    print(f"  检索成功: {stats['retrieval_success']} ({stats['retrieval_success']/stats['total']*100:.1f}%)")
    print(f"  LLM回退: {stats['llm_fallback']} ({stats['llm_fallback']/stats['total']*100:.1f}%)")
    print(f"\n  置信度分布:")
    print(f"    高 (>0.7): {stats['high_confidence']} ({stats['high_confidence']/stats['retrieval_success']*100:.1f}%)")
    print(f"    中 (0.5-0.7): {stats['medium_confidence']} ({stats['medium_confidence']/stats['retrieval_success']*100:.1f}%)")
    print(f"    低 (<=0.5): {stats['low_confidence']} ({stats['low_confidence']/stats['retrieval_success']*100:.1f}%)")
    print(f"  平均置信度: {stats['avg_confidence']:.3f}")

    return stats


def compare_retrieval_details(v1_stats: Dict, v2_stats: Dict):
    """对比检索细节"""
    print("\n" + "=" * 70)
    print("检索质量对比")
    print("=" * 70)

    print(f"\n{'指标':<25} {'V1':<15} {'V2':<15} {'改进':<15}")
    print("-" * 70)

    # 检索成功率
    v1_rate = v1_stats['retrieval_success'] / v1_stats['total'] * 100
    v2_rate = v2_stats['retrieval_success'] / v1_stats['total'] * 100
    improvement = v2_rate - v1_rate
    imp_str = f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
    print(f"{'检索成功率':<25} {v1_rate:>13.1f}% {v2_rate:>13.1f}% {imp_str:>15}")

    # LLM回退率
    v1_fallback = v1_stats['llm_fallback'] / v1_stats['total'] * 100
    v2_fallback = v2_stats['llm_fallback'] / v2_stats['total'] * 100
    improvement = v1_fallback - v2_fallback
    imp_str = f"-{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
    print(f"{'LLM回退率':<25} {v1_fallback:>13.1f}% {v2_fallback:>13.1f}% {imp_str:>15}")

    # 高置信度比例
    if v1_stats['retrieval_success'] > 0 and v2_stats['retrieval_success'] > 0:
        v1_high = v1_stats['high_confidence'] / v1_stats['retrieval_success'] * 100
        v2_high = v2_stats['high_confidence'] / v2_stats['retrieval_success'] * 100
        improvement = v2_high - v1_high
        imp_str = f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
        print(f"{'高置信度比例':<25} {v1_high:>13.1f}% {v2_high:>13.1f}% {imp_str:>15}")

    # 平均置信度
    conf_diff = v2_stats['avg_confidence'] - v1_stats['avg_confidence']
    conf_str = f"+{conf_diff:.3f}" if conf_diff > 0 else f"{conf_diff:.3f}"
    print(f"{'平均置信度':<25} {v1_stats['avg_confidence']:>13.3f} {v2_stats['avg_confidence']:>13.3f} {conf_str:>15}")

    # 显示V2的详细检索案例
    if v2_stats['retrieval_candidates']:
        print("\n" + "=" * 70)
        print("V2 检索案例展示（前10个）")
        print("=" * 70)

        for i, case in enumerate(v2_stats['retrieval_candidates'][:10], 1):
            print(f"\n{i}. 查询: \"{case['query']}\"")
            print(f"   类别: {case['category']}")
            print(f"   技能: {case['skill_name']}")
            print(f"   置信度: {case['confidence']:.3f}")
            print(f"   分数分解: 关键词={case['keyword_score']:.2f}, 向量={case['vector_score']:.2f}")


def main():
    """主函数"""
    print("=" * 70)
    print("V1 vs V2 检索质量深入分析")
    print("=" * 70)

    # 测试用例（专注于需要检索的情况）
    test_cases = [
        # 空调相关
        {"text": "打开空调", "category_name": "climate_control"},
        {"text": "温度24度", "category_name": "climate_control"},
        {"text": "设置温度", "category_name": "climate_control"},
        {"text": "空调风量", "category_name": "climate_control"},
        {"text": "除霜", "category_name": "climate_control"},

        # 座椅相关
        {"text": "座椅加热", "category_name": "seat_control"},
        {"text": "座椅通风", "category_name": "seat_control"},
        {"text": "按摩座椅", "category_name": "seat_control"},

        # 车窗相关
        {"text": "打开车窗", "category_name": "window_control"},
        {"text": "关闭车窗", "category_name": "window_control"},
        {"text": "天窗", "category_name": "window_control"},

        # 灯光相关
        {"text": "打开大灯", "category_name": "light_control"},
        {"text": "阅读灯", "category_name": "light_control"},
        {"text": "氛围灯", "category_name": "light_control"},

        # 音乐相关
        {"text": "播放音乐", "category_name": "music_media"},
        {"text": "调大音量", "category_name": "music_media"},
        {"text": "上一首", "category_name": "music_media"},
        {"text": "下一首", "category_name": "music_media"},

        # 导航相关
        {"text": "导航到公司", "category_name": "navigation"},
        {"text": "开始导航", "category_name": "navigation"},
        {"text": "回家", "category_name": "navigation"},

        # 电话相关
        {"text": "打电话", "category_name": "phone_call"},
        {"text": "接听电话", "category_name": "phone_call"},

        # 后视镜
        {"text": "后视镜加热", "category_name": "mirror_control"},
        {"text": "折叠后视镜", "category_name": "mirror_control"},

        # 车门
        {"text": "打开后备箱", "category_name": "door_control"},
        {"text": "解锁车门", "category_name": "door_control"},
    ]

    print(f"\n测试用例数: {len(test_cases)}")

    # 初始化引擎
    print("\n初始化引擎...")

    engine_v1 = InferenceEngine(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        device="cuda"
    )

    engine_v2 = InferenceEngineV2(
        router_model_path="data/models/router_clean_final/best_model.pth",
        skills_dir=None,
        use_llm=False,
        use_embedding=True,
        retriever_device="cuda",
        device="cuda"
    )

    # 分析检索质量
    v1_stats = analyze_retrieval_quality(engine_v1, "V1", test_cases)
    v2_stats = analyze_retrieval_quality(engine_v2, "V2", test_cases)

    # 对比
    compare_retrieval_details(v1_stats, v2_stats)

    # 结论
    print("\n" + "=" * 70)
    print("结论")
    print("=" * 70)

    retrieval_improvement = (v2_stats['retrieval_success'] - v1_stats['retrieval_success'])
    reduction_fallback = (v1_stats['llm_fallback'] - v2_stats['llm_fallback'])

    print(f"\nV2 的主要改进:")
    print(f"  1. 检索成功率增加: {retrieval_improvement} 个样本")
    print(f"  2. LLM回退减少: {reduction_fallback} 个样本")
    print(f"  3. 平均置信度提升: {v2_stats['avg_confidence'] - v1_stats['avg_confidence']:.3f}")

    if v2_stats['avg_confidence'] > v1_stats['avg_confidence']:
        print(f"\n[OK] V2 的检索质量显著提升")
    else:
        print(f"\n[!] V2 的检索质量提升有限")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
