---
name: PedalPedalWelcomeElectric
description: Toggle welcome pedal|electric pedal (迎宾踏板|电动踏板开关)
---

## 功能说明
- 迎宾踏板|电动踏板开关

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
        "action": "打开",
        "feature": "迎宾",
        "customInnerType": "nativeCommand",
        "object": "电动踏板"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `feature` | string | feature | `迎宾` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `电动踏板` |

## 调用示例

### 示例 1
**用户输入**: 关闭电动踏板

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "电动踏板",
        "customInnerType": "nativeCommand",
        "object": "电动踏板"
    }
}
```

### 示例 2
**用户输入**: 打开电动侧踏

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "电动侧踏",
        "customInnerType": "nativeCommand",
        "object": "电动侧踏"
    }
}
```

### 示例 3
**用户输入**: 打开迎宾踏板

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "feature": "迎宾",
        "customInnerType": "nativeCommand",
        "object": "电动踏板"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
