---
name: ToggleLocationBreathableMode
description: Toggle [location] breathable mode ([location]透气模式开关)
---

## 功能说明
- 【位置】透气模式开关
- 打开/关闭透气模式

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
        "value": "-10/100",
        "action": "打开",
        "object": "车窗",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `幅度` |
| `value` | string | value | `-10/100` |
| `action` | string | action | `打开` |
| `object` | string | object | `车窗` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭透气模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-10/100",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "action": "打开",
        "object": "车窗"
    }
}
```

### 示例 2
**用户输入**: 再开一点左后车窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-10/100",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "action": "打开",
        "object": "车窗"
    }
}
```

### 示例 3
**用户输入**: 副驾透气模式关闭

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "车窗",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 副驾透气模式打开

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "minor",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "action": "打开",
        "object": "车窗"
    }
}
```

### 示例 5
**用户输入**: 左后车玻璃开一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-10/100",
        "customInnerType": "nativeCommand",
        "part": "幅度",
        "action": "打开",
        "object": "车窗"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
