---
name: LumbarSupport
description: Adjust [前排/后排/左侧/右侧/全车] seat lumbar support up/down ([前排/后排/左侧/右侧/全车]座椅腰托调高/调低一点)
---

## 功能说明
- 【前排/后排/左侧/右侧/全车】座椅腰托调高/调低一点
- 座椅腰托往前/往后移一点
- 座椅腰托调高/调低一点
- 把【座椅腰托】+调到最前/后/上/下

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
        "object": "座椅腰托",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `方向` |
| `value` | string | value | `上` |
| `object` | string | object | `座椅腰托` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 全车座椅腰托调低一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "value": "下",
        "object": "座椅腰托",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 全车座椅腰托调后一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "滑动",
        "part": "方向",
        "value": "前",
        "object": "座椅腰托",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 前排座椅腰托调高一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "滑动",
        "part": "方向",
        "value": "后",
        "object": "座椅腰托",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 右侧座椅腰托调后一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "object": "座椅腰托",
        "customInnerType": "nativeCommand",
        "value": "前",
        "action_concrete": "true",
        "direction_range": "max"
    }
}
```

### 示例 5
**用户输入**: 后排座椅腰托调前一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "方向",
        "object": "座椅腰托",
        "customInnerType": "nativeCommand",
        "value": "后",
        "action_concrete": "true",
        "direction_range": "max"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
