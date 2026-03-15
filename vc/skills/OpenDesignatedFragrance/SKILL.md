---
name: OpenDesignatedFragrance
description: Open designated fragrance (控制车辆打开指定香氛功能)
---

## 功能说明
- 控制车辆打开指定香氛功能

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
        "object": "香氛",
        "part": "香味",
        "value": "自由的探戈",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `香氛` |
| `part` | string | part | `香味` |
| `value` | string | value | `自由的探戈` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 打开哥德堡的海风香氛

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "香氛",
        "part": "香味",
        "value": "哥德堡的海风",
        "action": "打开"
    }
}
```

### 示例 2
**用户输入**: 打开曼妙的春日香氛

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "香氛",
        "part": "香味",
        "value": "曼妙的春日",
        "action": "打开"
    }
}
```

### 示例 3
**用户输入**: 打开自由的探戈香氛

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "香氛",
        "part": "香味",
        "value": "自由的探戈",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
