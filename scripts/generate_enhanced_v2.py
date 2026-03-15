"""
增强版规则训练样本生成器
使用改进的规则系统，为每个技能生成 8+ 条高质量样本
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import random


# ============ 扩展同义词库 ============
SYNONYMS = {
    # 空调相关
    "空调": ["冷气", "暖气", "风", "AC", "空气", "空调器", "出风", "吹风"],
    "打开": ["开启", "启动", "开", "把...打开", "开开", "打开一下"],
    "关闭": ["关掉", "关上", "关", "把...关闭", "关了", "别吹了"],

    # 车窗相关
    "车窗": ["玻璃", "窗户", "窗", "车窗玻璃", "玻璃窗"],
    "降下": ["放下", "降低", "打开", "开条缝", "降一点"],
    "升起": ["升起", "抬起", "关闭", "关上", "升起来"],

    # 座椅相关
    "座椅": ["座位", "椅子", "坐垫", "位子"],
    "加热": ["加热功能", "坐垫加热", "座椅加热", "热一下"],
    "通风": ["通风功能", "座椅通风", "吹一下", "凉快一下"],
    "调节": ["调整", "设置", "设为", "调", "弄一下"],

    # 后视镜
    "后视镜": ["镜子", "耳朵", "侧镜", "外后视镜"],
    "折叠": ["收起", "收回", "折叠起来", "关上"],

    # 灯光
    "灯": ["灯光", "照明", "灯泡", "阅读灯", "氛围灯"],
    "打开": ["开", "点亮", "开启", "打开"],

    # 音量/音乐
    "音量": ["声音", "音乐", "音量大小", "播放"],
    "调大": ["大声点", "提高", "增加", "声音大点", "放大点"],
    "调小": ["小声点", "降低", "减小", "声音小点", "放小点"],

    # 位置相关
    "主驾": ["驾驶员", "驾驶位", "左前", "司机", "前面左边"],
    "副驾": ["乘客", "副驾驶", "右前", "前面右边"],
    "二排": ["后排", "后面", "二座位", "后座"],
    "全车": ["全部", "整车", "所有", "整体", "到处"],

    # 程度副词
    "非常": ["很", "特别", "太", "超", "超级", "真是"],
    "一点": ["一下", "一点", "一点点", "稍微", "少许"],
    "全部": ["所有", "全部", "都", "统统"],
}


# ============ 场景模板库 ============
SCENARIO_TEMPLATES = {
    "climate_control": {
        "热": [
            "有点热",
            "太热了",
            "车里热死了",
            "热得受不了",
            "怎么这么热",
            "热死了热死了",
            "一身汗",
            "汗流浃背",
        ],
        "冷": [
            "有点冷",
            "太冷了",
            "车里冷",
            "冷死了",
            "冻死了",
            "好冷",
            "有点凉",
        ],
        "闷": [
            "太闷了",
            "车里闷",
            "透气",
            "想透透气",
            "闷死了",
            "空气不流通",
        ],
        "风大": [
            "风太大了",
            "吹得头疼",
            "风太大",
            "别吹了",
            "风小点",
        ],
        "空调": [
            "开空调",
            "打开空调",
            "开下冷气",
            "开个暖气",
            "把风开大点",
            "关了空调",
            "关掉冷气",
        ],
    },

    "window_control": {
        "透气": [
            "想透气",
            "透透气",
            "开点缝",
            "开条缝",
            "降一点玻璃",
            "窗户开一点",
        ],
        "噪音": [
            "外面太吵",
            "太吵了",
            "关窗安静点",
            "把窗户关上",
            "噪音太大",
        ],
        "冷风": [
            "冷风吹进来了",
            "外面风大",
            "把窗户升起来",
            "关窗户",
            "车窗关一下",
        ],
        "烟味": [
            "烟味太大",
            "有烟味",
            "散散味",
            "换换气",
            "开窗散味",
        ],
        "风景": [
            "想看看外面",
            "窗户打开",
            "降下玻璃",
            "把窗户全降了",
        ],
    },

    "seat_control": {
        "加热": [
            "背有点凉",
            "腰有点酸",
            "座位冷",
            "座椅加热",
            "打开加热",
            "把座椅加热打开",
            "坐垫加热",
            "加热一下",
        ],
        "通风": [
            "背上出汗",
            "坐着太热",
            "后背湿了",
            "座椅通风",
            "打开通风",
            "吹吹背",
            "凉快一下",
        ],
        "调节": [
            "座椅往后调",
            "靠背调一下",
            "座椅往前",
            "头枕调高点",
            "腰托调一下",
        ],
    },

    "light_control": {
        "暗": [
            "太暗了",
            "看不清",
            "有点暗",
            "灯打开",
            "开灯",
            "太黑了",
        ],
        "亮": [
            "太亮了",
            "刺眼",
            "灯光调暗",
            "亮度调低",
            "不想要那么亮",
        ],
        "阅读": [
            "开阅读灯",
            "要看书",
            "开个灯",
            "副驾灯打开",
        ],
        "氛围": [
            "氛围灯打开",
            "开个氛围",
            "灯光变色",
            "七彩灯",
        ],
    },

    "mirror_control": {
        "折叠": [
            "折叠后视镜",
            "收起后视镜",
            "关上耳朵",
            "折叠起来",
            "收回镜子",
        ],
        "调节": [
            "后视镜调一下",
            "镜子位置不对",
            "调镜子",
            "后视镜往下",
            "镜子往左",
        ],
    },

    "music_media": {
        "播放": [
            "放歌",
            "播放音乐",
            "来点音乐",
            "放首歌",
            "听歌",
        ],
        "音量": [
            "声音大点",
            "大声点",
            "音量调高",
            "声音小点",
            "小声点",
            "音量调低",
            "声音刚好",
            "音量中等",
        ],
        "切歌": [
            "下一首",
            "切歌",
            "换一首",
            "跳过",
        ],
    },

    "navigation": {
        "导航": [
            "开导航",
            "打开导航",
            "我要去",
            "导航到",
            "设置目的地",
        ],
        "取消": [
            "取消导航",
            "关闭导航",
            "不用导航了",
        ],
    },

    "phone_call": {
        "打电话": [
            "给...打电话",
            "呼叫",
            "拨打电话",
            "联系",
        ],
        "挂断": [
            "挂电话",
            "挂断",
            "结束通话",
        ],
    },

    "vehicle_info": {
        "查询": [
            "现在...多少",
            "查一下",
            "看看",
            "什么情况",
            "告诉我",
        ],
    },

    "system_settings": {
        "设置": [
            "设置一下",
            "调一下",
            "更改设置",
            "配置",
        ],
    },
}


# ============ 动作-对象映射 ============
ACTION_OBJECT_MAP = {
    "打开": ["空调", "车窗", "座椅", "灯", "加热", "通风", "音乐", "导航"],
    "关闭": ["空调", "车窗", "灯", "加热", "通风", "音乐", "导航"],
    "调节": ["座椅", "音量", "灯光", "后视镜", "温度"],
    "升起": ["车窗", "后视镜"],
    "降下": ["车窗"],
}


def extract_action_and_object(skill_name: str, description: str) -> Tuple[str, str, str]:
    """
    提取动作和对象

    Returns:
        (action, object, category)
    """
    name_lower = skill_name.lower()
    desc_lower = description.lower()

    # 提取对象
    obj = None
    if "air" in name_lower or "空调" in description:
        obj = "空调"
    elif "window" in name_lower or "车窗" in description or "玻璃" in description:
        obj = "车窗"
    elif "seat" in name_lower or "座椅" in description:
        obj = "座椅"
    elif "light" in name_lower or "灯" in description or "灯光" in description:
        obj = "灯"
    elif "mirror" in name_lower or "后视镜" in description or "镜子" in description:
        obj = "后视镜"
    elif "music" in name_lower or "音量" in description or "声音" in description:
        obj = "音量"
    elif "navigation" in name_lower or "导航" in description:
        obj = "导航"
    elif "phone" in name_lower or "电话" in description:
        obj = "电话"

    # 提取动作
    action = None
    if "open" in name_lower or "打开" in description or "开启" in description:
        action = "打开"
    elif "close" in name_lower or "关闭" in description:
        action = "关闭"
    elif "adjust" in name_lower or "调节" in description or "调整" in description:
        action = "调节"
    elif "fold" in name_lower or "折叠" in description or "收起" in description:
        action = "折叠"
    elif "heat" in name_lower or "加热" in description:
        action = "加热"
    elif "ventilate" in name_lower or "通风" in description:
        action = "通风"

    # 确定分类
    category = guess_category(skill_name, description)

    return action, obj, category


def guess_category(skill_name: str, description: str) -> str:
    """根据技能名称和描述猜测分类"""
    name_lower = skill_name.lower()
    desc_lower = description.lower()

    if "air" in name_lower or "空调" in description:
        return "climate_control"
    elif "window" in name_lower or "车窗" in description or "玻璃" in description:
        return "window_control"
    elif "seat" in name_lower or "座椅" in description:
        return "seat_control"
    elif "light" in name_lower or "灯" in description or "灯光" in description:
        return "light_control"
    elif "mirror" in name_lower or "后视镜" in description:
        return "mirror_control"
    elif "music" in name_lower or "音量" in name_lower or "声音" in description:
        return "music_media"
    elif "navigation" in name_lower or "导航" in description:
        return "navigation"
    elif "phone" in name_lower or "电话" in description:
        return "phone_call"
    elif "query" in name_lower or "查询" in description or "现在" in description:
        return "vehicle_info"
    else:
        return "system_settings"


def generate_standard_queries(action: str, obj: str) -> List[str]:
    """生成标准型表达"""
    queries = []

    if action and obj:
        # 基础表达
        queries.append(f"{action}{obj}")
        queries.append(f"把{obj}{action}")
        queries.append(f"帮我{action}{obj}")
        queries.append(f"{action}一下{obj}")

        # 同义词替换
        obj_synonyms = SYNONYMS.get(obj, [obj])
        action_synonyms = SYNONYMS.get(action, [action])

        for obj_syn in obj_synonyms[:3]:  # 限制数量
            queries.append(f"{action}{obj_syn}")

    return queries[:6]  # 返回最多 6 条


def generate_scenario_queries(category: str, action: str, obj: str) -> List[str]:
    """生成场景型表达"""
    queries = []

    if category in SCENARIO_TEMPLATES:
        templates = SCENARIO_TEMPLATES[category]

        # 根据动作选择合适的场景
        if category == "climate_control":
            if action == "打开" or obj == "空调":
                queries.extend(templates.get("热", [])[:3])
                queries.extend(templates.get("空调", [])[:3])
            elif action == "关闭":
                queries.extend(templates.get("冷", [])[:2])
                queries.extend(templates.get("风大", [])[:2])

        elif category == "window_control":
            if action == "打开" or action == "降下":
                queries.extend(templates.get("透气", [])[:3])
                queries.extend(templates.get("烟味", [])[:2])
            elif action == "关闭" or action == "升起":
                queries.extend(templates.get("噪音", [])[:2])
                queries.extend(templates.get("冷风", [])[:2])

        elif category == "seat_control":
            if action and ("加热" in action or "heat" in action.lower()):
                queries.extend(templates.get("加热", [])[:4])
            elif action and ("通风" in action or "ventilate" in action.lower()):
                queries.extend(templates.get("通风", [])[:4])
            else:
                queries.extend(templates.get("调节", [])[:3])

        elif category == "light_control":
            if action == "打开":
                queries.extend(templates.get("暗", [])[:4])
            elif action == "关闭":
                queries.extend(templates.get("亮", [])[:3])
            else:
                queries.extend(templates.get("阅读", [])[:3])

        elif category == "music_media":
            if obj == "音量":
                queries.extend(templates.get("音量", [])[:4])
            else:
                queries.extend(templates.get("播放", [])[:3])

        else:
            # 其他分类，取前 3 个模板
            for scenario_list in templates.values():
                queries.extend(scenario_list[:2])
                if len(queries) >= 5:
                    break

    return queries[:6]  # 返回最多 6 条


def generate_colloquial_queries(action: str, obj: str, category: str) -> List[str]:
    """生成口语型表达"""
    queries = []

    # 极简表达
    if obj:
        queries.append(f"{obj}")
        queries.append(f"弄一下{obj}")
        queries.append(f"把{obj}弄一下")
        queries.append(f"{obj}弄一下")

    # 方言/俗称
    if category == "climate_control":
        queries.extend(["开风", "关风", "来点风", "别吹了"])
    elif category == "window_control":
        queries.extend(["开窗", "关窗", "降玻璃", "升玻璃"])
    elif category == "seat_control":
        queries.extend(["热座", "凉座", "座位弄一下"])
    elif category == "light_control":
        queries.extend(["开灯", "关灯", "灯亮一下"])

    # 省略表达
    if action:
        queries.append(f"{action}一下")
        queries.append(f"帮我{action}一下")

    # 程度副词
    if obj:
        for degree in ["一点", "稍微", "一点点"]:
            queries.append(f"{obj}{degree}")

    return list(set(queries))  # 去重


def generate_negative_queries(action: str, obj: str, category: str) -> List[str]:
    """生成否定/反向型表达"""
    queries = []

    if category == "climate_control":
        queries.extend([
            "别吹风了",
            "太冷了关掉",
            "不想要那么冷",
            "风太大了",
            "太热了"
        ])
    elif category == "window_control":
        queries.extend([
            "别开窗",
            "关上吧",
            "外面太吵",
            "不想开窗",
            "不要开那么大"
        ])
    elif category == "light_control":
        queries.extend([
            "太亮了",
            "不想要那么亮",
            "关了算了",
            "太刺眼",
            "不需要灯"
        ])
    elif category == "music_media":
        queries.extend([
            "太吵了",
            "声音小点",
            "不要音乐",
            "静音",
            "别放了"
        ])

    # 通用否定
    if obj:
        queries.append(f"不要{obj}")
        queries.append(f"{obj}关了")
        queries.append(f"别弄{obj}")

    return list(set(queries))


def generate_context_queries(action: str, obj: str, category: str) -> List[str]:
    """生成上下文型表达"""
    queries = []

    # 连续操作
    if category == "climate_control" and category == "window_control":
        queries.extend([
            "先开空调",
            "还是开窗吧",
            "先关窗再开空调"
        ])

    # 上下文依赖
    queries.extend([
        "和刚才一样",
        "再弄一次",
        "保持这样",
        "恢复默认"
    ])

    # 条件表达
    if obj:
        queries.append(f"如果...就{action}{obj}")
        queries.append(f"好像{obj}没开")

    return list(set(queries))


def combine_with_positions(action: str, obj: str) -> List[str]:
    """组合位置信息"""
    queries = []
    positions = ["主驾", "副驾", "二排", "全车"]

    if not obj:
        return queries

    # 随机选择几个位置组合（避免过多）
    selected_positions = random.sample(positions, min(3, len(positions)))

    for pos in selected_positions:
        if action:
            queries.append(f"{action}{pos}{obj}")
            queries.append(f"把{pos}{obj}{action}")
        queries.append(f"{pos}{obj}")
        queries.append(f"{pos}的{obj}")

    return queries


def generate_variations(skill_name: str, description: str, existing_queries: List[str]) -> List[str]:
    """
    为技能生成多样化的训练样本

    Args:
        skill_name: 技能名称
        description: 技能描述
        existing_queries: 已有的查询

    Returns:
        扩展后的查询列表
    """
    queries = list(existing_queries)

    # 提取关键信息
    action, obj, category = extract_action_and_object(skill_name, description)

    # 1. 标准型 (2-4 条)
    standard = generate_standard_queries(action, obj)
    queries.extend(standard)

    # 2. 场景型 (2-4 条)
    scenario = generate_scenario_queries(category, action, obj)
    queries.extend(scenario)

    # 3. 口语型 (2-4 条)
    colloquial = generate_colloquial_queries(action, obj, category)
    queries.extend(colloquial)

    # 4. 否定型 (1-2 条)
    negative = generate_negative_queries(action, obj, category)
    queries.extend(negative)

    # 5. 上下文型 (1-2 条)
    context = generate_context_queries(action, obj, category)
    queries.extend(context)

    # 6. 位置组合 (1-3 条，如果适用)
    if category in ["climate_control", "seat_control", "light_control", "window_control"]:
        position_queries = combine_with_positions(action, obj)
        queries.extend(position_queries)

    # 去重但保持顺序
    seen = set()
    final_queries = []
    for q in queries:
        q = q.strip()
        if q and q not in seen and len(q) <= 15:  # 限制长度
            seen.add(q)
            final_queries.append(q)

    return final_queries


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="增强版规则训练样本生成器")
    parser.add_argument("--input", type=str, default="data/processed/skills_database.json")
    parser.add_argument("--output", type=str, default="data/processed/skills_enhanced_v2.json")
    parser.add_argument("--target-count", type=int, default=8)

    args = parser.parse_args()

    print("=" * 60)
    print("增强版规则训练样本生成")
    print("=" * 60)

    # 加载数据
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8-sig') as f:
        skills = json.load(f)

    print(f"加载了 {len(skills)} 个技能")

    # 为每个技能生成样本
    print(f"\n开始生成样本（目标: {args.target_count} 条/技能）")
    print("-" * 60)

    enhanced_skills = []
    stats = {
        "total": 0,
        "enhanced": 0,
        "already_enough": 0,
        "insufficient": 0,
        "by_category": defaultdict(int),
    }

    for i, skill in enumerate(skills, 1):
        skill_copy = skill.copy()
        existing = skill.get("example_queries", [])

        # 生成样本
        generated = generate_variations(
            skill["name"],
            skill["description"],
            existing
        )

        # 统计分类
        category = guess_category(skill["name"], skill["description"])
        stats["by_category"][category] += len(generated)

        skill_copy["example_queries"] = generated
        stats["total"] += len(generated)
        stats["enhanced"] += 1

        if len(generated) < args.target_count:
            stats["insufficient"] += 1
        else:
            stats["already_enough"] += 1

        # 定期打印进度
        if i % 50 == 0 or len(generated) < args.target_count:
            status = "[OK]" if len(generated) >= args.target_count else "[--]"
            print(f"{status} [{i}/{len(skills)}] {skill['name'][:30]:30s}: {len(generated):2d} 条")

        enhanced_skills.append(skill_copy)

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_skills, f, ensure_ascii=False, indent=2)

    # 统计
    print("\n" + "=" * 60)
    print("生成完成")
    print("=" * 60)
    print(f"已增强: {stats['enhanced']} 个")
    print(f"满足目标: {stats['already_enough']} 个")
    print(f"不足: {stats['insufficient']} 个")
    print(f"输出文件: {output_path}")

    # 验证
    with open(output_path, 'r', encoding='utf-8') as f:
        enhanced = json.load(f)

    total_queries = sum(len(s.get("example_queries", [])) for s in enhanced)
    avg_queries = total_queries / len(enhanced)

    print(f"\n验证统计:")
    print(f"  总技能数: {len(enhanced)}")
    print(f"  总样本数: {total_queries}")
    print(f"  平均样本数: {avg_queries:.2f}")

    sufficient = sum(1 for s in enhanced if len(s.get("example_queries", [])) >= args.target_count)
    print(f"  满足目标: {sufficient}/{len(enhanced)} ({sufficient/len(enhanced)*100:.1f}%)")

    # 按分类统计
    print(f"\n按分类统计:")
    for cat, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        cat_skills = sum(1 for s in enhanced if guess_category(s["name"], s["description"]) == cat)
        avg = count / cat_skills if cat_skills > 0 else 0
        print(f"  {cat:20s}: {count:4d} 条 ({cat_skills} 个技能, 平均 {avg:.1f} 条/技能)")

    return str(output_path)


if __name__ == "__main__":
    main()
