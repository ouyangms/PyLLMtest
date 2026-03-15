---
name: SetPrivacyMode
description: Close privacy mode settings (关闭隐私模式设置)
---

## 功能说明
- 关闭隐私模式设置
- 打开隐私模式设置

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
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page": "设置",
        "part": "模式",
        "mode": "隐私"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `page` | string | page | `设置` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `隐私` |

## 调用示例

### 示例 1
**用户输入**: 关闭隐私模式设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "page": "设置",
        "part": "模式",
        "mode": "隐私"
    }
}
```

### 示例 2
**用户输入**: 打开隐私模式设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page": "设置",
        "part": "模式",
        "mode": "隐私"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
