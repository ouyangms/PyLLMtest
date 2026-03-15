---
name: TakePhoto
description: Take photo (控制车辆帮我拍照一下/拍照/拍张照/普通拍照/我要拍照/再来一张功能)
---

## 功能说明
- 控制车辆帮我拍照一下/拍照/拍张照/普通拍照/我要拍照/再来一张功能

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
        "object": "摄像头",
        "cammode": "定时拍照",
        "part": "时长",
        "value": "00:00:03",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `摄像头` |
| `cammode` | string | cammode | `定时拍照` |
| `part` | string | part | `时长` |
| `value` | string | value | `00:00:03` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 帮我拍张照

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "摄像头",
        "cammode": "定时拍照",
        "part": "时长",
        "value": "00:00:03",
        "action": "打开"
    }
}
```

### 示例 2
**用户输入**: 帮我拍照

```json
{
    "api": "sys.car.crl",
    "param": {
        "cammode": "拍照",
        "customInnerType": "nativeCommand",
        "object": "摄像头",
        "action": "打开",
        "part": "摄像头模式"
    }
}
```

### 示例 3
**用户输入**: 帮我拍照一下

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "摄像头",
        "cammode": "定时拍照",
        "part": "时长",
        "value": "00:00:03",
        "action": "打开"
    }
}
```

### 示例 4
**用户输入**: 帮我普通拍照

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "摄像头",
        "cammode": "定时拍照",
        "part": "时长",
        "value": "00:00:03",
        "action": "打开"
    }
}
```

### 示例 5
**用户输入**: 我要拍照

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "摄像头",
        "cammode": "定时拍照",
        "part": "时长",
        "value": "00:00:03",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
