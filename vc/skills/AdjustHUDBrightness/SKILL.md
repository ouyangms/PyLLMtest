---
name: AdjustHUDBrightness
description: Adjust HUD brightness to highest/lowest (HUD亮度调到最高/最低)
---

## 功能说明
- HUD亮度调到最高/最低
- HUD亮度调到百分之二十
- HUD亮度调高/调低+一点/百分之二十
- 关闭HUD亮度设置
- 打开HUD亮度设置
- 调节HUD亮度到XX档位

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
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "20/100",
        "object": "HUD",
        "object_raw": "HUD",
        "part_raw": "亮度"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `亮度` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `20/100` |
| `object` | string | object | `HUD` |
| `object_raw` | string | object_raw | `HUD` |
| `part_raw` | string | part_raw | `亮度` |

## 调用示例

### 示例 1
**用户输入**: HUD亮度调低一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "value": "1",
        "object": "HUD",
        "object_raw": "HUD",
        "part_raw": "亮度"
    }
}
```

### 示例 2
**用户输入**: HUD亮度调低百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "value": "+",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: HUD亮度调到最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "value": "-",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: HUD亮度调到最高

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "value": "+20/100",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: HUD亮度调到百分之二十

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "value": "-20/100",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
