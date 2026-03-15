---
name: OpenFragrance
description: Open fragrance (控制车辆打开香氛功能)
---

## 功能说明
- 控制车辆打开香氛功能

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
        "object": "香氛",
        "customInnerType": "nativeCommand",
        "object_raw": "香氛",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object` | string | object | `香氛` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object_raw` | string | object_raw | `香氛` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 打开香氛

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "香氛",
        "customInnerType": "nativeCommand",
        "object_raw": "香氛",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
