---
name: SetEnergyRecoveryAuto
description: Set energy recovery to auto (动力回收设置为自动)
---

## 功能说明
- 动力回收设置为自动
- 动力回收设置为高
- 能量回收设置为中
- 能量回收设置为低

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
        "part": "能量回收等级",
        "object": "整车",
        "part_raw": "能量回收",
        "customInnerType": "nativeCommand",
        "value": "low",
        "action_concrete": "true"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `能量回收等级` |
| `object` | string | object | `整车` |
| `part_raw` | string | part_raw | `能量回收` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `low` |
| `action_concrete` | string | action_concrete | `true` |

## 调用示例

### 示例 1
**用户输入**: 动力回收切换为自动

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "能量回收等级",
        "object": "整车",
        "part_raw": "能量回收",
        "customInnerType": "nativeCommand",
        "value": "mid",
        "action_concrete": "true"
    }
}
```

### 示例 2
**用户输入**: 动力回收切换为高

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "能量回收等级",
        "object": "整车",
        "part_raw": "动力回收",
        "customInnerType": "nativeCommand",
        "value": "high",
        "action_concrete": "true"
    }
}
```

### 示例 3
**用户输入**: 动能回收调高一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+",
        "part_raw": "动能回收",
        "part": "能量回收等级",
        "customInnerType": "nativeCommand",
        "object": "整车"
    }
}
```

### 示例 4
**用户输入**: 能量回收切换为中

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+",
        "part_raw": "能量回收",
        "part": "能量回收等级",
        "customInnerType": "nativeCommand",
        "object": "整车"
    }
}
```

### 示例 5
**用户输入**: 能量回收切换为低

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "能量回收等级",
        "mode": "自动",
        "part_raw": "动力回收",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action_concrete": "true"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
