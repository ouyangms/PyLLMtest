---
name: OpenCinemaMode
description: Cinema mode enabled (好的，影院模式已开启)
---

## 功能说明
- 好的，影院模式已开启

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
        "mode": "银河影院",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `mode` | string | mode | `银河影院` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 启动影院模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "mode": "银河影院",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "模式"
    }
}
```

### 示例 2
**用户输入**: 开启影院模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "银河影院",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action": "打开"
    }
}
```

### 示例 3
**用户输入**: 打开影院模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "part": "模式",
        "customInnerType": "nativeCommand",
        "mode": "银河影院",
        "object": "整车"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
