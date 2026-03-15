---
name: WirelessCharging
description: Close [location] wireless charging ([location]关闭无线充电)
---

## 功能说明
- 【位置】关闭无线充电
- 【位置】打开无线充电
- 关闭这边的无线充电
- 打开这边的无线充电

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
        "function": "无线充电",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "position": "前排"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `无线充电` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `position` | string | position | `前排` |

## 调用示例

### 示例 1
**用户输入**: 关闭后排手机无线充电

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "无线充电",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "position": "后排"
    }
}
```

### 示例 2
**用户输入**: 关闭无线充电

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "无线充电",
        "customInnerType": "nativeCommand",
        "action": "打开",
        "position": "当前"
    }
}
```

### 示例 3
**用户输入**: 关闭这边的无线充电

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "无线充电",
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "position": "当前"
    }
}
```

### 示例 4
**用户输入**: 开启无线充电

```json
{
    "api": "vehicle.wirelessCharging.open",
    "param": {
        "intent": "打开无线充电",
        "duiWidget": "text",
        "isActive": "$extra.isActive$"
    }
}
```

### 示例 5
**用户输入**: 打开前排手机无线充电

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "function": "无线充电"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
