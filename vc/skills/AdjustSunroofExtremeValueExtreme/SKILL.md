---
name: AdjustSunroofExtremeValueExtreme
description: Adjust sunroof extreme value (天窗极值调节)
---

## 功能说明
- 天窗极值调节

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
        "part": "幅度",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "value": "max",
        "object_raw": "天窗",
        "action_concrete": "true",
        "object": "天窗"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `幅度` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `max` |
| `object_raw` | string | object_raw | `天窗` |
| `action_concrete` | string | action_concrete | `true` |
| `object` | string | object | `天窗` |

## 调用示例

### 示例 1
**用户输入**: 天窗开到最大

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "幅度",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "value": "min",
        "object_raw": "天窗",
        "action_concrete": "true",
        "object": "天窗"
    }
}
```

### 示例 2
**用户输入**: 天窗开到最小

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "幅度",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "value": "max",
        "object_raw": "天窗",
        "action_concrete": "true",
        "object": "天窗"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
