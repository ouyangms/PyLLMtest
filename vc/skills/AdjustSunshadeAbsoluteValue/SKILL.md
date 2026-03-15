---
name: AdjustSunshadeAbsoluteValue
description: Adjust sunshade absolute value (控制车辆遮阳帘绝对值调节功能)
---

## 功能说明
- 控制车辆遮阳帘绝对值调节功能

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
        "action": "打开",
        "action_concrete": "true",
        "part": "幅度",
        "value": "20/100",
        "customInnerType": "nativeCommand",
        "object_raw": "遮阳帘",
        "object": "遮阳帘"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `action_concrete` | string | action_concrete | `true` |
| `part` | string | part | `幅度` |
| `value` | string | value | `20/100` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object_raw` | string | object_raw | `遮阳帘` |
| `object` | string | object | `遮阳帘` |

## 调用示例

### 示例 1
**用户输入**: 把遮阳帘关一半

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-50/100",
        "object": "遮阳帘",
        "object_raw": "遮阳帘",
        "part": "幅度",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 遮阳帘开到百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+50/100",
        "object": "遮阳帘",
        "object_raw": "遮阳帘",
        "part": "幅度",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 遮阳帘打开50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "action_concrete": "true",
        "part": "幅度",
        "value": "20/100",
        "customInnerType": "nativeCommand",
        "object_raw": "遮阳帘",
        "object": "遮阳帘"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
