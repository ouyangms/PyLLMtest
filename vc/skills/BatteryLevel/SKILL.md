---
name: BatteryLevel
description: Toggle low battery auto start generator (开启后，低电量时燃油发电机启动发动机)
---

## 功能说明
- 开启后，低电量时燃油发电机启动发动机

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
        "action": "打开",
        "function": "低电量启动发动机",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `function` | string | function | `低电量启动发动机` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭低电量启机

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "function": "低电量启动发动机",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开低电量启机

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "function": "低电量启动发动机",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
