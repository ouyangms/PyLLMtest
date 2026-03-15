"""
路由分类配置
定义13个车控技能分类体系，实现自动分类逻辑
"""

from typing import Dict, List, Optional, Set
import re


class CategoryConfig:
    """路由分类配置"""

    # 13个主要分类
    CATEGORIES = [
        "climate_control",      # 空调控制
        "seat_control",         # 座椅控制
        "window_control",       # 车窗控制
        "light_control",        # 灯光控制
        "mirror_control",       # 后视镜控制
        "door_control",         # 车门控制
        "music_media",          # 音乐媒体
        "navigation",           # 导航
        "phone_call",           # 电话
        "vehicle_info",         # 车辆信息查询
        "system_settings",      # 系统设置
        "driving_assist",       # 驾驶辅助
        "charging_energy",      # 充电/能源
    ]

    # 分类关键词映射
    CATEGORY_KEYWORDS = {
        "climate_control": {
            "primary": ["空调", "冷气", "暖气", "温度", "风向", "风量", "除雾", "除霜",
                       "air", "conditioner", "ac", "hvac", "temperature", "climate"],
            "secondary": ["制冷", "制热", "升温", "降温", "恒温", "auto", "内循环", "外循环",
                         "净化", "负离子", "香氛", "干燥", "防雾"],
            "skills_prefix": ["AirConditioner", "ZoneAirConditioner", "AutoAirConditioner",
                            "PurificationModeAir", "Fragrance", "SyncAirConditioner"],
        },
        "seat_control": {
            "primary": ["座椅", "座位", "坐垫", "靠背", "腰托", "腿托", "头枕",
                       "seat", "chair", "cushion"],
            "secondary": ["加热", "通风", "按摩", "记忆", "迎宾", "方便进出", "折叠",
                         "调节", "角度", "前后", "高低", "侧翼", "动态"],
            "skills_prefix": ["Seat", "Cushion", "Backrest", "Lumbar", "LegRest"],
        },
        "window_control": {
            "primary": ["车窗", "玻璃", "窗户", "window", "glass"],
            "secondary": ["升", "降", "开", "关", "锁", "条缝", "透气", "天窗", "天幕",
                         "遮阳帘", "sunroof", "sunshade"],
            "skills_prefix": ["Window", "Sunroof", "Sunshade"],
        },
        "light_control": {
            "primary": ["灯", "光", "照明", "light", "lamp", "lighting"],
            "secondary": ["大灯", "近光", "远光", "雾灯", "阅读灯", "氛围灯", "顶灯",
                         "日行", "转向", "双闪", "示宽", "刹车", "倒车", "迎宾",
                         "headlight", "fog", "reading", "ambient"],
            "skills_prefix": ["Light", "Lamp", "Headlight", "Fog", "Reading"],
        },
        "mirror_control": {
            "primary": ["后视镜", "镜子", "mirror", "side", "rearview"],
            "secondary": ["折叠", "展开", "加热", "防眩", "调节", "外后视镜", "内后视镜",
                         "流媒体", "折叠"],
            "skills_prefix": ["SideMirror", "Mirror"],
        },
        "door_control": {
            "primary": ["车门", "门", "后备箱", "尾箱", "door", "trunk", "tailgate"],
            "secondary": ["锁", "解锁", "开锁", "儿童锁", "车门锁", "尾门", "地门", "天门"],
            "skills_prefix": ["Door", "Trunk", "ChildLock"],
        },
        "music_media": {
            "primary": ["音乐", "媒体", "音量", "声音", "音效", "播放", "暂停", "停止",
                       "music", "media", "audio", "sound", "volume"],
            "secondary": ["均衡器", "环绕", "低音", "高音", "蓝牙", "电台", "歌", "曲",
                         "equalizer", "surround", "bass", "treble"],
            "skills_prefix": ["Volume", "Sound", "Music", "Audio", "Multimedia", "Equalizer"],
        },
        "navigation": {
            "primary": ["导航", "地图", "路线", "destination", "route", "map", "navigation"],
            "secondary": ["目的地", "位置", "搜索", "规划", "拥堵", "避开"],
            "skills_prefix": ["Navigation", "Map", "Route"],
        },
        "phone_call": {
            "primary": ["电话", "通话", "呼叫", "拨打", "phone", "call", "telephone"],
            "secondary": ["接听", "挂断", "免提", "蓝牙电话", "联系人"],
            "skills_prefix": ["Phone", "Call"],
        },
        "vehicle_info": {
            "primary": ["查询", "状态", "信息", "多少", "如何", "怎么样",
                       "query", "info", "status", "check", "information"],
            "secondary": ["胎压", "油量", "电量", "续航", "里程", "温度", "速度", "设置"],
            "skills_prefix": ["Query", "Info", "Status", "Check"],
        },
        "system_settings": {
            "primary": ["设置", "配置", "模式", "偏好", "settings", "config", "setup", "mode"],
            "secondary": ["显示", "主题", "语言", "单位", "时间", "日期", "账号", "连接",
                         "wifi", "蓝牙", "热点"],
            "skills_prefix": ["Settings", "Setting", "Config", "Setup", "Mode", "Display"],
        },
        "driving_assist": {
            "primary": ["辅助", "巡航", "自动驾驶", "车道", "预警", "刹车",
                       "assist", "cruise", "autopilot", "lane", "warning"],
            "secondary": ["ACC", "LKA", "AEB", "自适应", "跟车", "保持", "偏离", "碰撞",
                         "泊车", "停车", "挪车"],
            "skills_prefix": ["Assist", "Cruise", "Pilot", "Lane", "Brake", "Parking"],
        },
        "charging_energy": {
            "primary": ["充电", "电量", "能源", "充电桩", "charging", "battery", "energy"],
            "secondary": ["交流", "直流", "快充", "慢充", "预约", "续航", "放电", "v2l"],
            "skills_prefix": ["Charging", "Charge", "Battery", "Energy", "Discharge"],
        },
    }

    # 域映射
    DOMAINS = {
        "hvac": ["climate_control"],
        "body": ["seat_control", "window_control", "light_control", "mirror_control", "door_control"],
        "infotainment": ["music_media", "navigation", "phone_call"],
        "vehicle": ["vehicle_info", "system_settings"],
        "adas": ["driving_assist"],
        "powertrain": ["charging_energy"],
    }

    @classmethod
    def classify_by_name(cls, skill_name: str, description: str = "") -> str:
        """
        根据技能名称和描述进行分类

        Args:
            skill_name: 技能名称
            description: 技能描述

        Returns:
            分类名称
        """
        # 合并名称和描述作为分析文本
        text = f"{skill_name} {description}".lower()

        # 计算每个分类的匹配分数
        scores = {}
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            score = 0

            # 检查技能名称前缀匹配（权重最高）
            for prefix in keywords.get("skills_prefix", []):
                if prefix.lower() in skill_name.lower():
                    score += 10

            # 检查主要关键词（权重中等）
            for keyword in keywords.get("primary", []):
                if keyword.lower() in text:
                    score += 3

            # 检查次要关键词（权重较低）
            for keyword in keywords.get("secondary", []):
                if keyword.lower() in text:
                    score += 1

            if score > 0:
                scores[category] = score

        # 返回得分最高的分类
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]

        # 默认分类
        return "system_settings"

    @classmethod
    def get_domain(cls, category: str) -> str:
        """
        根据分类获取所属域

        Args:
            category: 分类名称

        Returns:
            域名称
        """
        for domain, categories in cls.DOMAINS.items():
            if category in categories:
                return domain
        return "general"

    @classmethod
    def get_category_id(cls, category: str) -> int:
        """
        获取分类的ID（用于模型训练）

        Args:
            category: 分类名称

        Returns:
            分类ID (0-12)
        """
        try:
            return cls.CATEGORIES.index(category)
        except ValueError:
            return cls.CATEGORIES.index("system_settings")  # 默认

    @classmethod
    def get_category_name(cls, category_id: int) -> str:
        """
        根据分类ID获取分类名称

        Args:
            category_id: 分类ID

        Returns:
            分类名称
        """
        if 0 <= category_id < len(cls.CATEGORIES):
            return cls.CATEGORIES[category_id]
        return "system_settings"

    @classmethod
    def create_vocabulary(cls) -> Dict[str, int]:
        """
        创建字符级词汇表（用于TextCNN）

        Returns:
            字符到ID的映射字典
        """
        # 中文字符集（常用汉字）
        chinese_chars = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严"

        # 英文字母和数字
        alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789"

        # 特殊字符
        special = "，。！？、；：「」『』（）【】《》+-*/=<>@#$%^&_"

        # 合并所有字符
        all_chars = chinese_chars + alphanumeric + special

        # 创建映射（保留0给padding）
        vocab = {"<PAD>": 0, "<UNK>": 1}
        for i, char in enumerate(all_chars, start=2):
            vocab[char] = i

        return vocab

    @classmethod
    def get_synonym_dict(cls) -> Dict[str, List[str]]:
        """
        获取车控领域同义词典

        Returns:
            同义词映射字典
        """
        return {
            "空调": ["冷气", "暖气", "风", "AC"],
            "车窗": ["玻璃", "窗户", "窗"],
            "后备箱": ["尾箱", "后盖", "行李箱"],
            "后视镜": ["镜子", "耳朵", "侧镜"],
            "打开": ["开启", "启动", "开"],
            "关闭": ["关掉", "关上", "关", "关闭"],
            "主驾": ["驾驶员", "驾驶位", "左前"],
            "副驾": ["乘客", "副驾驶", "右前"],
            "二排": ["后排", "后面"],
            "全车": ["全部", "整车", "所有"],
            "调节": ["调整", "设置", "设为"],
            "升高": ["调高", "向上", "增加"],
            "降低": ["调低", "向下", "减少"],
        }


def classify_skills(skills: List[Dict]) -> List[Dict]:
    """
    为技能列表自动分类

    Args:
        skills: 技能列表

    Returns:
    添加了分类信息的技能列表
    """
    classified_skills = []

    for skill in skills:
        skill_copy = skill.copy()

        # 分类
        category = CategoryConfig.classify_by_name(
            skill.get("name", ""),
            skill.get("description", "")
        )

        skill_copy["category"] = category
        skill_copy["category_id"] = CategoryConfig.get_category_id(category)
        skill_copy["domain"] = CategoryConfig.get_domain(category)

        classified_skills.append(skill_copy)

    return classified_skills


def main():
    """测试分类配置"""
    # 测试分类
    test_cases = [
        ("OpenAirConditioner", "打开空调"),
        ("SeatHeat", "座椅加热"),
        ("OpenWindow", "打开车窗"),
        ("ControlLight", "控制灯光"),
        ("SideMirrorFold", "折叠后视镜"),
        ("QueryBatteryLevel", "查询电量"),
    ]

    print("测试自动分类:")
    print("=" * 60)

    for name, desc in test_cases:
        category = CategoryConfig.classify_by_name(name, desc)
        domain = CategoryConfig.get_domain(category)
        category_id = CategoryConfig.get_category_id(category)
        print(f"{name:30} -> {category:20} (域: {domain}, ID: {category_id})")

    print("=" * 60)
    print(f"词汇表大小: {len(CategoryConfig.create_vocabulary())}")
    print(f"分类数量: {len(CategoryConfig.CATEGORIES)}")


if __name__ == "__main__":
    main()
