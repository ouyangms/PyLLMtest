---
name: SetSeat
description: Set passenger seat easy entry to off/exit only/exit+entry (副驾座椅方便进出设为关闭/仅离车/离车+上车)
---

## 功能说明
- 副驾座椅方便进出设为关闭/仅离车/离车+上车

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
        "action": "关闭",
        "position": "副驾",
        "function": "方便进出",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "object": "座椅"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `position` | string | position | `副驾` |
| `function` | string | function | `方便进出` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `座椅` |

## 调用示例

### 示例 1
**用户输入**: 副驾座椅方便进出设为仅离车

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "position": "副驾",
        "function": "方便进出",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "object": "座椅"
    }
}
```

### 示例 2
**用户输入**: 副驾座椅方便进出设为关闭

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "副驾",
        "function": "方便进出",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "object": "座椅",
        "value": "离车"
    }
}
```

### 示例 3
**用户输入**: 副驾座椅方便进出设为打开

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "副驾",
        "function": "方便进出",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "object": "座椅",
        "value": "离车和上车"
    }
}
```

### 示例 4
**用户输入**: 副驾座椅方便进出设为离车加上车

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "position": "副驾",
        "function": "方便进出",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "object": "座椅"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
