---
name: OpenAutoAirConditionerAntiFog
description: Auto activate anti-fog when fog detected, keep AC in AUTO (检测到车内可能起雾，自动激活防起雾模式，空调保持在AUTO状态)
---

## 功能说明
- 检测到车内可能起雾，自动激活防起雾模式，空调保持在AUTO状态

## 调用逻辑
1. **意图解析**：系统自动识别用户指令中的操作意图和参数
2. **参数提取**：从用户自然语言中提取相关参数
3. **工具调用**：调用车辆控制工具执行相应操作

## 参数规范
用户输入自然语言指令后，LLM 需要提取参数并输出以下格式：

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "自动防起雾",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "空调"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `自动防起雾` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `object` | string | object | `空调` |

## 调用示例

### 示例 1
**用户输入**: 打开空调自动防起雾

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "自动防起雾",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "空调"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
