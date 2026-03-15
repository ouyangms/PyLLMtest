---
name: TrunkRearHeight
description: Set trunk opening height to 60%/70%/80%90%100% (后备箱开启高度设置为 60%/70%/80%90%100%)
---

## 功能说明
- 后备箱开启高度设置为 60%/70%/80%90%100%

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
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "60/100",
        "object": "后备箱",
        "object_raw": "后备箱",
        "part_raw": "高度"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `高度` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `60/100` |
| `object` | string | object | `后备箱` |
| `object_raw` | string | object_raw | `后备箱` |
| `part_raw` | string | part_raw | `高度` |

## 调用示例

### 示例 1
**用户输入**: 后备箱开启高度设置为100%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "70/100",
        "object": "后备箱",
        "object_raw": "后备箱",
        "part_raw": "高度"
    }
}
```

### 示例 2
**用户输入**: 后备箱开启高度设置为60%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "80/100",
        "object": "后备箱",
        "object_raw": "后备箱",
        "part_raw": "高度"
    }
}
```

### 示例 3
**用户输入**: 后备箱开启高度设置为70%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "90/100",
        "object": "后备箱",
        "object_raw": "后备箱",
        "part_raw": "高度"
    }
}
```

### 示例 4
**用户输入**: 后备箱开启高度设置为80%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "100/100",
        "object": "后备箱",
        "object_raw": "后备箱",
        "part_raw": "高度"
    }
}
```

### 示例 5
**用户输入**: 后备箱开启高度设置为90%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "高度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "60/100",
        "object": "后备箱",
        "object_raw": "后备箱",
        "part_raw": "高度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
