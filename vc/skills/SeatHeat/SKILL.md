---
name: SeatHeat
description: Set [前排/后排/左侧/右侧/全车] seat heating to low/medium/high/auto ([前排/后排/左侧/右侧/全车]座椅加热开到低/中/高/自动挡)
---

## 功能说明
- 【前排/后排/左侧/右侧/全车】座椅加热开到低/中/高/自动挡
- 【前排/后排/左侧/右侧/全车】座椅加热开到最大/最小
- 座椅加热调到具体档位
- 座椅加热调到最高/最低
- 座椅加热调大/调小/调高/调低+一点/一挡
- 打开/关闭座椅加热
- 打开/关闭自动座椅加热

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
        "feature": "加热",
        "object": "座椅",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `加热` |
| `object` | string | object | `座椅` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 全车座椅加热开到最小

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "加热",
        "customInnerType": "nativeCommand",
        "object_raw": "座椅",
        "action": "打开",
        "object": "座椅"
    }
}
```

### 示例 2
**用户输入**: 全车座椅加热开到自动挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "加热",
        "customInnerType": "nativeCommand",
        "object_raw": "座椅",
        "action": "打开",
        "object": "座椅"
    }
}
```

### 示例 3
**用户输入**: 全车座椅加热开到高挡

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "加热",
        "object": "座椅",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 关座椅加热

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "加热",
        "customInnerType": "nativeCommand",
        "object_raw": "座椅",
        "action": "关闭",
        "object": "座椅"
    }
}
```

### 示例 5
**用户输入**: 关闭主驾座椅加热

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "加热",
        "part": "温度",
        "object": "座椅",
        "value": "+",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
