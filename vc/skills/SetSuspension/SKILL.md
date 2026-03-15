---
name: SetSuspension
description: Set suspension damping (控制车辆设定悬架阻尼功能)
---

## 功能说明
- 控制车辆设定悬架阻尼功能

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
        "action_concrete": "true",
        "object": "悬架",
        "part": "悬架阻尼",
        "value": "low",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action_concrete` | string | action_concrete | `true` |
| `object` | string | object | `悬架` |
| `part` | string | part | `悬架阻尼` |
| `value` | string | value | `low` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 将悬架阻尼设置为中

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "悬架",
        "part": "悬架阻尼",
        "value": "high",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 将悬架阻尼设置为偏软

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "悬架",
        "part": "悬架阻尼",
        "value": "min",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 将悬架阻尼设置为最硬

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "悬架",
        "part": "悬架阻尼",
        "value": "max",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 将悬架阻尼设置为最软

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "悬架",
        "part": "悬架阻尼",
        "value": "mid",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 将悬架阻尼设置为标准

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "悬架",
        "part": "悬架阻尼",
        "value": "std",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
