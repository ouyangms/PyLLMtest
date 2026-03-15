---
name: RestSpace
description: Rest space closed (休憩空间已关闭)
---

## 功能说明
- 休憩空间已关闭
- 好的，休憩空间已开启

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
        "action": "打开",
        "mode": "太空睡眠舱",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "part": "模式"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `mode` | string | mode | `太空睡眠舱` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `part` | string | part | `模式` |

## 调用示例

### 示例 1
**用户输入**: 主驾休憩空间开始休息

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "太空睡眠舱",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action": "打开"
    }
}
```

### 示例 2
**用户输入**: 主驾休憩空间结束休息

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "太空睡眠舱",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action": "打开"
    }
}
```

### 示例 3
**用户输入**: 休憩空间开始休息

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "mode": "太空睡眠舱",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "action": "打开"
    }
}
```

### 示例 4
**用户输入**: 休憩空间结束休息

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "太空睡眠舱",
        "part": "模式",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 停止休憩空间

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "mode": "太空睡眠舱",
        "part": "模式",
        "object": "整车",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
