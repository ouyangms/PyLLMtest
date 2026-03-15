---
name: RearAngle
description: Set rear wheel steering angle to off/small/medium/full (后轮转向角度利用幅度切换关/小幅/中幅/全幅)
---

## 功能说明
- 后轮转向角度利用幅度切换关/小幅/中幅/全幅

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
        "action": "关闭",
        "function": "后轮转向角度利用",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "object": "整车"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `function` | string | function | `后轮转向角度利用` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `幅度` |
| `object` | string | object | `整车` |

## 调用示例

### 示例 1
**用户输入**: 后轮转向角度利用幅度切换中幅

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "function": "后轮转向角度利用",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "value": "小幅",
        "object": "整车"
    }
}
```

### 示例 2
**用户输入**: 后轮转向角度利用幅度切换全幅

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "function": "后轮转向角度利用",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "value": "中幅",
        "object": "整车"
    }
}
```

### 示例 3
**用户输入**: 后轮转向角度利用幅度切换关

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "function": "后轮转向角度利用",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "value": "全幅",
        "object": "整车"
    }
}
```

### 示例 4
**用户输入**: 后轮转向角度利用幅度切换小幅

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "function": "后轮转向角度利用",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "object": "整车"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
