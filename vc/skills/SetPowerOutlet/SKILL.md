---
name: SetPowerOutlet
description: Close power outlet (关闭电源插座)
---

## 功能说明
- 关闭电源插座
- 打开电源插座

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
        "position": "车内",
        "object": "电源"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `position` | string | position | `车内` |
| `object` | string | object | `电源` |

## 调用示例

### 示例 1
**用户输入**: 关闭220v电源插座

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "电源",
        "object_raw": "电源插座"
    }
}
```

### 示例 2
**用户输入**: 关闭车内电源

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "电源"
    }
}
```

### 示例 3
**用户输入**: 开始220v放电

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "电源"
    }
}
```

### 示例 4
**用户输入**: 开始电源插座

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "object": "电源",
        "object_raw": "220v电源插座"
    }
}
```

### 示例 5
**用户输入**: 打开220v电源插座

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "position": "车内",
        "object": "电源"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
