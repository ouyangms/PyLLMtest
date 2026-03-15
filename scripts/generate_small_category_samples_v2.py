"""
为小样本类别生成训练数据 - 扩充版
使用更多模板生成足够数量的样本
"""

import json
import sys
import random
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.router.category_config import CategoryConfig


# 小样本类别的训练模板（扩充版）
CATEGORY_TEMPLATES = {
    "door_control": {
        "templates": [
            "打开{position}车门", "关闭{position}车门", "开{position}门", "关{position}门",
            "打开后备箱", "关闭后备箱", "开后备箱", "关后备箱", "后备箱打开", "后备箱关闭",
            "打开尾门", "关闭尾门", "开尾门", "关尾门", "尾门打开", "尾门关闭",
            "锁车", "解锁", "上锁", "开锁", "车锁上", "车锁开", "车辆上锁", "车辆解锁",
            "打开{position}车门锁", "关闭{position}车门锁", "解锁{position}车门", "锁上{position}车门",
            "打开引擎盖", "关闭引擎盖", "开启引擎盖", "引擎盖开启",
            "{position}车门打开", "{position}车门关闭", "{position}门开", "{position}门关",
            "后备箱弹开", "尾门解锁", "全车门锁死", "车门开锁", "锁上所有车门",
            "请打开{position}车门", "帮我关闭{position}车门", "我想打开后备箱",
            "{position}车门别锁", "车门全开", "把{position}车门打开", "把后备箱关上",
            "车门解锁", "车辆解锁", "车辆上锁", "后备箱解锁", "尾门打开",
            "解锁后备箱", "锁上后备箱", "尾门上锁", "尾门开锁",
            "{position}门解锁", "{position}门上锁", "车门全锁", "车门全开",
            "请帮我锁车", "帮我解锁", "后备箱开一下", "车门打开一下",
        ],
        "values": {
            "position": ["左前", "右前", "左后", "右后", "主驾驶", "副驾驶", "后排", "前", "后", "所有", "全部", "左边", "右边", "两侧"]
        }
    },

    "navigation": {
        "templates": [
            "导航到{destination}", "去{destination}", "我要去{destination}", "设置目的地为{destination}",
            "开始导航到{destination}", "规划去{destination}的路线", "搜索{destination}", "查找{destination}",
            "我想去{destination}", "帮我去{destination}", "设置导航终点{destination}", "路线规划到{destination}",
            "导航去{destination}", "{destination}怎么走", "我要去{destination}的路线", "带我去{destination}",
            "我要到{destination}", "开车去{destination}", "帮我导航到{destination}",
            "设定路线到{destination}", "{destination}导航", "去{destination}的路",
            "规划去{destination}", "寻找去{destination}的路", "我要开车到{destination}",
            "导航设置{destination}", "目的地{destination}", "把{destination}设为目的地",
            "搜索{destination}位置", "查找{destination}位置", "{destination}在哪里",
            "我要去{destination}", "带路去{destination}", "路线{destination}",
            "帮我查{destination}", "找{destination}", "我要找{destination}",
            "导航到附近的{destination}", "搜索最近的{destination}", "查找附近的{destination}",
            "去附近的{destination}", "我要去最近的{destination}",
            "设置途经点{destination}", "添加途经点{destination}",
            "避开{destination}", "路线避开{destination}", "导航避开{condition}",
        ],
        "values": {
            "destination": ["家", "公司", "医院", "机场", "火车站", "商场", "加油站", "停车场", "服务区", "目的地", "酒店", "餐厅", "银行", "超市", "学校", "充电站"],
            "condition": ["拥堵", "高速费", "收费站"]
        }
    },

    "charging_energy": {
        "templates": [
            "开始充电", "停止充电", "打开充电", "关闭充电", "启动充电", "停止充电",
            "打开充电口", "关闭充电口", "充电口开启", "充电口关闭",
            "开启慢充模式", "开启快充模式", "切换慢充", "切换快充", "慢充模式", "快充模式",
            "设置充电时间为{time}", "充电时间设定{time}", "{time}开始充电",
            "预约充电", "取消预约充电", "设置预约充电", "充电预约",
            "检查充电状态", "电量管理", "充电状态", "充电管理",
            "开启充电保护", "关闭充电保护", "充电保护开", "充电保护关",
            "搜索充电桩", "查找充电桩", "找充电桩", "附近充电桩", "搜索附近的充电桩", "查找附近的充电桩",
            "充电到{percent}%", "设定充电上限{percent}%", "充电限制{percent}%", "充到{percent}%",
            "开启预约充电{time}", "放电模式开启", "关闭放电模式", "开启放电", "关闭放电",
            "开始慢充", "开始快充", "停止慢充", "停止快充", "充电完成提示",
            "充电口盖打开", "充电口盖关闭", "连接充电枪", "断开充电枪",
            "电池预热", "电池保温", "充电功率最大", "充电功率最小",
            "定时充电", "取消定时充电", "充电定时设置{time}", "充电预约设置{time}",
            "最大充电{percent}", "充电限值{percent}", "设置充电限制{percent}",
            "开启备用充电", "关闭备用充电", "充电口解锁", "充电口锁定",
        ],
        "values": {
            "time": ["晚上10点", "凌晨2点", "23点", "00:00", "22点", "今晚10点", "今晚11点", "凌晨1点"],
            "percent": ["80", "90", "100", "85", "95", "70", "75"]
        }
    },

    "driving_assist": {
        "templates": [
            "开启定速巡航", "关闭定速巡航", "启动定速巡航", "停止定速巡航",
            "定速巡航开", "定速巡航关", "打开巡航", "关闭巡航",
            "启动ACC自适应巡航", "关闭ACC", "开启ACC", "ACC开启", "ACC关闭", "自适应巡航开启",
            "开启车道保持", "关闭车道保持", "车道保持开", "车道保持关", "车道辅助开启",
            "启动辅助驾驶", "关闭辅助驾驶", "打开辅助驾驶", "辅助驾驶模式", "智能辅助开启",
            "开启自动泊车", "启动自动泊车", "开始泊车", "自动泊车", "泊车辅助开启",
            "取消自动泊车", "停止泊车", "退出泊车", "结束泊车",
            "开启跟车模式", "关闭跟车模式", "跟车模式开", "跟车模式关", "跟车功能开启",
            "设置巡航速度为{speed}", "设定速度{speed}", "速度设为{speed}", "限速{speed}",
            "调整跟车距离", "增加跟车距离", "减少跟车距离", "跟车距离调大", "跟车距离调小",
            "开启LKA车道保持辅助", "关闭LKA", "LKA开启", "LKA关闭",
            "启动AEB自动刹车", "关闭自动紧急制动", "AEB开启", "AEB关闭", "自动刹车开启", "紧急制动开启",
            "限速控制开启", "限速控制关闭", "交通标志识别开启", "交通标志识别关闭",
            "智能驾驶开启", "智能驾驶关闭", "自动驾驶模式", "辅助模式开启", "高级辅助驾驶开启",
            "开启盲区监测", "关闭盲区监测", "盲区检测开", "盲区监测开启",
            "开启并线辅助", "关闭并线辅助", "并线辅助开启",
            "设置跟车距离{level}", "跟车距离设为{level}", "调整跟车距离为{level}",
            "速度限制解除", "超速提醒开启", "超速提醒关闭",
            "疲劳提醒开启", "疲劳提醒关闭", "驾驶员监测开启",
        ],
        "values": {
            "speed": ["60", "80", "100", "120", "40", "50", "70", "90", "110"],
            "level": ["近", "中", "远", "1", "2", "3"]
        }
    }
}


def generate_samples(category, count=150):
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
    max_attempts = count * 5

    while len(samples) < count and attempts < max_attempts:
        attempts += 1

        # 随机选择模板
        template = random.choice(templates)

        # 填充模板
        try:
            text = template.format(**{k: random.choice(v) for k, v in values.items()})
        except (KeyError, ValueError):
            text = template

        # 去重
        if text not in used_texts:
            used_texts.add(text)
            samples.append(text)

    return samples[:count]


def main():
    print("=" * 70)
    print("为小样本类别生成训练数据（扩充版）")
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

    # 定义小样本类别
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

        samples = generate_samples(category, needed)

        category_id = CategoryConfig.get_category_id(category)

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
