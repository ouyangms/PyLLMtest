"""
使用 LLM 生成多样化训练样本
为每个类别生成高质量的泛化样本
支持：千问(Qwen)、OpenAI、本地规则
"""

import json
import time
from pathlib import Path
from typing import List, Dict
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router.category_config import CategoryConfig

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# 5维度模板
DIMENSION_TEMPLATES = {
    "standard": {
        "description": "标准指令型：清晰完整的表达",
        "prompt": "生成{count}个标准、清晰的{category}指令，要求：\n"
                 "1. 使用完整的主谓宾结构\n"
                 "2. 明确指出操作对象和目标状态\n"
                 "3. 使用正式或常用的表达方式\n"
                 "4. 避免省略主语或模糊指代\n\n"
                 "示例格式：\n"
                 "- 打开主驾驶座椅加热\n"
                 "- 将空调温度设置为24度\n\n"
                 "请生成{count}个{category}的标准指令（仅输出指令列表，不要解释）："
    },
    "scenario": {
        "description": "场景/感受型：描述当前状态或感受",
        "prompt": "生成{count}个描述场景或感受的{category}指令，要求：\n"
                 "1. 从用户感受出发（冷、热、暗、吵等）\n"
                 "2. 描述当前状态而非直接操作\n"
                 "3. 系统需要推断用户意图\n"
                 "4. 更加自然、拟人化\n\n"
                 "示例格式：\n"
                 "- 车里太冷了\n"
                 "- 有点看不清路\n"
                 "- 腰有点酸\n\n"
                 "请生成{count}个{category}的场景感受型指令："
    },
    "colloquial": {
        "description": "模糊/口语型：省略主语、方言词、极简表达",
        "prompt": "生成{count}个口语化、简洁的{category}指令，要求：\n"
                 "1. 省略主语（直接说动作）\n"
                 "2. 使用常用简称或口语\n"
                 "3. 极简表达（2-5字）\n"
                 "4. 包含一些方言或习惯用法\n\n"
                 "示例格式：\n"
                 "- 开点缝\n"
                 "- 太热了\n"
                 "- 调高点\n\n"
                 "请生成{count}个{category}的口语化指令："
    },
    "negative": {
        "description": "否定/反向型：关闭、停止、降低等反向操作",
        "prompt": "生成{count}个反向操作的{category}指令，要求：\n"
                 "1. 使用否定词（不、别、停止、关闭）\n"
                 "2. 降低、减小、减弱类操作\n"
                 "3. 取消、撤销类操作\n"
                 "4. 边界情况处理\n\n"
                 "示例格式：\n"
                 "- 不需要通风了\n"
                 "- 停止加热\n"
                 "- 别太亮\n\n"
                 "请生成{count}个{category}的反向操作指令："
    },
    "contextual": {
        "description": "组合/上下文型：多轮对话、复杂指令",
        "prompt": "生成{count}个复杂或上下文相关的{category}指令，要求：\n"
                 "1. 多个操作组合（同时调节多个参数）\n"
                 "2. 指定具体位置或对象\n"
                 "3. 包含数值或程度描述\n"
                 "4. 上下文相关的表达\n\n"
                 "示例格式：\n"
                 "- 把主驾座椅调低一点，大概两档\n"
                 "- 后排窗户都开条缝，透气就行\n"
                 "- 左边镜子往上抬，我要看后面\n\n"
                 "请生成{count}个{category}的复杂指令："
    }
}


# 类别描述（用于生成）
CATEGORY_DESCRIPTIONS = {
    "climate_control": "空调、温度、风量、风向、除雾、香氛等车内气候控制",
    "seat_control": "座椅加热、通风、按摩、位置调节、记忆、腰托、腿托、头枕",
    "window_control": "车窗升降、天窗开合、遮阳帘控制、透气模式",
    "light_control": "车内灯光、阅读灯、氛围灯、大灯、转向灯、日行灯",
    "mirror_control": "后视镜调节、折叠、加热、防眩目",
    "door_control": "车门开关、锁车、解锁、后备箱、尾门、儿童锁",
    "music_media": "音乐播放、音量调节、蓝牙、电台、切歌、暂停、均衡器",
    "navigation": "导航设置、目的地搜索、路线规划、地图缩放、避开拥堵",
    "phone_call": "拨打电话、接听、挂断、蓝牙电话、联系人",
    "vehicle_info": "查询车辆状态、胎压、油量、电量、续航、里程、设置",
    "system_settings": "系统设置、显示、主题、语言、连接、偏好配置",
    "driving_assist": "巡航控制、辅助驾驶、车道保持、自动刹车、泊车辅助",
    "charging_energy": "充电控制、充电桩、电量管理、预约充电、放电"
}


def get_openai_client():
    """获取 OpenAI 客户端"""
    try:
        from openai import OpenAI
        # 检查是否有 API key
        import os
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            return OpenAI(api_key=api_key)
    except Exception as e:
        print(f"OpenAI 不可用: {e}")
    return None


def generate_samples_qwen(category: str, dimension: str, count: int, client_config: dict, model: str = "qwen-turbo") -> List[str]:
    """使用千问 API 生成样本"""
    prompt = DIMENSION_TEMPLATES[dimension]["prompt"].format(
        count=count,
        description=CATEGORY_DESCRIPTIONS[category],
        category=category
    )

    # 针对千问优化提示词
    prompt += "\n\n重要：请直接输出指令列表，每行一个，不要添加任何编号、序号或其他符号。"

    try:
        content = call_qwen_api(prompt, client_config, model)

        if not content:
            return []

        # 解析生成的样本
        samples = []
        for line in content.split('\n'):
            line = line.strip()

            # 移除常见的前缀符号
            for prefix in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.",
                           "-", "*", "•", "、", ")", "(", "（", "）", "【", "】"]:
                if line.startswith(prefix):
                    line = line[len(prefix):].strip()

            # 过滤无效行
            if line and len(line) >= 2 and len(line) <= 30:
                # 排除明显的解释文字
                if not line.startswith(("注意", "以下是", "示例", "指令", "生成")):
                    samples.append(line)

        return samples[:count]

    except Exception as e:
        print(f"  [错误] {e}")
        return []


def get_openai_client():
    """使用 OpenAI API 生成样本"""
    prompt = DIMENSION_TEMPLATES[dimension]["prompt"].format(
        count=count,
        description=CATEGORY_DESCRIPTIONS[category],
        category=category
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个车载语音助手训练数据生成专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )

        content = response.choices[0].message.content

        # 解析生成的样本
        samples = []
        for line in content.split('\n'):
            line = line.strip()
            # 移除序号和符号
            line = line.lstrip('0123456789.-*、）)]')
            if line and len(line) >= 2 and len(line) <= 30:
                samples.append(line)

        return samples[:count]

    except Exception as e:
        print(f"  [错误] {e}")
        return []


def generate_samples_local(category: str, dimension: str, count: int) -> List[str]:
    """本地规则生成样本（降级方案）"""
    samples = []

    # 基于规则生成
    if dimension == "standard":
        templates = {
            "climate_control": ["打开空调", "关闭空调", "设置空调温度为{temp}度", "将风量调大", "将风量调小"],
            "seat_control": ["打开座椅加热", "关闭座椅加热", "调节座椅位置", "打开座椅通风"],
            "window_control": ["打开车窗", "关闭车窗", "打开天窗", "车窗降下一半"],
            "light_control": ["打开阅读灯", "关闭阅读灯", "打开大灯", "调节灯光亮度"],
            "mirror_control": ["折叠后视镜", "展开后视镜", "调节后视镜"],
            "door_control": ["打开车门", "关闭车门", "打开后备箱", "锁车"],
            "music_media": ["播放音乐", "暂停音乐", "增大音量", "减小音量", "切换歌曲"],
            "navigation": ["开始导航", "取消导航", "搜索目的地", "设置路线"],
            "phone_call": ["拨打{name}的电话", "接听电话", "挂断电话"],
            "vehicle_info": ["查询剩余电量", "查询续航里程", "查询胎压"],
            "system_settings": ["打开设置", "调节显示亮度", "切换语言"],
            "driving_assist": ["开启巡航", "关闭巡航", "开启车道保持"],
            "charging_energy": ["开始充电", "停止充电", "设置充电时间"]
        }

        base_templates = templates.get(category, ["打开", "关闭", "调节"])

        for i in range(count):
            import random
            template = random.choice(base_templates)
            if "{temp}" in template:
                template = template.replace("{temp}", str(random.randint(16, 28)))
            elif "{name}" in template:
                template = template.replace("{name}", "张三")
            samples.append(template)

    elif dimension == "scenario":
        templates = {
            "climate_control": ["太冷了", "太热了", "有点闷", "空气不好"],
            "seat_control": ["腰有点酸", "背部不舒服", "有点冷", "有点热"],
            "window_control": ["想透透气", "有点闷", "光线太强"],
            "light_control": ["太暗了", "太亮了", "看不清"],
            "mirror_control": ["看不清后面", "镜子晃眼"],
            "door_control": ["打不开车门"],
            "music_media": ["声音太小", "声音太大", "想听歌"],
            "navigation": ["不知道怎么走", "想找地方"],
            "phone_call": ["有人打电话"],
            "vehicle_info": ["还有多少电", "能跑多远"],
            "system_settings": ["屏幕太暗", "屏幕太亮"],
            "driving_assist": ["跟车太近"],
            "charging_energy": ["需要充电"]
        }

        base_templates = templates.get(category, ["太{adj}", "有点{adj}"])

        for i in range(count):
            import random
            samples.append(random.choice(base_templates))

    elif dimension == "colloquial":
        samples = ["开点", "关了", "调大", "调小", "高点", "低点"] * count

    elif dimension == "negative":
        samples = ["不开了", "别调了", "停止", "关闭", "取消"] * count

    elif dimension == "contextual":
        samples = ["把主驾的调一下", "两边都开", "全部关闭"] * count

    return samples[:count]


def augment_category(
    category: str,
    samples_per_dimension: int = 20,
    use_openai: bool = True
) -> List[str]:
    """为单个类别生成增强样本"""
    print(f"\n处理类别: {category}")

    all_samples = []

    # 尝试使用 OpenAI
    client = None
    if use_openai:
        client = get_openai_client()
        if not client:
            print("  [降级] 使用本地规则生成")
            use_openai = False

    # 为每个维度生成样本
    for dimension, template in DIMENSION_TEMPLATES.items():
        print(f"  [{template['description']}] 生成 {samples_per_dimension} 个样本...")

        if use_openai:
            samples = generate_samples_openai(category, dimension, samples_per_dimension, client)
        else:
            samples = generate_samples_local(category, dimension, samples_per_dimension)

        print(f"    实际生成: {len(samples)} 个")
        all_samples.extend(samples)

        # 避免 API 限流
        if use_openai:
            time.sleep(1)

    # 去重
    unique_samples = list(set(all_samples))
    if len(unique_samples) < len(all_samples):
        print(f"  去重: {len(all_samples)} -> {len(unique_samples)}")

    return unique_samples


def main():
    import argparse

    parser = argparse.ArgumentParser(description="LLM 数据增强")
    parser.add_argument(
        "--samples-per-dimension",
        type=int,
        default=20,
        help="每个维度生成的样本数"
    )
    parser.add_argument(
        "--use-openai",
        action="store_true",
        help="使用 OpenAI API"
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="指定类别（默认处理所有类别）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/augmented_samples.json",
        help="输出文件"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LLM 数据增强")
    print("=" * 60)
    print(f"每维度样本数: {args.samples_per_dimension}")
    print(f"使用 OpenAI: {args.use_openai}")
    print(f"目标类别: {args.category or '全部'}")

    # 确定要处理的类别
    if args.category:
        categories = [args.category]
    else:
        categories = CategoryConfig.CATEGORIES

    # 为每个类别生成样本
    augmented_data = []

    for category in categories:
        samples = augment_category(category, args.samples_per_dimension, args.use_openai)

        # 获取类别 ID
        category_id = CategoryConfig.get_category_id(category)

        # 转换为数据格式
        for sample in samples:
            augmented_data.append({
                "text": sample,
                "category_id": category_id,
                "category": category,
                "source": "llm_augment"
            })

    print("\n" + "=" * 60)
    print(f"总计生成: {len(augmented_data)} 个样本")

    # 保存
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(augmented_data, f, ensure_ascii=False, indent=2)

    print(f"已保存: {output_path}")

    # 统计
    print("\n类别分布:")
    from collections import Counter
    counter = Counter([item["category"] for item in augmented_data])
    for cat, count in sorted(counter.items()):
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
