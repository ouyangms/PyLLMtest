---
name: OpenNavigationEarphoneBluetoothPhoneCall
description: Open sound volume settings control (/)
---

## 功能说明
- /

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
        "part": "音量",
        "part_raw": "声音",
        "customInnerType": "nativeCommand",
        "position": "车内",
        "object": "屏幕"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `page` | string | page | `设置` |
| `part` | string | part | `音量` |
| `part_raw` | string | part_raw | `声音` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `position` | string | position | `车内` |
| `object` | string | object | `屏幕` |

## 调用示例

### 示例 1
**用户输入**: 打开车内声音设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "设置",
        "part_raw": "音效",
        "customInnerType": "nativeCommand",
        "part": "音效",
        "object": "整车"
    }
}
```

### 示例 2
**用户输入**: 打开音效

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "part": "音效",
        "customInnerType": "nativeCommand",
        "part_raw": "音效",
        "object": "整车"
    }
}
```

### 示例 3
**用户输入**: 打开音效控制设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "page": "设置",
        "part": "音量",
        "part_raw": "声音",
        "customInnerType": "nativeCommand",
        "position": "车内",
        "object": "屏幕"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
