---
name: NotificationMiddle
description: Close notification center page (关闭通知中心页面)
---

## 功能说明
- 关闭通知中心页面
- 打开通知中心页面

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
        "action": "打开",
        "page": "页面",
        "module": "通知"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `page` | string | page | `页面` |
| `module` | string | module | `通知` |

## 调用示例

### 示例 1
**用户输入**: 关闭通知中心页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "module": "通知",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开通知中心

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "page": "页面",
        "module": "通知"
    }
}
```

### 示例 3
**用户输入**: 打开通知中心页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page": "页面",
        "module": "通知"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
