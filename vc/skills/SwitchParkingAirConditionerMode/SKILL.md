---
name: SwitchParkingAirConditionerMode
description: Switch parking air conditioner mode (控制车辆驻车空调模式切换功能)
---

## 功能说明
- 控制车辆驻车空调模式切换功能

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
        "function": "驻车",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "object": "空调",
        "mode": "通风",
        "part_raw": "模式"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `驻车` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `模式` |
| `object` | string | object | `空调` |
| `mode` | string | mode | `通风` |
| `part_raw` | string | part_raw | `模式` |

## 调用示例

### 示例 1
**用户输入**: 打开驻车空调通风

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "驻车",
        "action_concrete": "true",
        "part_raw": "模式",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "object": "空调",
        "mode": "智能",
        "object_raw": "空调"
    }
}
```

### 示例 2
**用户输入**: 把驻车空调切换到智能模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "驻车",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "object": "空调",
        "mode": "智能",
        "object_raw": "空调"
    }
}
```

### 示例 3
**用户输入**: 把驻车空调切换到通风模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "驻车",
        "action_concrete": "true",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "feature": "通风",
        "object_raw": "空调"
    }
}
```

### 示例 4
**用户输入**: 把驻车空调调到智能

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "驻车",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part": "模式",
        "object": "空调",
        "mode": "通风",
        "part_raw": "模式"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
