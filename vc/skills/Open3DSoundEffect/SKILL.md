---
name: Open3DSoundEffect
description: Toggle 3D surround sound (打开/关闭3D环绕音效)
---

## 功能说明
- 打开/关闭3D环绕音效
- 打开/关闭3D超感空间音设置页面
- 调节/调整/调高/调低 3D 环绕音效/3D 环绕音效强

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
        "feature": "3D环绕音",
        "object": "扬声器",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `feature` | string | feature | `3D环绕音` |
| `object` | string | object | `扬声器` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭3D环绕音效

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "feature": "3D环绕音",
        "object": "扬声器",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭3D超感空间音设置页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "音量",
        "value": "-",
        "feature": "3D环绕音"
    }
}
```

### 示例 3
**用户输入**: 打开3D环绕音效

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "音量",
        "value": "+",
        "feature": "3D环绕音"
    }
}
```

### 示例 4
**用户输入**: 打开3D超感空间音设置页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "feature": "3D环绕音",
        "action": "打开",
        "object": "扬声器",
        "page": "设置"
    }
}
```

### 示例 5
**用户输入**: 调低3D环绕音效

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "feature": "3D环绕音",
        "action": "关闭",
        "object": "扬声器",
        "page": "设置"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
