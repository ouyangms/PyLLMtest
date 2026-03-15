"""
为小样本类别生成训练数据
使用基于规则的模板生成，确保分类正确
"""

import json
import sys
import random
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.router.category_config import CategoryConfig


# 小样本类别的训练模板
CATEGORY_TEMPLATES = {
    "door_control": {
        "templates": [
            "打开{position}车门", "关闭{position}车门", "开{position}门", "关{position}门",
            "打开后备箱", "关闭后备箱", "开后备箱", "关后备箱", "后备箱打开", "后备箱关闭",
            "打开尾门", "关闭尾门", "开尾门", "关尾门",
            "锁车", "解锁", "上锁", "开锁", "车锁上", "车锁开",
            "打开{position}车门锁", "关闭{position}车门锁", "解锁{position}车门", "锁上{position}车门",
            "打开引擎盖", "关闭引擎盖", "开启引擎盖",
            "{position}车门打开", "{position}车门关闭", "{position}门开", "{position}门关",
            "后备箱弹开", "尾门解锁", "全车门锁死", "车门开锁", "锁上所有车门",
            "请打开{position}车门", "帮我关闭{position}车门", "我想打开后备箱",
            "{position}车门别锁", "车门全开", "把{position}车门打开", "把后备箱关上",
            "车门解锁", "车辆解锁", "车辆上锁", "后备箱解锁", "尾门打开",
        ],
        "values": {
            "position": ["左前", "右前", "左后", "右后", "主驾驶", "副驾驶", "后排", "前", "后", "所有"]
        }
    },

    "navigation": {
        "templates": [
            "导航到{destination}",
            "去{destination}",
            "我要去{destination}",
            "设置目的地为{destination}",
            "开始导航到{destination}",
            "规划去{destination}的路线",
            "搜索{destination}",
            "查找{destination}",
            "我想去{destination}",
            "帮我去{destination}",
            "设置导航终点{destination}",
            "路线规划到{destination}",
            "导航去{destination}",
            "{destination}怎么走",
            "我要去{destination}的路线",
        ],
        "values": {
            "destination": ["家", "公司", "医院", "机场", "火车站", "商场", "加油站", "停车场", "最近的服务区", "目的地"]
        }
    },

    "charging_energy": {
        "templates": [
            "开始充电",
            "停止充电",
            "打开充电口",
            "关闭充电口",
            "开启慢充模式",
            "开启快充模式",
            "设置充电时间为{time}",
            "预约充电",
            "取消预约充电",
            "检查充电状态",
            "电量管理",
            "开启充电保护",
            "关闭充电保护",
            "搜索充电桩",
            "查找附近的充电桩",
            "充电到{percent}%",
            "设定充电上限{percent}%",
            "开启预约充电{time}",
            "放电模式开启",
            "关闭放电模式",
        ],
        "values": {
            "time": ["晚上10点", "凌晨2点", "23点", "00:00"],
            "percent": ["80", "90", "100"]
        }
    },

    "driving_assist": {
        "templates": [
            "开启定速巡航",
            "关闭定速巡航",
            "启动ACC自适应巡航",
            "关闭ACC",
            "开启车道保持",
            "关闭车道保持",
            "启动辅助驾驶",
            "关闭辅助驾驶",
            "开启自动泊车",
            "启动自动泊车功能",
            "取消自动泊车",
            "开启跟车模式",
            "关闭跟车模式",
            "设置巡航速度为{speed}",
            "调整跟车距离",
            "增加跟车距离",
            "减少跟车距离",
            "开启LKA车道保持辅助",
            "关闭LKA",
            "启动AEB自动刹车",
            "关闭自动紧急制动",
        ],
        "values": {
            "speed": ["60", "80", "100", "120"]
        }
    }
}


def generate_samples(category, count=100):
    """为指定类别生成样本"""
    if category not in CATEGORY_TEMPLATES:
        print(f"错误: 类别 {category} 没有定义模板")
        return []

    templates = CATEGORY_TEMPLATES[category]["templates"]
    values = CATEGORY_TEMPLATES[category]["values"]

    samples = []
    used_texts = set()

    # 生成指定数量的样本
    attempts = 0
    max_attempts = count * 3  # 最多尝试3倍数量

    while len(samples) < count and attempts < max_attempts:
        attempts += 1

        # 随机选择模板
        template = random.choice(templates)

        # 填充模板
        try:
            text = template.format(**{k: random.choice(v) for k, v in values.items()})
        except (KeyError, ValueError):
            # 模板不需要填充值
            text = template

        # 去重
        if text not in used_texts:
            used_texts.add(text)
            samples.append(text)

    return samples[:count]


def augment_existing_samples(category, existing_data, target_count=100):
    """基于现有样本进行变体生成"""
    # 提取现有文本
    existing_texts = [item["text"] for item in existing_data if item.get("category_name") == category or item.get("category") == category]

    if not existing_texts:
        return generate_samples(category, target_count)

    # 变体生成规则
    variants = []

    for text in existing_texts:
        # 原始文本
        variants.append(text)

        # 添加语气词
        variants.append(f"请{text}")
        variants.append(f"帮我{text}")
        variants.append(f"我想{text}")

        # 简化表达
        for keyword in ["打开", "关闭", "开启", "启动"]:
            if keyword in text:
                variants.append(text.replace(keyword, "开"))
                variants.append(text.replace(keyword, "关"))
                break

    # 去重并限制数量
    unique_variants = list(set(variants))
    random.shuffle(unique_variants)

    return unique_variants[:target_count]


def main():
    print("=" * 70)
    print("为小样本类别生成训练数据")
    print("=" * 70)

    # 加载清洗后的训练数据
    data_dir = Path("data/processed")

    with open(data_dir / "train_data_clean.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    # 统计各类别数量
    from collections import Counter
    category_counts = Counter([item.get("category_name", item.get("category", "")) for item in train_data])

    print("\n当前各类别样本数:")
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat:20s}: {count:3d}")

    # 定义小样本类别（目标：每个至少100个样本）
    small_categories = {
        "door_control": {"current": category_counts.get("door_control", 0), "target": 150},
        "navigation": {"current": category_counts.get("navigation", 0), "target": 150},
        "charging_energy": {"current": category_counts.get("charging_energy", 0), "target": 150},
        "driving_assist": {"current": category_counts.get("driving_assist", 0), "target": 150},
    }

    print("\n需要增强的类别:")
    for cat, info in small_categories.items():
        needed = info["target"] - info["current"]
        print(f"  {cat:20s}: {info['current']:3d} -> {info['target']:3d} (需生成 {needed} 个)")

    # 生成样本
    all_generated = []

    for category, info in small_categories.items():
        needed = info["target"] - info["current"]

        if needed <= 0:
            print(f"\n{category}: 已有足够样本，跳过")
            continue

        print(f"\n为 {category} 生成 {needed} 个样本...")

        # 生成样本
        samples = generate_samples(category, needed)

        # 获取类别 ID
        category_id = CategoryConfig.get_category_id(category)

        # 转换为数据格式
        for sample in samples:
            all_generated.append({
                "text": sample,
                "category_id": category_id,
                "category_name": category,
                "source": "generated_small_category"
            })

        print(f"  实际生成: {len(samples)} 个")

    # 保存生成的样本
    output_path = data_dir / "small_category_samples.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_generated, f, ensure_ascii=False, indent=2)

    print(f"\n已保存: {output_path}")
    print(f"总计生成: {len(all_generated)} 个样本")

    # 合并到清洗后的训练集
    print("\n合并到训练集...")
    merged_data = train_data + all_generated

    output_merged = data_dir / "train_data_clean_aug.json"
    with open(output_merged, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"已保存: {output_merged}")
    print(f"合并后总样本数: {len(merged_data)}")

    # 统计合并后的分布
    merged_counts = Counter([item.get("category_name", item.get("category", "")) for item in merged_data])
    print("\n合并后类别分布:")
    for cat, count in sorted(merged_counts.items()):
        print(f"  {cat:20s}: {count:4d}")


if __name__ == "__main__":
    main()
