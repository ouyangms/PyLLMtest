---
name: OpenLight
description: Close light page/settings (关闭灯光页面/设置)
---

## 功能说明
- 关闭灯光页面/设置
- 打开灯光页面/设置

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
        "page": "页面",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "车灯",
        "object_raw": "灯光"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `page` | string | page | `页面` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `车灯` |
| `object_raw` | string | object_raw | `灯光` |

## 调用示例

### 示例 1
**用户输入**: 关闭灯光设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "车灯",
        "object_raw": "灯光"
    }
}
```

### 示例 2
**用户输入**: 关闭灯光页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "车灯",
        "object_raw": "灯光"
    }
}
```

### 示例 3
**用户输入**: 打开灯光设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "车灯",
        "object_raw": "灯光"
    }
}
```

### 示例 4
**用户输入**: 打开灯光页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "车灯",
        "object_raw": "灯光"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
