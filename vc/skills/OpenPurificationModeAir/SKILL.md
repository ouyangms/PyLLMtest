---
name: OpenPurificationModeAir
description: Open air purification mode (控制车辆打开空气净化模式功能)
---

## 功能说明
- 控制车辆打开空气净化模式功能

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
        "object_raw": "空气净化模式",
        "object": "空气净化器",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object_raw` | string | object_raw | `空气净化模式` |
| `object` | string | object | `空气净化器` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 启用空气净化

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "空气净化",
        "object": "空调",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开空气净化

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "负离子",
        "object": "空调",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 打开空气净化模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "空气净化",
        "object": "空调",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开负离子

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "通风",
        "object": "空气净化器",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 调节空气净化到增强模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "通风",
        "object": "空气净化器",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
