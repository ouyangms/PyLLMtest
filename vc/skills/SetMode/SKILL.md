---
name: SetMode
description: Set speed limit recognition reminder mode (控制车辆设置限速信息识别提醒模式功能)
---

## 功能说明
- 控制车辆设置限速信息识别提醒模式功能

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
        "action_concrete": "true",
        "part": "模式",
        "function": "限速信息识别提醒",
        "mode": "闪烁"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action_concrete` | string | action_concrete | `true` |
| `part` | string | part | `模式` |
| `function` | string | function | `限速信息识别提醒` |
| `mode` | string | mode | `闪烁` |

## 调用示例

### 示例 1
**用户输入**: 限速信息识别提醒设置为闪烁

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "交通标志",
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "part": "预警方式",
        "value": "闪灯声音",
        "subfunction": "限速提醒"
    }
}
```

### 示例 2
**用户输入**: 限速信息识别提醒设置为闪烁加响铃

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "part": "模式",
        "function": "限速信息识别提醒",
        "mode": "闪烁"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
