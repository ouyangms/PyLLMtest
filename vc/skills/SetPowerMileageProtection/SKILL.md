---
name: SetPowerMileageProtection
description: Close power mileage protection (关闭供电里程保护)
---

## 功能说明
- 关闭供电里程保护
- 打开供电里程保护
- 把供电里程保护设置到某个目标数值

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
        "part": "里程",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "function": "供电综合里程保护",
        "value": "200KM"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `里程` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `供电综合里程保护` |
| `value` | string | value | `200KM` |

## 调用示例

### 示例 1
**用户输入**: 关闭供电里程保护

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "供电里程保护",
        "action": "打开"
    }
}
```

### 示例 2
**用户输入**: 打开供电里程保护

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "供电里程保护",
        "action": "关闭"
    }
}
```

### 示例 3
**用户输入**: 把供电综合里程保护设为200KM

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "里程",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "function": "供电综合里程保护",
        "value": "200KM"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
