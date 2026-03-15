---
name: SetExtremeRangeMode
description: Close extreme range mode (关闭极致续航)
---

## 功能说明
- 关闭极致续航
- 关闭超级节能
- 打开极致续航
- 打开超级节能

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
        "mode": "超级节能",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "模式"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `mode` | string | mode | `超级节能` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `part` | string | part | `模式` |

## 调用示例

### 示例 1
**用户输入**: 关闭极致续航

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "超级节能",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "模式"
    }
}
```

### 示例 2
**用户输入**: 关闭超级节能

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "mode": "极致续航",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "模式"
    }
}
```

### 示例 3
**用户输入**: 打开极致续航

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "极致续航",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "模式"
    }
}
```

### 示例 4
**用户输入**: 打开超级节能

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "mode": "超级节能",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "模式"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
