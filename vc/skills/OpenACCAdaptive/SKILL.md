---
name: OpenACCAdaptive
description: Toggle adaptive cruise ACC (控制车辆打开/关闭自适应巡航ACC功能)
---

## 功能说明
- 控制车辆打开/关闭自适应巡航ACC功能

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
        "function": "自适应巡航",
        "action": "关闭"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `自适应巡航` |
| `action` | string | action | `关闭` |

## 调用示例

### 示例 1
**用户输入**: 关闭ACC

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "自适应巡航",
        "action": "关闭"
    }
}
```

### 示例 2
**用户输入**: 关闭自适应巡航辅助

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "自适应巡航",
        "action": "打开"
    }
}
```

### 示例 3
**用户输入**: 切换到自适应巡航ACC

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "function": "自适应巡航"
    }
}
```

### 示例 4
**用户输入**: 打开ACC

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action_concrete": "true",
        "action": "切换",
        "function": "自适应巡航"
    }
}
```

### 示例 5
**用户输入**: 打开自适应巡航ACC

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "自适应巡航",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
