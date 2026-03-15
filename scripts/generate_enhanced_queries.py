"""
高质量训练样本生成器
使用改进的规则生成方法，为每个技能生成 8+ 条高质量样本
"""

import json
import os
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# 车控领域同义词库
SYNONYMS = {
    "空调": ["冷气", "暖气", "风", "AC", "空气", "空调器"],
    "车窗": ["玻璃", "窗户", "窗", "车窗玻璃"],
    "座椅": ["座位", "椅子", "坐垫"],
    "后视镜": ["镜子", "耳朵", "侧镜", "外后视镜"],
    "打开": ["开启", "启动", "开", "把...打开"],
    "关闭": ["关掉", "关上", "关", "把...关闭"],
    "调节": ["调整", "设置", "设为", "调"],
    "主驾": ["驾驶员", "驾驶位", "左前", "司机"],
    "副驾": ["乘客", "副驾驶", "右前"],
    "二排": ["后排", "后面", "二座位"],
    "全车": ["全部", "整车", "所有", "整体"],
}

# 场景型表达模板
SCENARIO_TEMPLATES = {
    "climate_control": [
        "有点{state}",
        "车里{state}了",
        "感觉{state}",
        "太{state}了",
        "{state}得受不了",
        "想{action}一下",
    ],
    "window_control": [
        "{state}闷",
        "{state}太大",
        "烟味{state}",
        "想{action}新鲜空气",
        "{state}得慌",
    ],
    "seat_control": [
        "坐着{state}",
        "背{state}",
        "腰{state}",
        "座椅{state}",
    ],
}

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
    desc_lower = description.lower()
    name_lower = skill_name.lower()

    # 提取关键信息
    action = None
    if "open" in name_lower or "打开" in desc_lower:
        action = "打开"
    elif "close" in name_lower or "关闭" in desc_lower:
        action = "关闭"
    elif "adjust" in name_lower or "调节" in desc_lower or "set" in name_lower:
        action = "调节"

    # 提取对象
    obj = None
    if "air" in desc_lower or "空调" in description:
        obj = "空调"
    elif "window" in desc_lower or "车窗" in description or "玻璃" in description:
        obj = "车窗"
    elif "seat" in desc_lower or "座椅" in description:
        obj = "座椅"
    elif "light" in desc_lower or "灯" in description or "灯光" in description:
        obj = "灯"
    elif "mirror" in desc_lower or "后视镜" in description or "镜子" in description:
        obj = "后视镜"
    elif "music" in desc_lower or "音量" in description or "声音" in description:
        obj = "音量"

    # 如果无法提取对象，从技能名称推断
    if obj is None:
        if "aircondition" in name_lower:
            obj = "空调"
        elif "window" in name_lower:
            obj = "车窗"
        elif "seat" in name_lower:
            obj = "座椅"
        elif "light" in name_lower:
            obj = "灯"
        elif "mirror" in name_lower:
            obj = "后视镜"

    # 生成标准型（2条）
    if obj and action:
        queries.append(f"{action}{obj}")
        queries.append(f"把{obj}{action}")

    # 生成场景型（2条）
    category = guess_category(skill_name, description)
    if category in SCENARIO_TEMPLATES:
        templates = SCENARIO_TEMPLATES[category]

        # 选择合适的场景
        if category == "climate_control":
            if action == "打开" or obj == "空调":
                queries.append("有点热")
                queries.append("车里太闷了")
            elif action == "关闭":
                queries.append("有点冷")
                queries.append("风太大了")
        elif category == "window_control":
            if action == "打开" or obj == "车窗":
                queries.append("烟味太大了")
                queries.append("想透透气")
            elif action == "关闭":
                queries.append("外面太吵了")
                queries.append("冷风吹进来了")
        elif category == "seat_control":
            if "heat" in name_lower or "加热" in desc_lower:
                queries.append("背有点凉")
                queries.append("腰有点酸")
            elif "vent" in name_lower or "通风" in desc_lower:
                queries.append("背上出汗了")
                queries.append("坐着太热")

    # 生成口语型（3条）
    if obj:
        # 省略主语
        queries.append(f"{obj}打开" if action == "打开" else f"{obj}")
        queries.append(f"帮我把{obj}弄一下")

        # 简短表达
        queries.append(f"{action}一下" if action else "弄一下")

    # 生成上下文型（1条）
    if action and obj:
        queries.append(f"先{action}{obj}")

    return queries

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
    elif "music" in name_lower or "音量" in name_lower:
        return "music_media"
    elif "phone" in name_lower or "电话" in name_lower:
        return "phone_call"
    elif "navigation" in name_lower or "导航" in name_lower:
        return "navigation"
    elif "charging" in name_lower or "充电" in name_lower or "battery" in name_lower:
        return "charging_energy"
    elif "query" in name_lower or "查询" in desc_lower or "info" in desc_lower:
        return "vehicle_info"
    else:
        return "system_settings"

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="高质量训练样本生成器")
    parser.add_argument("--input", type=str, default="data/processed/skills_database.json")
    parser.add_argument("--output", type=str, default="data/processed/skills_enhanced.json")
    parser.add_argument("--target-count", type=int, default=8)

    args = parser.parse_args()

    print("=" * 60)
    print("高质量训练样本生成")
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
    }

    for i, skill in enumerate(skills, 1):
        skill_copy = skill.copy()
        existing = skill.get("example_queries", [])

        # 如果已满足数量，跳过
        if len(existing) >= args.target_count:
            skill_copy["example_queries"] = existing
            stats["already_enough"] += 1
            if i % 50 == 0:
                print(f"[{i}/{len(skills)}] 跳过: {skill['name'][:30]} ({len(existing)} 条)")
        else:
            # 生成额外样本
            needed = args.target_count - len(existing)
            generated = generate_variations(
                skill["name"],
                skill["description"],
                existing
            )

            # 合并并去重
            seen = set(existing)
            final_queries = []
            for q in existing:
                if q not in seen:
                    seen.add(q)
                    final_queries.append(q)

            for q in generated:
                if q not in seen and q not in final_queries:
                    final_queries.append(q)

            skill_copy["example_queries"] = final_queries
            stats["enhanced"] += 1
            stats["total"] += len(final_queries)

            if len(final_queries) < args.target_count:
                stats["insufficient"] += 1

            if i % 50 == 0 or len(final_queries) < args.target_count:
                print(f"[{i}/{len(skills)}] {skill['name'][:30]:30s}: {len(existing):2d} -> {len(final_queries):2d} 条")

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
    print(f"已跳过: {stats['already_enough']} 个（已满足数量）")
    print(f"已增强: {stats['enhanced']} 个")
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

    return str(output_path)

if __name__ == "__main__":
    main()
