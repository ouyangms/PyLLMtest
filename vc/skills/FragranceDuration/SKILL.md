---
name: FragranceDuration
description: Set fragrance duration to 30/60/90/120 minutes (控制车辆香氛开启时长设为30/60/90/120分钟功能)
---

## 功能说明
- 控制车辆香氛开启时长设为30/60/90/120分钟功能

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
        "customInnerType": "nativeCommand",
        "object": "香氛",
        "part": "时长",
        "value": "00:30:00"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `香氛` |
| `part` | string | part | `时长` |
| `value` | string | value | `00:30:00` |

## 调用示例

### 示例 1
**用户输入**: 香氛开启时长设置为30分钟

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "object": "香氛",
        "part": "时长",
        "value": "00:30:00"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
