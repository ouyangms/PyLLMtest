---
name: NegativeIonOffWarnIfWindowsNotClosed
description: Negative ion on from off, warn if windows not closed (负离子从关闭到打开时，如果有车窗未关闭，则会弹窗提醒)
---

## 功能说明
- 负离子从关闭到打开时，如果有车窗未关闭，则会弹窗提醒

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
        "function": "负离子关窗提醒",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `负离子关窗提醒` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 打开负离子关窗提醒

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "负离子关窗提醒",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
