---
name: QuerySeatMassage
description: Query seat massage status (查询座椅按摩开关状态)
---

## 功能说明
- 查询座椅按摩开关状态
- 查询座椅按摩挡位

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
        "action": "查看",
        "object": "座椅",
        "function": "查询座椅按摩开关状态",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `查看` |
| `object` | string | object | `座椅` |
| `function` | string | function | `查询座椅按摩开关状态` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 座椅按摩关了吗

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "查看",
        "object": "座椅",
        "function": "查询座椅按摩开关状态",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 座椅按摩开了吗

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "查看",
        "object": "座椅",
        "function": "查询座椅按摩挡位",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 查询座椅按摩挡位

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "查看",
        "object": "座椅",
        "function": "查询座椅按摩开关状态",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
