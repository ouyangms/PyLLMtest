---
name: AdjustSideMirror
description: Adjust side mirror up/down/left/right (后视镜向上/下/左/右调节一点)
---

## 功能说明
- 后视镜向上/下/左/右调节一点
- 左侧/右侧后视镜向上/下/左/右调节一点
- 左侧/右侧后视镜调到最上/最下/最左/最右

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
        "position": "左",
        "object": "后视镜",
        "value": "上",
        "part": "方向",
        "object_raw": "后视镜",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `position` | string | position | `左` |
| `object` | string | object | `后视镜` |
| `value` | string | value | `上` |
| `part` | string | part | `方向` |
| `object_raw` | string | object_raw | `后视镜` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 右侧后视镜向上调节一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "上",
        "object_raw": "后视镜",
        "customInnerType": "nativeCommand",
        "part": "方向",
        "position": "左",
        "object": "后视镜"
    }
}
```

### 示例 2
**用户输入**: 右侧后视镜向下调节一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "左",
        "object": "后视镜",
        "value": "下",
        "part": "方向",
        "object_raw": "后视镜",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 右侧后视镜向右调节一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "左",
        "object": "后视镜",
        "value": "左",
        "part": "方向",
        "object_raw": "后视镜",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 右侧后视镜向左调节一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "左",
        "object": "后视镜",
        "value": "右",
        "part": "方向",
        "object_raw": "后视镜",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 右侧后视镜调到最上

```json
{
    "api": "sys.car.crl",
    "param": {
        "position": "右",
        "object": "后视镜",
        "value": "上",
        "part": "方向",
        "object_raw": "后视镜",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
