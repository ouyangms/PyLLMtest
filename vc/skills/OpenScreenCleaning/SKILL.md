---
name: OpenScreenCleaning
description: Toggle screen cleaning (打开/关闭屏幕清洁)
---

## 功能说明
- 打开/关闭屏幕清洁

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
        "object_raw": "屏幕",
        "object": "屏幕",
        "mode": "清洁",
        "part": "模式",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `屏幕` |
| `object` | string | object | `屏幕` |
| `mode` | string | mode | `清洁` |
| `part` | string | part | `模式` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭二排屏幕清洁

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "customInnerType": "nativeCommand",
        "mode": "清洁",
        "action": "打开",
        "object": "屏幕"
    }
}
```

### 示例 2
**用户输入**: 关闭前排屏幕清洁

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "屏幕",
        "object": "屏幕",
        "mode": "清洁",
        "part": "模式",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭屏幕清洁

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "position": "前排",
        "object_raw": "屏幕",
        "object": "屏幕",
        "mode": "清洁",
        "part": "模式",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开二排屏幕清洁

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "position": "前排",
        "object_raw": "屏幕",
        "object": "屏幕",
        "mode": "清洁",
        "part": "模式",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 打开前排屏幕清洁

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "position": "第二排",
        "object_raw": "屏幕",
        "object": "屏幕",
        "mode": "清洁",
        "part": "模式",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
