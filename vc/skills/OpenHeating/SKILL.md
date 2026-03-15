---
name: OpenHeating
description: Open [zone] rapid heating (控制车辆打开[zone]极速升温功能)
---

## 功能说明
- 控制车辆打开【音区】极速升温功能

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
        "mode": "强力制热",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "打开"
    }
}
```

### 特殊参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `zone` | string | 音区参数（主驾音区/副驾音区/全车/一排/二排/三排） | `主驾音区` |

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `mode` | string | mode | `强力制热` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `空调` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 打开极速升温

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "强力制热",
        "customInnerType": "nativeCommand",
        "object": "空调",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
