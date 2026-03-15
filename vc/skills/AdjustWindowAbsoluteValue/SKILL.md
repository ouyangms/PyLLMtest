---
name: AdjustWindowAbsoluteValue
description: Adjust [location] window absolute value ([location]车窗绝对值调节)
---

## 功能说明
- 【位置】车窗绝对值调节
- 车窗开到一半/百分之二十

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
        "action_concrete": "true",
        "part": "幅度",
        "value": "20/100",
        "customInnerType": "nativeCommand",
        "object_raw": "车窗",
        "object": "车窗"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `action_concrete` | string | action_concrete | `true` |
| `part` | string | part | `幅度` |
| `value` | string | value | `20/100` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object_raw` | string | object_raw | `车窗` |
| `object` | string | object | `车窗` |

## 调用示例

### 示例 1
**用户输入**: 关20%的车窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+20/100",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "action": "关闭",
        "object": "车窗"
    }
}
```

### 示例 2
**用户输入**: 关一半车窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "50/100",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "object": "车窗",
        "action": "打开",
        "action_concrete": "true"
    }
}
```

### 示例 3
**用户输入**: 副驾车窗调低百分之三十

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+50/100",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "action": "关闭",
        "object": "车窗"
    }
}
```

### 示例 4
**用户输入**: 把主驾车窗降到一半

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "50/100",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "object": "车窗",
        "position": "主驾",
        "action_concrete": "true"
    }
}
```

### 示例 5
**用户输入**: 车窗开到一半

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "幅度",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "value": "-30/100",
        "position": "副驾",
        "object_raw": "车窗"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
