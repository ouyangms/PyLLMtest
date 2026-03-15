"""
计算过滤无效样本后的准确率
找出模型真实能力的上限
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, 'E:/ai/py/whisperModel')

import torch
from src.router.textcnn_model import TextCNNLite
from src.router.category_config import CategoryConfig


# 定义无效模式（极度模糊、无法分类的表达）
INVALID_PATTERNS = [
    "调一调", "弄一下", "关一点", "开一点", "调一点",
    "恢复默认", "重置", "取消", "关闭", "打开", "开启",
    "弄大点", "弄小点", "调高点", "调低点",
    "增加", "减少", "变大", "变小",
]


def is_valid_sample(text):
    """判断样本是否有效（包含足够的信息）"""
    # 极短样本
    if len(text) <= 2:
        return False

    # 包含无效模式
    for pattern in INVALID_PATTERNS:
        if text == pattern:
            return False

    # 检查是否包含类别关键词
    CATEGORY_KEYWORDS = {
        "climate_control": ["空调", "温度", "风量", "风向", "除雾", "制冷", "制热"],
        "seat_control": ["座椅", "加热", "通风", "按摩", "腰托"],
        "window_control": ["车窗", "窗户", "天窗", "遮阳帘"],
        "light_control": ["灯光", "阅读灯", "氛围灯", "大灯", "亮度"],
        "mirror_control": ["后视镜", "镜子"],
        "door_control": ["车门", "后备箱", "尾门", "锁车"],
        "music_media": ["音乐", "音量", "播放", "暂停", "蓝牙", "电台", "歌曲"],
        "navigation": ["导航", "路线", "目的地", "地图"],
        "phone_call": ["电话", "拨打", "接听", "挂断"],
        "vehicle_info": ["电量", "续航", "胎压", "油量", "里程"],
        "system_settings": ["设置", "显示", "主题", "语言"],
        "driving_assist": ["巡航", "车道", "辅助", "刹车", "泊车"],
        "charging_energy": ["充电", "充电桩"]
    }

    # 至少包含一个关键词
    for keywords in CATEGORY_KEYWORDS.values():
        for keyword in keywords:
            if keyword in text:
                return True

    # 不包含任何关键词，可能是无效样本
    return False


def evaluate_filtered(model_path, test_data, vocab, filter_func=None, device="cuda"):
    """评估模型（可选过滤）"""
    model = TextCNNLite(len(vocab), num_classes=13)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    # 过滤数据
    if filter_func:
        filtered_data = [item for item in test_data if filter_func(item["text"])]
        print(f"过滤: {len(test_data)} -> {len(filtered_data)}")
        data = filtered_data
    else:
        data = test_data

    correct = 0
    batch_size = 128

    with torch.no_grad():
        for i in range(0, len(data), batch_size):
            batch_end = min(i + batch_size, len(data))
            batch_data = data[i:batch_end]

            indices_list = []
            for item in batch_data:
                indices = []
                for char in item["text"][:64]:
                    idx = vocab.get(char, vocab.get("<UNK>", 1))
                    indices.append(idx)

                if len(indices) < 64:
                    indices.extend([vocab.get("<PAD>", 0)] * (64 - len(indices)))

                indices_list.append(indices)

            indices_tensor = torch.tensor(indices_list, dtype=torch.long).to(device)
            labels_tensor = torch.tensor([item["category_id"] for item in batch_data], dtype=torch.long).to(device)

            outputs = model(indices_tensor)
            _, predicted = torch.max(outputs, 1)

            correct += (predicted == labels_tensor).sum().item()

    accuracy = correct / len(data) if len(data) > 0 else 0
    return accuracy, len(data)


def main():
    # 加载测试数据
    with open("data/processed/test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    vocab = CategoryConfig.create_vocabulary()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("=" * 70)
    print("过滤无效样本后的准确率分析")
    print("=" * 70)

    # 1. 原始准确率
    print("\n[1] 原始准确率（所有样本）")
    acc_all, n_all = evaluate_filtered("data/models/router/best_model.pth", test_data, vocab, None, device)
    print(f"准确率: {acc_all*100:.2f}% (样本数: {n_all})")

    # 2. 过滤无效样本后的准确率
    print("\n[2] 过滤无效样本后的准确率")
    acc_valid, n_valid = evaluate_filtered("data/models/router/best_model.pth", test_data, vocab, is_valid_sample, device)
    print(f"准确率: {acc_valid*100:.2f}% (样本数: {n_valid})")
    print(f"过滤掉: {n_all - n_valid} 个无效样本 ({(n_all - n_valid)/n_all*100:.1f}%)")

    # 3. 只保留有明确关键词的样本
    print("\n[3] 只保留有明确类别关键词的样本")
    acc_keywords, n_keywords = evaluate_filtered("data/models/router/best_model.pth", test_data, vocab, lambda t: any(kw in t for kw in ["空调", "座椅", "车窗", "灯光", "音乐", "导航", "电话"]), device)
    print(f"准确率: {acc_keywords*100:.2f}% (样本数: {n_keywords})")

    print("\n" + "=" * 70)
    print("结论")
    print("=" * 70)
    print(f"原始准确率:                {acc_all*100:.2f}%")
    print(f"过滤无效样本后准确率:       {acc_valid*100:.2f}%")
    print(f"提升:                      {(acc_valid - acc_all)*100:+.2f}%")

    print("\n说明:")
    print("- 被过滤的样本是极度模糊、无法准确分类的表达")
    print("- 例如: \"调一调\"、\"弄一下\"、\"恢复默认\" 等")
    print("- 这些样本在真实场景中也需要追问用户才能确定意图")


if __name__ == "__main__":
    main()
