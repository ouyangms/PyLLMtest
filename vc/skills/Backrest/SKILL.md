---
name: Backrest
description: Adjust [前排/后排/左侧/右侧/全车] seat backrest forward/backward ([前排/后排/左侧/右侧/全车]座椅靠背往前/往后一点)
---

## 功能说明
- 【前排/后排/左侧/右侧/全车】座椅靠背往前/往后一点
- 【前排/后排/左侧/右侧/全车】座椅靠背往前/往后移到50%
- 【前排/后排/左侧/右侧/全车】座椅靠背移到最前/最后
- 座椅靠背往上/往下/往前/往后/调直/放倒+一点/百分之二十
- 座椅靠背调到最上/最下/最前/最后
- 靠背角度调到70度

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
        "part": "方向",
        "value": "上",
        "object": "靠背",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `方向` |
| `value` | string | value | `上` |
| `object` | string | object | `靠背` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 全车座椅靠背往后一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "value": "下",
        "object": "靠背",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 全车座椅靠背往后移到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "value": "前",
        "object": "靠背",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 全车座椅靠背移到最后

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "前",
        "customInnerType": "nativeCommand",
        "position": "副驾",
        "object_raw": "靠背",
        "object": "靠背",
        "part": "方向"
    }
}
```

### 示例 4
**用户输入**: 前排座椅靠背往前一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "value": "后",
        "object": "靠背",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 前排座椅靠背往前移到50%

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "后",
        "customInnerType": "nativeCommand",
        "object_raw": "靠背",
        "object": "靠背",
        "part": "方向"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
