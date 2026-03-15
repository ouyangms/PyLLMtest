---
name: ButtonBrightness
description: Close instrument auto brightness switch (关闭仪表自动切换亮暗)
---

## 功能说明
- 关闭仪表自动切换亮暗
- 打开仪表自动切换亮暗
- 整车背光亮度调大1
- 整车背光亮度调大一点
- 整车背光亮度调大百分之十
- 整车背光亮度调节至1
- 整车背光亮度调节至最大
- 整车背光亮度调节至百分之十

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
        "part": "亮度",
        "part_raw": "亮度",
        "object_raw": "整车",
        "position": "all",
        "customInnerType": "nativeCommand",
        "value": "1",
        "action_concrete": "true",
        "object": "整车"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `亮度` |
| `part_raw` | string | part_raw | `亮度` |
| `object_raw` | string | object_raw | `整车` |
| `position` | string | position | `all` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `1` |
| `action_concrete` | string | action_concrete | `true` |
| `object` | string | object | `整车` |

## 调用示例

### 示例 1
**用户输入**: 关闭仪表自动切换亮暗

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "object_raw": "整车",
        "position": "all",
        "customInnerType": "nativeCommand",
        "value": "max",
        "action_concrete": "true",
        "object": "整车"
    }
}
```

### 示例 2
**用户输入**: 打开仪表自动切换亮暗

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "object_raw": "整车",
        "position": "all",
        "customInnerType": "nativeCommand",
        "value": "10/100",
        "action_concrete": "true",
        "object": "整车"
    }
}
```

### 示例 3
**用户输入**: 整车背光亮度调大1

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "object_raw": "整车",
        "customInnerType": "nativeCommand",
        "value": "+1",
        "position": "all",
        "object": "整车"
    }
}
```

### 示例 4
**用户输入**: 整车背光亮度调大一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "object_raw": "整车",
        "customInnerType": "nativeCommand",
        "value": "+10/100",
        "position": "all",
        "object": "整车"
    }
}
```

### 示例 5
**用户输入**: 整车背光亮度调大百分之十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "object_raw": "整车",
        "customInnerType": "nativeCommand",
        "value": "+",
        "position": "all",
        "object": "整车"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
