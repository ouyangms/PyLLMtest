---
name: SteeringWheelButton
description: Toggle steering wheel button custom page (打开/关闭方向盘按键自定义页)
---

## 功能说明
- 打开/关闭方向盘按键自定义页

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
        "page": "页面",
        "action": "打开",
        "part": "模式",
        "mode": "自定义",
        "object": "方向盘按键"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `page` | string | page | `页面` |
| `action` | string | action | `打开` |
| `part` | string | part | `模式` |
| `mode` | string | mode | `自定义` |
| `object` | string | object | `方向盘按键` |

## 调用示例

### 示例 1
**用户输入**: 关闭方向盘按键自定义设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "page": "页面",
        "action": "关闭",
        "part": "模式",
        "mode": "自定义",
        "object": "方向盘按键"
    }
}
```

### 示例 2
**用户输入**: 关闭方向盘按键自定义页

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "page": "页面",
        "action": "打开",
        "part": "模式",
        "mode": "自定义",
        "object": "方向盘按键"
    }
}
```

### 示例 3
**用户输入**: 打开方向盘按键自定义调节

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "page": "设置",
        "action": "关闭",
        "part": "模式",
        "mode": "自定义",
        "object": "方向盘按键"
    }
}
```

### 示例 4
**用户输入**: 打开方向盘按键自定义页

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "page": "页面",
        "action": "打开",
        "part": "模式",
        "mode": "自定义",
        "object": "方向盘按键"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
