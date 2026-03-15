---
name: SetVolumeBalance
description: Set volume balance to -10 (将音量平衡设置为-10)
---

## 功能说明
- 将音量平衡设置为-10

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
        "part": "音量",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "value": "负10",
        "action_concrete": "true",
        "feature": "音量平衡",
        "part_raw": "音量"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `音量` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `value` | string | value | `负10` |
| `action_concrete` | string | action_concrete | `true` |
| `feature` | string | feature | `音量平衡` |
| `part_raw` | string | part_raw | `音量` |

## 调用示例

### 示例 1
**用户输入**: 将音量平衡设置为负十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "value": "负10",
        "action_concrete": "true",
        "feature": "音量平衡",
        "part_raw": "音量"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
