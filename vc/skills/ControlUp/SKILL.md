---
name: ControlUp
description: Toggle leave vehicle lock (打开/关闭离车上锁)
---

## 功能说明
- 打开/关闭离车上锁

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
        "feature": "离车闭锁",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "门锁"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `离车闭锁` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `门锁` |

## 调用示例

### 示例 1
**用户输入**: 关闭离车上锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "离车闭锁",
        "object": "门锁",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭离车闭锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "离车闭锁",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "门锁"
    }
}
```

### 示例 3
**用户输入**: 打开离车上锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "离车闭锁",
        "object": "门锁",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 打开离车闭锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "离车闭锁",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "门锁"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
