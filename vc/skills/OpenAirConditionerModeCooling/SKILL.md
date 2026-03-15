---
name: OpenAirConditionerModeCooling
description: Open air conditioner cooling mode (控制车辆打开空调制冷模式功能)
---

## 功能说明
- 控制车辆打开空调制冷模式功能

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
        "part": "模式",
        "mode": "制冷",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "打开",
        "part_raw": "模式"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `mode` | string | mode | `制冷` |
| `object_raw` | string | object_raw | `空调` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `空调` |
| `action` | string | action | `打开` |
| `part_raw` | string | part_raw | `模式` |

## 调用示例

### 示例 1
**用户输入**: 打开AC

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "空调",
        "part_raw": "模式",
        "customInnerType": "nativeCommand",
        "mode": "制冷",
        "object_raw": "空调",
        "part": "模式"
    }
}
```

### 示例 2
**用户输入**: 打开空调制冷

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "object": "空调",
        "part_raw": "模式",
        "customInnerType": "nativeCommand",
        "mode": "制冷",
        "object_raw": "空调",
        "part": "模式"
    }
}
```

### 示例 3
**用户输入**: 打开空调制冷模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "空调",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "mode": "制冷",
        "object_raw": "空调",
        "part": "模式"
    }
}
```

### 示例 4
**用户输入**: 把空调转到制冷模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "空调",
        "customInnerType": "nativeCommand",
        "mode": "制冷",
        "action": "打开",
        "part": "模式"
    }
}
```

### 示例 5
**用户输入**: 换到空调制冷模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "制冷",
        "object_raw": "空调",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "打开",
        "part_raw": "模式"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
