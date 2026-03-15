---
name: FrontDown
description: Take front photo (控制车辆拍下前面照片功能)
---

## 功能说明
- 控制车辆拍下前面照片功能

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
        "position": "前",
        "part": "摄像头模式",
        "object": "摄像头",
        "cammode": "拍照",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `position` | string | position | `前` |
| `part` | string | part | `摄像头模式` |
| `object` | string | object | `摄像头` |
| `cammode` | string | cammode | `拍照` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 拍下前面照片

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "position": "前",
        "part": "摄像头模式",
        "object": "摄像头",
        "cammode": "拍照",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
