---
name: SetWiperControl
description: Default front wiper when direction not specified (用户指令中未指定方位时，默认前雨刮)
---

## 功能说明
- 用户指令中未指定方位时，默认前雨刮

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
        "action": "打开",
        "object": "雨刷"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `object` | string | object | `雨刷` |

## 调用示例

### 示例 1
**用户输入**: 关闭雨刮

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object": "雨刷",
        "object_raw": "雨刮",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭雨刷

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "object": "雨刷"
    }
}
```

### 示例 3
**用户输入**: 打开自动雨刮

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "雨刷",
        "object_raw": "雨刮",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开雨刮

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "customInnerType": "nativeCommand",
        "object_raw": "雨刮",
        "mode": "自动",
        "action": "打开",
        "object": "雨刷"
    }
}
```

### 示例 5
**用户输入**: 打开雨刷

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "雨刷"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
