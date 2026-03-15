---
name: AdjustWindowExtremeValue
description: Adjust [location] window extreme value ([location]车窗极值调节)
---

## 功能说明
- 【位置】车窗极值调节
- 车窗开到最大/最小

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
        "value": "max",
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
| `value` | string | value | `max` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object_raw` | string | object_raw | `车窗` |
| `object` | string | object | `车窗` |

## 调用示例

### 示例 1
**用户输入**: 副驾车窗调到最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "action_concrete": "true",
        "part": "幅度",
        "value": "min",
        "customInnerType": "nativeCommand",
        "object_raw": "车窗",
        "object": "车窗"
    }
}
```

### 示例 2
**用户输入**: 副驾车窗调到最高

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "幅度",
        "object": "车窗",
        "customInnerType": "nativeCommand",
        "value": "max",
        "position": "副驾",
        "action_concrete": "true",
        "object_raw": "车窗"
    }
}
```

### 示例 3
**用户输入**: 车窗开到最大

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "幅度",
        "object": "车窗",
        "customInnerType": "nativeCommand",
        "value": "min",
        "position": "副驾",
        "action_concrete": "true",
        "object_raw": "车窗"
    }
}
```

### 示例 4
**用户输入**: 车窗开到最小

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "action_concrete": "true",
        "part": "幅度",
        "value": "max",
        "customInnerType": "nativeCommand",
        "object_raw": "车窗",
        "object": "车窗"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
