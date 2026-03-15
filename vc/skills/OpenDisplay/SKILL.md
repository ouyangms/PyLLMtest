---
name: OpenDisplay
description: Close display page/settings (关闭显示页面/设置)
---

## 功能说明
- 关闭显示页面/设置
- 打开显示页面/设置

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
        "feature": "显示",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "page": "设置"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `显示` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `屏幕` |
| `page` | string | page | `设置` |

## 调用示例

### 示例 1
**用户输入**: 关闭显示设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "显示",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "page": "页面"
    }
}
```

### 示例 2
**用户输入**: 关闭显示页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "显示",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "page": "设置"
    }
}
```

### 示例 3
**用户输入**: 打开显示设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "显示",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "page": "页面"
    }
}
```

### 示例 4
**用户输入**: 打开显示页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "显示",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "屏幕",
        "page": "设置"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
