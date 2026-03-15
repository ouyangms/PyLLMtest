---
name: CurrentAirConditionerTemperature
description: Query current air conditioner temperature (目前空调多少度/车里多少度)
---

## 功能说明
- 目前空调多少度/车里多少度

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
        "function": "查询空调温度",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "object": "空调"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `查询空调温度` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `查看` |
| `object` | string | object | `空调` |

## 调用示例

### 示例 1
**用户输入**: 当前空调温度多少度

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "查看",
        "function": "查询空调温度"
    }
}
```

### 示例 2
**用户输入**: 目前空调多少度

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "查看",
        "function": "查询空调温度"
    }
}
```

### 示例 3
**用户输入**: 车里多少度

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "查询空调温度",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "object": "空调"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
