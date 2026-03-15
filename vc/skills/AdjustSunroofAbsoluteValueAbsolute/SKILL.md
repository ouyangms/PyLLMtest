---
name: AdjustSunroofAbsoluteValueAbsolute
description: Adjust sunroof absolute value (天窗绝对值调节)
---

## 功能说明
- 天窗绝对值调节

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
        "part": "幅度",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "value": "+30/100",
        "object": "天窗",
        "object_raw": "天窗"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `幅度` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `关闭` |
| `value` | string | value | `+30/100` |
| `object` | string | object | `天窗` |
| `object_raw` | string | object_raw | `天窗` |

## 调用示例

### 示例 1
**用户输入**: 天窗关百分之三十

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+20/100",
        "object": "天窗",
        "object_raw": "天窗",
        "part": "幅度",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 天窗开百分之三十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "幅度",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "value": "-30/100",
        "object": "天窗",
        "object_raw": "天窗"
    }
}
```

### 示例 3
**用户输入**: 天窗打开一半

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-50/100",
        "object": "天窗",
        "object_raw": "天窗",
        "part": "幅度",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 把天窗关一半

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-50/100",
        "object": "天窗",
        "object_raw": "天窗",
        "part": "幅度",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 把天窗关闭20%

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+50/100",
        "object": "天窗",
        "object_raw": "天窗",
        "part": "幅度",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
