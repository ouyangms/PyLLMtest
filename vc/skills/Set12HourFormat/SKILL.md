---
name: Set12HourFormat
description: 12-hour format (12小时制)
---

## 功能说明
- 12小时制
- 24小时制
- 续航里程切换为CLTC
- 续航里程切换为WLTC

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
        "action": "切换",
        "function": "续航里程",
        "part": "模式",
        "mode": "CLTC",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action_concrete` | string | action_concrete | `true` |
| `action` | string | action | `切换` |
| `function` | string | function | `续航里程` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `CLTC` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 时间设为12小时制

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "action": "切换",
        "function": "续航里程",
        "part": "模式",
        "mode": "WLTC",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 时间设为24小时制

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "时间格式",
        "customInnerType": "nativeCommand",
        "value": "12小时制",
        "action_concrete": "true",
        "object": "屏幕"
    }
}
```

### 示例 3
**用户输入**: 续航里程切换为CLTC

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "时间格式",
        "customInnerType": "nativeCommand",
        "value": "24小时制",
        "action_concrete": "true",
        "object": "屏幕"
    }
}
```

### 示例 4
**用户输入**: 续航里程切换为WLTC

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "action": "切换",
        "function": "续航里程",
        "part": "模式",
        "mode": "CLTC",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
