---
name: SwitchWarning
description: Switch lane change warning mode (控制车辆变道安全预警方式切换功能)
---

## 功能说明
- 控制车辆变道安全预警方式切换功能

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
        "subfunction": "变道安全预警",
        "function": "智慧巡航",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "action_concrete": "true"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `subfunction` | string | subfunction | `变道安全预警` |
| `function` | string | function | `智慧巡航` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `关闭` |
| `action_concrete` | string | action_concrete | `true` |

## 调用示例

### 示例 1
**用户输入**: 变道安全预警调整成声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "变道安全预警",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "智慧巡航",
        "value": "指示灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 变道安全预警调整成指示灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "变道安全预警",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "智慧巡航",
        "value": "指示灯声音",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 变道安全预警调整成指示灯声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "变道安全预警",
        "action_concrete": "true",
        "part": "预警方式",
        "function": "智慧巡航",
        "value": "声音",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 变道安全预警调整成无预警

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "变道安全预警",
        "function": "智慧巡航",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
