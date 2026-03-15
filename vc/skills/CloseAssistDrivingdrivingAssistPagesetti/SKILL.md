---
name: CloseAssistDrivingdrivingAssistPagesetti
description: Close assist driving/driving assist page/settings (关闭辅助驾驶/驾驶辅助页面/设置)
---

## 功能说明
- 关闭辅助驾驶/驾驶辅助页面/设置
- 打开辅助驾驶/驾驶辅助页面/设置

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
        "function": "智慧巡航",
        "subfunction": "辅助驾驶"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `page` | string | page | `页面` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `智慧巡航` |
| `subfunction` | string | subfunction | `辅助驾驶` |

## 调用示例

### 示例 1
**用户输入**: 关闭辅助驾驶设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "subfunction": "辅助驾驶",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "智慧巡航"
    }
}
```

### 示例 2
**用户输入**: 关闭辅助驾驶页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "智慧巡航",
        "subfunction": "辅助驾驶"
    }
}
```

### 示例 3
**用户输入**: 关闭驾驶辅助设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "智慧巡航",
        "subfunction": "辅助驾驶"
    }
}
```

### 示例 4
**用户输入**: 关闭驾驶辅助页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "智慧巡航",
        "subfunction": "辅助驾驶"
    }
}
```

### 示例 5
**用户输入**: 打开辅助驾驶

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "智慧巡航",
        "subfunction": "辅助驾驶"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
