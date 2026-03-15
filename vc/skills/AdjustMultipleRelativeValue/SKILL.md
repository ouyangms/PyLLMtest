---
name: AdjustMultipleRelativeValue
description: Adjust sunroof opening ([前/后/全部]天幕开大/开小一点)
---

## 功能说明
- 【前/后/全部】天幕开大/开小一点
- 【前/后/全部】遮阳帘开大/开小一点
- 对多个车窗开度进行相对调节

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
        "value": "-",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "前排"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `-` |
| `part` | string | part | `幅度` |
| `action` | string | action | `打开` |
| `object` | string | object | `车窗` |
| `position` | string | position | `前排` |

## 调用示例

### 示例 1
**用户输入**: 全车车窗开小一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "+",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "左"
    }
}
```

### 示例 2
**用户输入**: 全部天幕开小一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "+",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "all"
    }
}
```

### 示例 3
**用户输入**: 全部遮阳帘开小一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "-30/100",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "前排"
    }
}
```

### 示例 4
**用户输入**: 前天幕开大一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "+30/100",
        "part": "幅度",
        "action": "打开",
        "object": "车窗",
        "position": "左"
    }
}
```

### 示例 5
**用户输入**: 前排车窗开大30%

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "-20/100",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "position": "副驾",
        "object": "车窗",
        "action": "打开",
        "part": "幅度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
