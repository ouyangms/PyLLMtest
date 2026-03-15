---
name: OpenTimedPhoto
description: Open timed photo (控制车辆打开定时拍照功能)
---

## 功能说明
- 控制车辆打开定时拍照功能

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
        "part": "摄像头模式",
        "object": "摄像头",
        "cammode": "定时拍照",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `摄像头模式` |
| `object` | string | object | `摄像头` |
| `cammode` | string | cammode | `定时拍照` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 321拍照

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "时长",
        "object": "摄像头",
        "cammode": "定时拍照",
        "action": "打开",
        "value": "00:00:05"
    }
}
```

### 示例 2
**用户输入**: 倒计时5秒拍摄

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "时长",
        "object": "摄像头",
        "cammode": "定时拍照",
        "action": "打开",
        "value": "00:00:03"
    }
}
```

### 示例 3
**用户输入**: 打开定时拍照

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "object": "摄像头",
        "cammode": "定时拍照",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
