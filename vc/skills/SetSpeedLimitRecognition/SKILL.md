---
name: SetSpeedLimitRecognition
description: Toggle speed limit recognition (控制车辆限速信息识别开关功能)
---

## 功能说明
- 控制车辆限速信息识别开关功能

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
        "function": "限速信息识别提醒",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `限速信息识别提醒` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭限速信息识别提醒

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "限速信息识别提醒",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开限速信息识别提醒

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "限速信息识别提醒",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
