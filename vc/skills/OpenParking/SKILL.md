---
name: OpenParking
description: View vehicle surroundings after parking via phone app (停车后通过手机 app 查看车辆周围信息，快速寻找爱车)
---

## 功能说明
- 停车后通过手机 app 查看车辆周围信息，快速寻找爱车

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
        "function": "驻车",
        "cammode": "拍照",
        "action": "打开"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `摄像头模式` |
| `function` | string | function | `驻车` |
| `cammode` | string | cammode | `拍照` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭驻车拍照

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "function": "驻车",
        "cammode": "拍照",
        "action": "关闭"
    }
}
```

### 示例 2
**用户输入**: 打开驻车拍照

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "function": "驻车",
        "cammode": "拍照",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
