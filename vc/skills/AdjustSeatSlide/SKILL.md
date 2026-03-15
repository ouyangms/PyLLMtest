---
name: AdjustSeatSlide
description: Adjust [前排/后排/左侧/右侧/全车] seat forward/backward ([前排/后排/左侧/右侧/全车]座椅往前/往后一点)
---

## 功能说明
- 【前排/后排/左侧/右侧/全车】座椅往前/往后一点
- 【前排/后排/左侧/右侧/全车】座椅往前/往后移到50%
- 【前排/后排/左侧/右侧/全车】座椅移到最前/最后
- 座椅往前/往后移+一点/百分之二十
- 座椅往前/往后移百分之十
- 座椅移到中间/百分之二十
- 座椅移到最前/最后

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
        "value": "前",
        "part": "方向",
        "object": "座椅"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `前` |
| `part` | string | part | `方向` |
| `object` | string | object | `座椅` |

## 调用示例

### 示例 1
**用户输入**: 全车座椅往后一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "value": "后",
        "part": "方向",
        "object": "座椅"
    }
}
```

### 示例 2
**用户输入**: 全车座椅往后移到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "后",
        "customInnerType": "nativeCommand",
        "position": "副驾",
        "object_raw": "座椅",
        "object": "座椅",
        "part": "方向"
    }
}
```

### 示例 3
**用户输入**: 全车座椅移到最后

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "滑动",
        "customInnerType": "nativeCommand",
        "value": "前",
        "part": "方向",
        "object": "座椅"
    }
}
```

### 示例 4
**用户输入**: 前排座椅往前一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "滑动",
        "customInnerType": "nativeCommand",
        "value": "后",
        "part": "方向",
        "object": "座椅"
    }
}
```

### 示例 5
**用户输入**: 前排座椅往前移到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "滑动",
        "part": "方向",
        "customInnerType": "nativeCommand",
        "value": "前",
        "direction_range": "20/100",
        "object": "座椅"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
