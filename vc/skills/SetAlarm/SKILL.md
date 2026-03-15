---
name: SetAlarm
description: Set alarm offset value (控制车辆设置报警偏移值功能)
---

## 功能说明
- 控制车辆设置报警偏移值功能

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
        "subfunction": "限速偏移",
        "action_concrete": "true",
        "part": "车速",
        "function": "智慧巡航",
        "value": "1km/h",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `subfunction` | string | subfunction | `限速偏移` |
| `action_concrete` | string | action_concrete | `true` |
| `part` | string | part | `车速` |
| `function` | string | function | `智慧巡航` |
| `value` | string | value | `1km/h` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 设置限速报警偏移值为1km/h

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "限速偏移",
        "action_concrete": "true",
        "part": "车速",
        "function": "智慧巡航",
        "value": "1km/h",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
