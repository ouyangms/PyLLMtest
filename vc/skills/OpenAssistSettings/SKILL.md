---
name: OpenAssistSettings
description: Toggle pre-collision assist settings (控制车辆打开/关闭预碰撞辅助设置好功能)
---

## 功能说明
- 控制车辆打开/关闭预碰撞辅助设置好功能

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
        "subfunction": "碰撞安全辅助",
        "page": "设置",
        "function": "前向辅助",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `subfunction` | string | subfunction | `碰撞安全辅助` |
| `page` | string | page | `设置` |
| `function` | string | function | `前向辅助` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭预碰撞辅助设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "碰撞安全辅助",
        "page": "设置",
        "function": "前向辅助",
        "customInnerType": "nativeCommand",
        "action": "关闭"
    }
}
```

### 示例 2
**用户输入**: 关闭预碰撞辅助页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "碰撞安全辅助",
        "page": "页面",
        "function": "前向辅助",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```

### 示例 3
**用户输入**: 打开预碰撞辅助设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "碰撞安全辅助",
        "page": "页面",
        "function": "前向辅助",
        "customInnerType": "nativeCommand",
        "action": "关闭"
    }
}
```

### 示例 4
**用户输入**: 打开预碰撞辅助页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "碰撞安全辅助",
        "page": "设置",
        "function": "前向辅助",
        "customInnerType": "nativeCommand",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
