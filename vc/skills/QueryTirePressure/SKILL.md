---
name: QueryTirePressure
description: Query tire pressure (控制车辆胎压查询功能)
---

## 功能说明
- 控制车辆胎压查询功能

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
        "function": "胎压监测",
        "customInnerType": "nativeCommand",
        "action": "查看"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `胎压监测` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `查看` |

## 调用示例

### 示例 1
**用户输入**: 关闭胎压监测

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "function": "胎压监测"
    }
}
```

### 示例 2
**用户输入**: 关闭胎压预警

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "function": "胎压监测"
    }
}
```

### 示例 3
**用户输入**: 哪个轮胎漏气

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "function": "胎压监测"
    }
}
```

### 示例 4
**用户输入**: 哪个轮胎胎压异常

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "function": "胎压监测"
    }
}
```

### 示例 5
**用户输入**: 当前胎压查询

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "查询轮胎状态"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
