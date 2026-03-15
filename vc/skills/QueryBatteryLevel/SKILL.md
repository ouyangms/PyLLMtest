---
name: QueryBatteryLevel
description: Query remaining fuel (查询剩余油量)
---

## 功能说明
- 查询剩余油量
- 查询剩余电量
- 查询剩余里程

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
        "action": "查看",
        "function": "查询剩余里程"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `查看` |
| `function` | string | function | `查询剩余里程` |

## 调用示例

### 示例 1
**用户输入**: 当前车剩余多少电量

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "查询剩余油量"
    }
}
```

### 示例 2
**用户输入**: 查询剩余油量

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "查询剩余电量"
    }
}
```

### 示例 3
**用户输入**: 查询剩余电量

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "查询剩余电量"
    }
}
```

### 示例 4
**用户输入**: 查询剩余里程

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "查看",
        "function": "查询剩余里程"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
