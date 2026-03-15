---
name: PhoneCallVolume
description: Close call volume settings (关闭通话音量设置)
---

## 功能说明
- 关闭通话音量设置
- 打开通话声音
- 打开通话音量设置
- 通话声音大点
- 通话声音小点
- 通话音量减小3
- 通话音量减小30%
- 通话音量增大3
- 通话音量增大30%
- 通话音量调到3
- 通话音量调到30%
- 通话音量调到最大
- 通话音量调到最小

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
        "action": "关闭",
        "mode": "静音",
        "part": "模式",
        "module": "电话",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `mode` | string | mode | `静音` |
| `part` | string | part | `模式` |
| `module` | string | module | `电话` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `屏幕` |

## 调用示例

### 示例 1
**用户输入**: 关闭通话音量设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "module": "电话",
        "value": "+",
        "part_raw": "声音",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 2
**用户输入**: 打开通话声音

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "module": "电话",
        "value": "-",
        "part_raw": "声音",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 3
**用户输入**: 打开通话音量设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "module": "电话",
        "value": "+30/100",
        "part_raw": "音量",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 4
**用户输入**: 通话声音大点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "module": "电话",
        "value": "+3",
        "part_raw": "音量",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```

### 示例 5
**用户输入**: 通话声音小点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "module": "电话",
        "value": "-3",
        "part_raw": "音量",
        "customInnerType": "nativeCommand",
        "object": "屏幕"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
