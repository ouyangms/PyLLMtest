---
name: TargetCharging
description: Adjust target charging lower (将目标充电量调低一点)
---

## 功能说明
- 将目标充电量调低一点
- 将目标充电量调到50%
- 将目标充电量调到X%
- 将目标充电量调到最低
- 将目标充电量调到最高
- 将目标充电量调高30%
- 将目标充电量调高一点

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
        "part_raw": "目标充电量",
        "part": "SOC电量目标",
        "feature": "充电",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action_concrete": "true",
        "value": "50/100"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part_raw` | string | part_raw | `目标充电量` |
| `part` | string | part | `SOC电量目标` |
| `feature` | string | feature | `充电` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `action_concrete` | string | action_concrete | `true` |
| `value` | string | value | `50/100` |

## 调用示例

### 示例 1
**用户输入**: 充电到20%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "目标充电量",
        "part": "SOC电量目标",
        "feature": "充电",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action_concrete": "true",
        "value": "min"
    }
}
```

### 示例 2
**用户输入**: 将目标充电量调低一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "SOC电量目标",
        "feature": "充电",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action_concrete": "true",
        "value": "max"
    }
}
```

### 示例 3
**用户输入**: 将目标充电量调到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part_raw": "目标充电量",
        "part": "SOC电量目标",
        "feature": "充电",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "value": "+30/100"
    }
}
```

### 示例 4
**用户输入**: 将目标充电量调到最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "充电限值",
        "part_raw": "充电限制",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action_concrete": "true",
        "value": "20/100"
    }
}
```

### 示例 5
**用户输入**: 将目标充电量调到最高

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "充电限值",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action_concrete": "true",
        "value": "20/100"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
