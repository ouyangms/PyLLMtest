---
name: SunroofTiltUp
description: Tilt sunroof up (天窗翘起+一点)
---

## 功能说明
- 天窗翘起+一点
- 天窗起翘

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
        "action": "起翘",
        "object_raw": "天窗",
        "customInnerType": "nativeCommand",
        "object": "天窗"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `起翘` |
| `object_raw` | string | object_raw | `天窗` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `天窗` |

## 调用示例

### 示例 1
**用户输入**: 天窗翘起

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "天窗",
        "object": "天窗",
        "action": "起翘",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 天窗翘起一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "天窗",
        "object": "天窗",
        "action": "起翘",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 天窗起翘

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "幅度",
        "customInnerType": "nativeCommand",
        "action": "起翘",
        "value": "-",
        "object": "天窗",
        "object_raw": "天窗"
    }
}
```

### 示例 4
**用户输入**: 天窗透气

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "起翘",
        "object_raw": "天窗",
        "customInnerType": "nativeCommand",
        "object": "天窗"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
