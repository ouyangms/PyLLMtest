"""
分析千问生成样本的质量
检查分类错误、重复率、长度分布等
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.router.category_config import CategoryConfig


# 定义每个类别的关键词（用于检测分类错误）
CATEGORY_KEYWORDS = {
    "climate_control": ["空调", "温度", "风量", "风向", "除雾", "香氛", "制冷", "制热", "送风", "空气净化", "PM2.5"],
    "seat_control": ["座椅", "加热", "通风", "按摩", "腰托", "腿托", "头枕", "座椅位置", "座椅调节", "座椅记忆"],
    "window_control": ["车窗", "窗户", "天窗", "遮阳帘", "升降", "透气", "开窗", "关窗", "开天窗", "关天窗"],
    "light_control": ["灯光", "阅读灯", "氛围灯", "大灯", "转向灯", "日行灯", "亮度", "远光", "近光", "示宽灯"],
    "mirror_control": ["后视镜", "镜子", "折叠", "加热", "防眩目", "倒车镜"],
    "door_control": ["车门", "后备箱", "尾门", "锁车", "解锁", "儿童锁", "引擎盖"],
    "music_media": ["音乐", "音量", "播放", "暂停", "切歌", "上一首", "下一首", "蓝牙", "电台", "均衡器", "歌"],
    "navigation": ["导航", "路线", "目的地", "地图", "避堵", "拥堵", "位置", "搜索", "规划"],
    "phone_call": ["打电话", "拨打电话", "接听", "挂断", "蓝牙电话", "联系人", "电话"],
    "vehicle_info": ["电量", "续航", "胎压", "油量", "里程", "车辆状态", "车况", "剩余"],
    "system_settings": ["设置", "显示", "主题", "语言", "连接", "偏好", "配置", "系统"],
    "driving_assist": ["巡航", "车道", "辅助", "刹车", "泊车", "自动", "跟车", "限速", "ACC", "LKA"],
    "charging_energy": ["充电", "充电桩", "电量管理", "预约", "放电", "慢充", "快充"]
}


def detect_misclassification(text, assigned_category):
    """检测文本是否被错误分类"""
    # 检查是否包含其他类别的关键词
    for category, keywords in CATEGORY_KEYWORDS.items():
        if category == assigned_category:
            continue

        for keyword in keywords:
            if keyword in text:
                # 找到关键词，返回可能的正确分类
                return category, keyword

    return None, None


def main():
    print("=" * 80)
    print("千问生成样本质量分析")
    print("=" * 80)

    # 加载数据
    data_dir = Path("data/processed")

    with open(data_dir / "augmented_samples.json", "r", encoding="utf-8") as f:
        qwen_data = json.load(f)

    with open(data_dir / "train_data.json", "r", encoding="utf-8") as f:
        original_data = json.load(f)

    print(f"\n千问样本数: {len(qwen_data)}")
    print(f"原始样本数: {len(original_data)}")

    # ========== 1. 基本统计 ==========
    print("\n" + "=" * 80)
    print("1. 基本统计")
    print("=" * 80)

    # 类别分布
    qwen_dist = Counter([item["category"] for item in qwen_data])
    print("\n类别分布:")
    for cat, count in sorted(qwen_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:4d}")

    # ========== 2. 重复率分析 ==========
    print("\n" + "=" * 80)
    print("2. 重复率分析")
    print("=" * 80)

    qwen_texts = [item["text"] for item in qwen_data]
    original_texts = [item["text"] for item in original_data]

    # 千问内部重复
    qwen_unique = set(qwen_texts)
    qwen_dup_rate = (len(qwen_texts) - len(qwen_unique)) / len(qwen_texts) * 100
    print(f"\n千问内部重复率: {qwen_dup_rate:.1f}% ({len(qwen_texts)} -> {len(qwen_unique)})")

    # 与原始数据重复
    overlap = set(qwen_texts) & set(original_texts)
    overlap_rate = len(overlap) / len(qwen_texts) * 100
    print(f"与原始数据重叠: {overlap_rate:.1f}% ({len(overlap)} 个样本)")

    # ========== 3. 分类错误检测 ==========
    print("\n" + "=" * 80)
    print("3. 分类错误检测")
    print("=" * 80)

    misclassified = []
    error_by_category = defaultdict(int)

    for item in qwen_data:
        text = item["text"]
        category = item["category"]

        # 检测分类错误
        correct_category, keyword = detect_misclassification(text, category)

        if correct_category:
            misclassified.append({
                "text": text,
                "assigned": category,
                "should_be": correct_category,
                "keyword": keyword
            })
            error_by_category[category] += 1

    error_rate = len(misclassified) / len(qwen_data) * 100

    print(f"\n检测到 {len(misclassified)} 个可能分类错误的样本 ({error_rate:.1f}%)")

    # 按类别统计错误
    print("\n各类别错误数:")
    for cat, count in sorted(error_by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:3d}")

    # 显示具体错误示例
    print("\n分类错误示例 (前20个):")
    print("-" * 80)

    # 按错误类型分组
    errors_by_type = defaultdict(list)
    for err in misclassified:
        key = f"{err['assigned']} -> {err['should_be']}"
        errors_by_type[key].append(err)

    for error_type, examples in sorted(errors_by_type.items(), key=lambda x: len(x[1]), reverse=True)[:20]:
        print(f"\n{error_type}:")
        for ex in examples[:3]:
            print(f"  - \"{ex['text']}\" (关键词: {ex['keyword']})")

    # ========== 4. 长度分布 ==========
    print("\n" + "=" * 80)
    print("4. 长度分布")
    print("=" * 80)

    length_dist = {
        "极短 (1-2字)": 0,
        "短 (3-5字)": 0,
        "中 (6-10字)": 0,
        "长 (11-20字)": 0,
        "超长 (>20字)": 0
    }

    for item in qwen_data:
        length = len(item["text"])
        if length <= 2:
            length_dist["极短 (1-2字)"] += 1
        elif length <= 5:
            length_dist["短 (3-5字)"] += 1
        elif length <= 10:
            length_dist["中 (6-10字)"] += 1
        elif length <= 20:
            length_dist["长 (11-20字)"] += 1
        else:
            length_dist["超长 (>20字)"] += 1

    for label, count in length_dist.items():
        pct = count / len(qwen_data) * 100
        print(f"  {label:15s}: {count:4d} ({pct:5.1f}%)")

    # ========== 5. 特殊问题样本 ==========
    print("\n" + "=" * 80)
    print("5. 特殊问题样本")
    print("=" * 80)

    # 极短样本
    very_short = [item for item in qwen_data if len(item["text"]) <= 2]
    print(f"\n极短样本 (<=2字): {len(very_short)} 个")
    if very_short:
        print("示例:", [item["text"] for item in very_short[:10]])

    # 过长样本
    very_long = [item for item in qwen_data if len(item["text"]) > 25]
    print(f"\n过长样本 (>25字): {len(very_long)} 个")
    if very_long:
        print("示例:")
        for item in very_long[:5]:
            print(f"  - \"{item['text']}\" ({item['category']})")

    # ========== 6. 建议修复措施 ==========
    print("\n" + "=" * 80)
    print("6. 建议修复措施")
    print("=" * 80)

    print(f"""
基于以上分析，建议采取以下修复措施：

1. 修复分类错误 ({len(misclassified)} 个样本)
   - 使用关键词规则重新分类
   - 或者使用小规模人工校验

2. 过滤问题样本
   - 删除极短样本 (<=2字): {len(very_short)} 个
   - 删除过长样本 (>25字): {len(very_long)} 个

3. 去重
   - 删除与原始数据重叠的 {len(overlap)} 个样本
   - 删除千问内部重复的样本

4. 重新训练
   - 使用清洗后的数据重新训练模型
   - 预期准确率提升: +5-10%

5. 改进千问提示词
   - 在提示词中明确包含各分类的关键词定义
   - 要求千问根据关键词进行分类
   - 增加分类验证步骤
    """)

    # ========== 7. 生成清洗后的数据 ==========
    print("\n" + "=" * 80)
    print("7. 生成清洗后的数据")
    print("=" * 80)

    # 清洗数据
    cleaned_data = []

    for item in qwen_data:
        text = item["text"]
        category = item["category"]

        # 跳过极短和过长
        if len(text) <= 2 or len(text) > 25:
            continue

        # 跳过与原始数据重叠的
        if text in original_texts:
            continue

        # 修复分类错误
        correct_category, keyword = detect_misclassification(text, category)
        if correct_category:
            # 使用正确的分类
            category = correct_category

        # 获取正确的 category_id
        category_id = CategoryConfig.get_category_id(category)

        cleaned_data.append({
            "text": text,
            "category_id": category_id,
            "category_name": category,
            "source": "qwen_cleaned"
        })

    # 去重
    unique_texts = set()
    final_data = []
    for item in cleaned_data:
        if item["text"] not in unique_texts:
            unique_texts.add(item["text"])
            final_data.append(item)

    print(f"\n清洗后样本数: {len(final_data)}")
    print(f"清洗过程: {len(qwen_data)} -> {len(cleaned_data)} -> {len(final_data)}")

    # 保存清洗后的数据
    output_path = data_dir / "qwen_samples_cleaned.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"已保存: {output_path}")

    # 清洗后类别分布
    print("\n清洗后类别分布:")
    cleaned_dist = Counter([item["category_name"] for item in final_data])
    for cat, count in sorted(cleaned_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:4d}")


if __name__ == "__main__":
    main()
