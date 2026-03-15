---
name: Display
description: Set pure electric range display to CLTC mode (设置纯电续航里程显示为CLTC模式)
---

## 功能说明
- 设置纯电续航里程显示为CLTC模式
- 设置纯电续航里程显示为WLTC模式

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
        "action_concrete": "true",
        "function": "纯电续航里程",
        "feature": "显示",
        "part": "模式",
        "mode": "CLTC",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action_concrete` | string | action_concrete | `true` |
| `function` | string | function | `纯电续航里程` |
| `feature` | string | feature | `显示` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `CLTC` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 设置纯电续航里程显示为CLTC模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "function": "纯电续航里程",
        "feature": "显示",
        "part": "模式",
        "mode": "WLTC",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 设置纯电续航里程显示为WLTC模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "function": "纯电续航里程",
        "feature": "显示",
        "part": "模式",
        "mode": "CLTC",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
