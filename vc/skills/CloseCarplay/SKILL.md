---
name: CloseCarplay
description: Close CarPlay (控制车辆关闭carplay功能)
---

## 功能说明
- 控制车辆关闭carplay功能

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
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "屏幕",
        "app": "CARPLAY",
        "feature": "系统应用"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `关闭` |
| `object` | string | object | `屏幕` |
| `app` | string | app | `CARPLAY` |
| `feature` | string | feature | `系统应用` |

## 调用示例

### 示例 1
**用户输入**: 关闭carplay

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "屏幕",
        "app": "CARPLAY",
        "feature": "系统应用"
    }
}
```

### 示例 2
**用户输入**: 隐藏carplay

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "屏幕",
        "app": "CARPLAY",
        "feature": "系统应用"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
