---
name: RightFrontTirePressure
description: Right front tire pressure (右前胎压)
---

## 功能说明
- 右前胎压
- 右后胎压
- 左前胎压
- 左后胎压

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
        "function": "查询胎压状态",
        "action": "查看",
        "position": "左前",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `查询胎压状态` |
| `action` | string | action | `查看` |
| `position` | string | position | `左前` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 右前胎压

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "左前",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "胎压监测"
    }
}
```

### 示例 2
**用户输入**: 右前胎压正常吗

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "查询胎压状态",
        "action": "查看",
        "position": "左后",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 右后胎压

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "左后",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "胎压监测"
    }
}
```

### 示例 4
**用户输入**: 右后胎压正常吗

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "查询胎压状态",
        "action": "查看",
        "position": "右后",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 复位胎压

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "右后",
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "胎压监测"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
