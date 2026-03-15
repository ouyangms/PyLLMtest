---
name: Details
description: View maintenance details (控制车辆查看保养项目详情功能)
---

## 功能说明
- 控制车辆查看保养项目详情功能

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
        "page": "页面",
        "customInnerType": "nativeCommand",
        "object": "保养检测",
        "module": "空气滤清器滤芯"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `page` | string | page | `页面` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `保养检测` |
| `module` | string | module | `空气滤清器滤芯` |

## 调用示例

### 示例 1
**用户输入**: 制动液情况怎么样

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "页面",
        "customInnerType": "nativeCommand",
        "object": "保养检测",
        "module": "空调滤芯"
    }
}
```

### 示例 2
**用户输入**: 发动机冷却液情况怎么样

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "页面",
        "customInnerType": "nativeCommand",
        "object": "保养检测",
        "module": "碳罐空气滤清器"
    }
}
```

### 示例 3
**用户输入**: 变速箱油情况怎么样

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "页面",
        "customInnerType": "nativeCommand",
        "object": "保养检测",
        "module": "燃油滤清器"
    }
}
```

### 示例 4
**用户输入**: 机油机滤情况怎么样

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "页面",
        "customInnerType": "nativeCommand",
        "object": "保养检测",
        "module": "机油机滤"
    }
}
```

### 示例 5
**用户输入**: 正时皮带情况怎么样

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "页面",
        "customInnerType": "nativeCommand",
        "object": "保养检测",
        "module": "发动机冷却液"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
