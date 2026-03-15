"""
技能数据增强 - 为每个技能生成更多示例查询
目标：通过增加训练数据提升准确率到80%+
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

sys.path.insert(0, 'E:/ai/py/whisperModel')


# 示例查询模板
EXAMPLE_TEMPLATES = {
    "climate_control": [
        "打开空调", "关闭空调", "开空调", "关空调",
        "温度调高", "温度调低", "设置温度", "调一下温度",
        "制冷", "制热", "除霜", "除雾",
        "风量大点", "风量小点", "空调风量", "风速",
        "太热了", "太冷了", "有点热", "有点冷",
    ],
    "seat_control": [
        "座椅加热", "座椅通风", "座椅制冷",
        "打开座椅加热", "关闭座椅加热",
        "座椅按摩", "按摩座椅", "开启按摩", "关闭按摩",
        "加热座椅", "座椅温度", "座椅制冷",
        "主驾座椅", "副驾座椅", "后排座椅",
    ],
    "window_control": [
        "打开车窗", "关闭车窗", "开窗", "关窗",
        "降下窗户", "升起窗户", "全部降下", "全部升起",
        "打开天窗", "关闭天窗", "天窗打开", "天窗关闭",
        "左前窗", "右前窗", "左后窗", "右后窗",
    ],
    "light_control": [
        "打开大灯", "关闭大灯", "开大灯", "关大灯",
        "近光灯", "远光灯", "远光", "近光",
        "阅读灯", "氛围灯", "车内灯",
        "打开灯光", "关闭灯光", "灯光调节",
        "日间行车灯", "雾灯", "转向灯",
    ],
    "music_media": [
        "播放音乐", "暂停音乐", "停止音乐",
        "上一首", "下一首", "切歌", "循环播放",
        "调大音量", "调小音量", "音量大点", "音量小点",
        "调节音量", "设置音量", "音量调节",
        "播放", "暂停", "继续播放",
    ],
    "navigation": [
        "导航到公司", "导航回家", "开始导航", "停止导航",
        "去公司", "回家", "去天安门", "到机场",
        "设置目的地", "导航设置", "路线规划",
        "取消导航", "退出导航", "关闭导航",
    ],
    "phone_call": [
        "打电话", "拨打", "接听电话", "挂断电话",
        "拨打电话", "呼叫", "接通", "挂起",
        "拒接电话", "静音", "免提",
    ],
    "mirror_control": [
        "后视镜加热", "折叠后视镜", "展开后视镜",
        "左后视镜", "右后视镜", "外后视镜",
        "电动折叠", "自动折叠", "后视镜调节",
    ],
    "door_control": [
        "打开后备箱", "关闭后备箱", "解锁车门", "锁上车门",
        "开后备箱", "关后备箱", "开锁", "上锁",
        "全部解锁", "全部上锁", "车门解锁", "车门锁定",
        "左前门", "右前门", "左后门", "右后门",
    ],
}


def enhance_skill_metadata(skills_dir: Path) -> Dict:
    """增强技能元数据"""
    print("=" * 70)
    print("技能数据增强")
    print("=" * 70)

    # 加载原始数据
    metadata_file = skills_dir / "skillMetaData.json"
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"\n原始技能数: {len(metadata)}")

    # 统计每个技能的示例数量
    enhanced_count = 0
    total_examples_added = 0

    for skill_meta in metadata:
        skill_name = skill_meta.get("name", "")
        description = skill_meta.get("description", "")

        # 推断类别
        category = _infer_category(skill_name, description)

        # 提取现有示例
        existing_examples = _extract_examples(description)

        # 如果示例不足，添加模板示例
        if len(existing_examples) < 5 and category in EXAMPLE_TEMPLATES:
            # 添加相关类别的示例
            template_examples = EXAMPLE_TEMPLATES[category]

            # 选择与技能相关的示例
            relevant_examples = []
            for example in template_examples:
                # 检查示例是否与技能相关
                if any(word in skill_name.lower() or word in description.lower()
                       for word in example.lower().split()):
                    relevant_examples.append(example)

            # 限制数量
            if len(relevant_examples) > 0:
                skill_meta["enhanced_examples"] = relevant_examples[:5]
                enhanced_count += 1
                total_examples_added += len(relevant_examples[:5])

    print(f"增强技能数: {enhanced_count}")
    print(f"新增示例数: {total_examples_added}")

    # 保存增强后的数据
    enhanced_file = skills_dir / "skillMetaData_enhanced.json"
    with open(enhanced_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"\n增强数据已保存: {enhanced_file}")

    return {
        'total_skills': len(metadata),
        'enhanced_count': enhanced_count,
        'examples_added': total_examples_added
    }


def _infer_category(skill_name: str, description: str) -> str:
    """推断类别"""
    text = (skill_name + " " + description).lower()

    if any(kw in text for kw in ["空调", "温度", "ac", "climate"]):
        return "climate_control"
    elif any(kw in text for kw in ["座椅", "seat", "加热", "通风"]):
        return "seat_control"
    elif any(kw in text for kw in ["车窗", "window", "天窗", "sunroof"]):
        return "window_control"
    elif any(kw in text for kw in ["灯光", "灯", "light"]):
        return "light_control"
    elif any(kw in text for kw in ["音乐", "music", "音量", "volume"]):
        return "music_media"
    elif any(kw in text for kw in ["导航", "navigation", "gps"]):
        return "navigation"
    elif any(kw in text for kw in ["电话", "phone", "拨打"]):
        return "phone_call"
    elif any(kw in text for kw in ["镜子", "mirror", "后视镜"]):
        return "mirror_control"
    elif any(kw in text for kw in ["车门", "door", "后备箱", "trunk"]):
        return "door_control"
    else:
        return "system_settings"


def _extract_examples(description: str) -> List[str]:
    """提取示例"""
    examples = []
    import re
    pattern = r'\(([^\)]+)\)'
    matches = re.findall(pattern, description)
    examples.extend(matches)
    return examples


def main():
    """主函数"""
    skills_dir = Path("E:/ai/py/whisperModel/vc/skills")

    # 增强技能数据
    stats = enhance_skill_metadata(skills_dir)

    # 创建增强报告
    print("\n" + "=" * 70)
    print("数据增强报告")
    print("=" * 70)
    print(f"总技能数: {stats['total_skills']}")
    print(f"增强技能数: {stats['enhanced_count']}")
    print(f"新增示例数: {stats['examples_added']}")
    print(f"平均每技能新增: {stats['examples_added']/stats['enhanced_count']:.1f} 个示例")

    print("\n建议下一步:")
    print("1. 使用增强后的数据重新训练路由模型")
    print("2. 测试混合检索器在增强数据上的性能")
    print("3. 如果准确率仍<80%，考虑使用更大的embedding模型")


if __name__ == "__main__":
    main()
