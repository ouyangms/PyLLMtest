---
name: QueryWiFi
description: Query Wi-Fi password (查询Wi-Fi密码)
---

## 功能说明
- 查询Wi-Fi密码

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
        "page": "设置",
        "customInnerType": "nativeCommand",
        "feature": "热点"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `page` | string | page | `设置` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `feature` | string | feature | `热点` |

## 调用示例

### 示例 1
**用户输入**: WiFi密码是多少

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "查询无线密码",
        "action": "查看",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 我的无线密码是多少

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "查询无线密码",
        "action": "查看",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 显示无线密码

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "设置",
        "customInnerType": "nativeCommand",
        "feature": "热点"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
