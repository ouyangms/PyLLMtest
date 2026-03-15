---
name: AdjustSpeedCompensatedVolume
description: Close speed compensated volume (关闭音量随速调节)
---

## 功能说明
- 关闭音量随速调节
- 打开音量随速调节
- 调节音量随速为中度补偿模式
- 调节音量随速为弱度补偿模式
- 调节音量随速为强度补偿模式

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
        "feature": "音随车速",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "音随车速挡位"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `音随车速` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `part` | string | part | `音随车速挡位` |

## 调用示例

### 示例 1
**用户输入**: 关闭音量随速调节

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "音随车速",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "音随车速挡位"
    }
}
```

### 示例 2
**用户输入**: 打开音量随速调节

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "音随车速",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "音随车速挡位",
        "value": "mid"
    }
}
```

### 示例 3
**用户输入**: 调节音量随速为中度补偿模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "音随车速",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "音随车速挡位",
        "value": "high"
    }
}
```

### 示例 4
**用户输入**: 调节音量随速为弱度补偿模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "音随车速",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "音随车速挡位",
        "value": "low"
    }
}
```

### 示例 5
**用户输入**: 调节音量随速为强度补偿模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "音随车速",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "音随车速挡位"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
