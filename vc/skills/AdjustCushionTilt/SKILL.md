---
name: AdjustCushionTilt
description: Adjust cushion tilt to highest/lowest (坐垫倾斜角度调到最高/最低)
---

## 功能说明
- 坐垫倾斜角度调到最高/最低
- 坐垫角度调到70度
- 坐垫角度调高/调低+70度

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
        "part": "角度",
        "part_raw": "角度",
        "value": "+70",
        "object": "坐垫",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `角度` |
| `part_raw` | string | part_raw | `角度` |
| `value` | string | value | `+70` |
| `object` | string | object | `坐垫` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 坐垫倾斜角度调到最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "part_raw": "角度",
        "value": "-70",
        "object": "坐垫",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 坐垫倾斜角度调到最高

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "坐垫",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "70",
        "part": "角度",
        "part_raw": "角度"
    }
}
```

### 示例 3
**用户输入**: 坐垫角度调低70度

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "坐垫",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "max",
        "part": "角度",
        "part_raw": "倾斜角度"
    }
}
```

### 示例 4
**用户输入**: 坐垫角度调到70度

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "坐垫",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "min",
        "part": "角度",
        "part_raw": "倾斜角度"
    }
}
```

### 示例 5
**用户输入**: 坐垫角度调高70度

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "角度",
        "part_raw": "角度",
        "value": "+70",
        "object": "坐垫",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
