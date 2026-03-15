---
name: SetChargingReservationEndTime3Oclock
description: Set charging reservation end time to 3 o'clock (设置预约充电的结束时间为3点)
---

## 功能说明
- 设置预约充电的结束时间为3点
- 设置预约充电结束时间

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
        "part": "结束时间",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "function": "预约充电",
        "value": "03:00:00"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `结束时间` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `预约充电` |
| `value` | string | value | `03:00:00` |

## 调用示例

### 示例 1
**用户输入**: 设置预约充电的结束时间为3点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "预约充电",
        "action": "打开",
        "page": "设置"
    }
}
```

### 示例 2
**用户输入**: 设置预约充电结束时间

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "结束时间",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "function": "预约充电",
        "value": "03:00:00"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
