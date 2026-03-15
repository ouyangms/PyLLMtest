---
name: SeatRow2
description: Restore both seats to 0 degrees (两侧座椅同时恢复至0度)
---

## 功能说明
- 两侧座椅同时恢复至0度
- 两侧座椅同时旋转至180度
- 将二排左/二排右座椅旋转角度设为特定值
- 将二排座椅旋转角度设为0度，恢复初始位置
- 将二排座椅旋转角度设为180度，形成跟三排对座
- 座椅旋转调节至0度
- 座椅旋转调节至180度
- 座椅旋转调节至90度

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
        "object": "座椅",
        "action": "转动",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "0",
        "part": "角度"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object` | string | object | `座椅` |
| `action` | string | action | `转动` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `0` |
| `part` | string | part | `角度` |

## 调用示例

### 示例 1
**用户输入**: 二排右座椅旋转角度设为90度

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "座椅",
        "action": "转动",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "90",
        "part": "角度"
    }
}
```

### 示例 2
**用户输入**: 二排左座椅旋转角度设为0度

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "座椅",
        "action": "转动",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "180",
        "part": "角度"
    }
}
```

### 示例 3
**用户输入**: 二排左座椅旋转角度设为180度

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "座椅",
        "action": "转动",
        "customInnerType": "nativeCommand",
        "value": "180",
        "part": "角度",
        "position": "第二排",
        "part_raw": "旋转"
    }
}
```

### 示例 4
**用户输入**: 二排座椅恢复至0度

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "座椅",
        "action": "还原",
        "customInnerType": "nativeCommand",
        "part": "角度",
        "position": "第二排",
        "value": "0"
    }
}
```

### 示例 5
**用户输入**: 二排座椅旋转至180度

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "座椅",
        "action": "转动",
        "customInnerType": "nativeCommand",
        "value": "0",
        "part": "角度",
        "position": "第二排左侧",
        "part_raw": "角度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
