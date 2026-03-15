"""
推理测试脚本
"""
import json
import pickle
import numpy as np
from pathlib import Path
from src.router.classifier import RouterClassifier

print('=' * 60)
print('车控技能推理引擎 - 测试')
print('=' * 60)

# 测试查询
test_queries = [
    '打开空调',
    '座椅加热',
    '车里太热了',
    '我想透透气',
    '查询胎压',
]

# 1. 测试路由分类器
print('\n[1/2] 测试路由分类器')
print('-' * 60)

try:
    classifier = RouterClassifier()
    print('路由模型加载成功!')

    for query in test_queries:
        category, probs = classifier.predict(query, return_probs=True)
        print(f'\n查询: {query}')
        print(f'预测: {category}')

        # 显示 Top-3
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        print('Top-3:')
        for cat, prob in sorted_probs[:3]:
            print(f'  {cat}: {prob:.4f}')

except Exception as e:
    print(f'路由分类器错误: {e}')
    import traceback
    traceback.print_exc()

# 2. 测试向量检索
print('\n[2/2] 测试向量检索')
print('-' * 60)

try:
    index_dir = Path('data/indexes')

    for query in test_queries[:3]:
        print(f'\n查询: {query}')

        # 预测分类
        category = classifier.predict(query)

        # 加载对应分类的向量
        mapping_path = index_dir / f'{category}_mapping.pkl'
        if mapping_path.exists():
            with open(mapping_path, 'rb') as f:
                mapping = pickle.load(f)

            print(f'分类: {category} (候选技能: {len(mapping["items"])})')

            # 显示前3个候选
            for i, item in enumerate(mapping['items'][:3], 1):
                print(f'  {i}. {item.get("skill_name", "N/A")}')
                print(f'     示例: {item.get("text", "N/A")}')
        else:
            print(f'  未找到分类索引: {category}')

except Exception as e:
    print(f'向量检索错误: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '=' * 60)
print('测试完成!')
print('=' * 60)
