---
name: DOWWarning
description: Toggle DOW warning (控制车辆DOW开门预警开关功能)
---

## 功能说明
- 控制车辆DOW开门预警开关功能

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
        "feature": "开门安全预警",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "车门"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `开门安全预警` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `object` | string | object | `车门` |

## 调用示例

### 示例 1
**用户输入**: 关闭开门安全预警开关

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "开门安全预警",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "车门"
    }
}
```

### 示例 2
**用户输入**: 关闭开门预警

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "开门安全预警",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "车门",
        "page": "开关"
    }
}
```

### 示例 3
**用户输入**: 关闭开门预警开关

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "开门安全预警",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "车门",
        "page": "开关"
    }
}
```

### 示例 4
**用户输入**: 打开开门安全预警开关

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "开门安全预警",
        "customInnerType": "nativeCommand",
        "object": "车门",
        "action": "打开",
        "page": "开关"
    }
}
```

### 示例 5
**用户输入**: 打开开门预警

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "开门安全预警",
        "customInnerType": "nativeCommand",
        "object": "车门",
        "action": "关闭",
        "page": "开关"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
