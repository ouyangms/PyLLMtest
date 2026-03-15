---
name: SetSuspensionHeight
description: Set suspension height (控制车辆设定悬架高度功能)
---

## 功能说明
- 控制车辆设定悬架高度功能

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
        "object_raw": "悬架",
        "action_concrete": "true",
        "part_raw": "高度",
        "object": "悬架",
        "part": "高度",
        "value": "std",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object_raw` | string | object_raw | `悬架` |
| `action_concrete` | string | action_concrete | `true` |
| `part_raw` | string | part_raw | `高度` |
| `object` | string | object | `悬架` |
| `part` | string | part | `高度` |
| `value` | string | value | `std` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 将悬架高度设置为中

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "action_concrete": "true",
        "part_raw": "高度",
        "object": "悬架",
        "part": "高度",
        "value": "min",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 将悬架高度设置为最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "part_raw": "高度",
        "object": "悬架",
        "part": "高度",
        "value": "low",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 将悬架高度设置为最高

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "action_concrete": "true",
        "part_raw": "高度",
        "object": "悬架",
        "part": "高度",
        "value": "mid",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 将悬架高度设置为正常

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "悬架",
        "part": "高度",
        "value": "high",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 将悬架高度设置低

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "悬架",
        "action_concrete": "true",
        "part_raw": "高度",
        "object": "悬架",
        "part": "高度",
        "value": "max",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
