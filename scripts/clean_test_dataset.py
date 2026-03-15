"""
清洗测试集，去除无效样本
保留包含明确关键词、可以准确分类的样本
"""

import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, 'E:/ai/py/whisperModel')

from src.router.category_config import CategoryConfig


# 每个类别的关键词
CATEGORY_KEYWORDS = {
    "climate_control": ["空调", "温度", "风量", "风向", "除雾", "香氛", "制冷", "制热", "送风", "空气净化", "除霜", "暖风", "冷风", "恒温", "自动空调"],
    "seat_control": ["座椅", "加热", "通风", "按摩", "腰托", "腿托", "头枕", "座椅位置", "座椅调节", "座椅记忆", "座椅靠背"],
    "window_control": ["车窗", "窗户", "天窗", "遮阳帘", "升降", "透气", "开窗", "关窗", "开天窗", "关天窗", "车窗玻璃"],
    "light_control": ["灯光", "阅读灯", "氛围灯", "大灯", "转向灯", "日行灯", "亮度", "远光", "近光", "示宽灯", "车内灯", "照明"],
    "mirror_control": ["后视镜", "镜子", "折叠", "加热", "防眩目", "倒车镜", "侧视镜"],
    "door_control": ["车门", "后备箱", "尾门", "锁车", "解锁", "儿童锁", "引擎盖", "车门锁"],
    "music_media": ["音乐", "音量", "播放", "暂停", "切歌", "上一首", "下一首", "蓝牙", "电台", "均衡器", "歌曲", "听歌", "播放器"],
    "navigation": ["导航", "路线", "目的地", "地图", "避堵", "拥堵", "位置", "搜索", "规划", "导航到", "设为目的地"],
    "phone_call": ["电话", "拨打", "接听", "挂断", "蓝牙电话", "联系人", "打电话", "来电"],
    "vehicle_info": ["电量", "续航", "胎压", "油量", "里程", "车辆状态", "车况", "剩余", "油表", "电量剩余", "续航里程"],
    "system_settings": ["设置", "显示", "主题", "语言", "连接", "偏好", "配置", "系统设置", "屏幕", "显示设置"],
    "driving_assist": ["巡航", "车道", "辅助", "刹车", "泊车", "自动", "跟车", "限速", "ACC", "LKA", "辅助驾驶", "定速巡航"],
    "charging_energy": ["充电", "充电桩", "电量管理", "预约", "放电", "慢充", "快充", "充电口", "充电枪"]
}


# 无效模式（极度模糊的表达）
INVALID_PATTERNS = [
    "调一调", "弄一下", "关一点", "开一点", "调一点",
    "恢复默认", "重置", "取消", "再来一次", "再弄一次",
    "随便", "不管", "都可以",
    # 纯操作词，无对象
    "打开", "关闭", "开启", "启动", "停止",
    "增加", "减少", "变大", "变小",
    "弄大点", "弄小点", "调高点", "调低点",
]


def is_valid_sample(text, category):
    """
    判断样本是否有效
    1. 不包含无效模式
    2. 长度适中（2-30字）
    3. 包含该类别的关键词
    """
    text = text.strip()

    # 长度检查
    if len(text) <= 1 or len(text) > 30:
        return False, "长度超出范围"

    # 检查无效模式
    for pattern in INVALID_PATTERNS:
        if text == pattern:
            return False, f"匹配无效模式: {pattern}"

    # 检查是否包含该类别的关键词
    keywords = CATEGORY_KEYWORDS.get(category, [])
    has_keyword = any(kw in text for kw in keywords)

    if not has_keyword:
        return False, "无类别关键词"

    return True, "有效"


def clean_dataset(data, output_reason=False):
    """清洗数据集"""
    cleaned = []
    invalid_samples = []

    for item in data:
        text = item["text"]
        category = item.get("category_name", item.get("category", ""))

        is_valid, reason = is_valid_sample(text, category)

        if is_valid:
            cleaned.append(item)
        else:
            invalid_samples.append({
                "text": text,
                "category": category,
                "reason": reason
            })

    if output_reason:
        return cleaned, invalid_samples
    return cleaned


def main():
    print("=" * 70)
    print("清洗测试集 - 去除无效样本")
    print("=" * 70)

    # 加载数据
    data_dir = Path("data/processed")

    datasets = ["train_data.json", "val_data.json", "test_data.json"]

    for dataset_name in datasets:
        print(f"\n处理: {dataset_name}")
        print("-" * 70)

        with open(data_dir / dataset_name, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"原始样本数: {len(data)}")

        # 清洗数据
        cleaned, invalid = clean_dataset(data, output_reason=True)

        print(f"有效样本数: {len(cleaned)} ({len(cleaned)/len(data)*100:.1f}%)")
        print(f"无效样本数: {len(invalid)} ({len(invalid)/len(data)*100:.1f}%)")

        # 统计无效原因
        reason_count = Counter([item["reason"] for item in invalid])
        print("\n无效原因统计:")
        for reason, count in reason_count.most_common():
            print(f"  {reason}: {count}")

        # 保存清洗后的数据
        output_name = dataset_name.replace(".json", "_clean.json")
        output_path = data_dir / output_name

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)

        print(f"\n已保存: {output_path}")

        # 显示无效样本示例
        print("\n无效样本示例（前10个）:")
        for item in invalid[:10]:
            print(f"  \"{item['text']}\" ({item['category']}) - {item['reason']}")

    print("\n" + "=" * 70)
    print("清洗完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
