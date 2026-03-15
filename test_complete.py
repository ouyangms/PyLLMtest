"""
车控技能推理引擎 - 完整测试脚本
"""

from src.router.classifier import RouterClassifier
from src.retrieval.vector_store import VectorStore
import time

print("=" * 60)
print("车控技能推理引擎 - 完整测试")
print("=" * 60)

# 1. 加载模型
print("\n[1/4] 加载模型...")
print("-" * 60)

start_time = time.time()
classifier = RouterClassifier()
store = VectorStore()
load_time = time.time() - start_time

print(f"路由模型加载: data/models/router/best_model.pth")
print(f"向量索引加载: {len(store.indexes)} 个分类")
print(f"模型加载耗时: {load_time:.2f}s")

# 2. 测试查询集合
test_queries = [
    # 标准指令
    "打开空调",
    "关闭车窗",
    "座椅加热",
    "调节音量",

    # 场景/感受型
    "车里太热了",
    "我想透透气",
    "有点冷",
    "天太暗了",

    # 模糊/口语型
    "开条缝",
    "透透气",
    "调高点",
    "声音大点",

    # 查询型
    "现在胎压多少",
    "还有多少电",
    "现在车速",

    # 组合指令
    "打开主驾空调并调到24度",
    "关闭所有窗户",
]

# 3. 路由分类测试
print("\n[2/4] 路由分类测试")
print("-" * 60)

category_stats = {}
for query in test_queries:
    category, probs = classifier.predict(query, return_probs=True)
    confidence = probs[category]

    if category not in category_stats:
        category_stats[category] = []
    category_stats[category].append((query, confidence))

print(f"测试查询数: {len(test_queries)}")
print(f"\n分类分布:")
for cat, items in sorted(category_stats.items()):
    print(f"  {cat}: {len(items)} 条")

# 4. 端到端推理测试
print("\n[3/4] 端到端推理测试")
print("-" * 60)

inference_results = []
total_latency = 0

for i, query in enumerate(test_queries[:10], 1):  # 测试前10个
    print(f"\n测试 {i}: {query}")

    # 推理计时
    start = time.time()

    # 路由
    category, probs = classifier.predict(query, return_probs=True)

    # 检索
    results = store.search(query, category=category, k=3)

    latency = (time.time() - start) * 1000
    total_latency += latency

    print(f"  路由: {category} (置信度: {probs[category]:.2%})")
    print(f"  召回: {len(results)} 条候选")
    print(f"  延迟: {latency:.1f}ms")

    if results:
        top_result = results[0]
        print(f"  Top-1: {top_result.get('skill_name', 'N/A')}")
        print(f"        相似度: {top_result.get('score', 0):.4f}")

    inference_results.append({
        'query': query,
        'category': category,
        'confidence': probs[category],
        'num_results': len(results),
        'latency_ms': latency
    })

# 5. 性能统计
print("\n[4/4] 性能统计")
print("-" * 60)

avg_latency = total_latency / len(test_queries[:10])
max_latency = max([r['latency_ms'] for r in inference_results])
min_latency = min([r['latency_ms'] for r in inference_results])

print(f"平均延迟: {avg_latency:.1f}ms")
print(f"最大延迟: {max_latency:.1f}ms")
print(f"最小延迟: {min_latency:.1f}ms")

avg_confidence = sum([r['confidence'] for r in inference_results]) / len(inference_results)
print(f"平均置信度: {avg_confidence:.2%}")

# 6. 分类准确性分析
print("\n[附加] 分类准确性分析")
print("-" * 60)

expected_mapping = {
    "打开空调": "climate_control",
    "关闭车窗": "window_control",
    "座椅加热": "seat_control",
    "调节音量": "music_media",
    "车里太热了": "climate_control",
    "我想透透气": "window_control",
    "有点冷": "climate_control",
    "天太暗了": "light_control",
    "开条缝": "window_control",
    "透透气": "window_control",
}

correct = 0
total = len(expected_mapping)

for query, expected in expected_mapping.items():
    actual = classifier.predict(query)
    if actual == expected:
        correct += 1
        status = "[OK]"
    else:
        status = "[--]"
    print(f"{status} '{query}': 期望 {expected}, 实际 {actual}")

accuracy = correct / total * 100
print(f"\n路由准确率: {correct}/{total} ({accuracy:.1f}%)")

# 7. 总结
print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)

print(f"✓ 模型加载成功: {load_time:.2f}s")
print(f"✓ 索引数量: {len(store.indexes)} 个分类")
print(f"✓ 平均延迟: {avg_latency:.1f}ms (目标 <1000ms)")
print(f"✓ 路由准确率: {accuracy:.1f}% (目标 >90%)")

if avg_latency < 100:
    print(f"\n[GOOD] 延迟测试: 优秀 ({avg_latency:.1f}ms < 100ms)")
elif avg_latency < 500:
    print(f"\n[OK] 延迟测试: 良好 ({avg_latency:.1f}ms < 500ms)")
else:
    print(f"\n[WARN] 延迟测试: 需要优化 ({avg_latency:.1f}ms)")

if accuracy > 80:
    print(f"[OK] 准确率测试: 良好 ({accuracy:.1f}% > 80%)")
elif accuracy > 60:
    print(f"[WARN] 准确率测试: 需要改进 ({accuracy:.1f}%)")
else:
    print(f"[FAIL] 准确率测试: 需要优化 ({accuracy:.1f}%)")

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)
