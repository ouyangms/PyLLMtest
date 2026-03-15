---
name: CloseFunction
description: Close function (控制车辆关闭功能)
---

## 功能说明
- 控制车辆关闭功能

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
        "object_raw": "行车记录仪",
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "object": "行车记录仪",
        "cammode": "录像",
        "action": "关闭"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object_raw` | string | object_raw | `行车记录仪` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `摄像头模式` |
| `object` | string | object | `行车记录仪` |
| `cammode` | string | cammode | `录像` |
| `action` | string | action | `关闭` |

## 调用示例

### 示例 1
**用户输入**: 停止录像

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "object": "摄像头",
        "cammode": "录像",
        "action": "关闭"
    }
}
```

### 示例 2
**用户输入**: 停止拍摄

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "object": "摄像头",
        "cammode": "录像",
        "action": "关闭"
    }
}
```

### 示例 3
**用户输入**: 关闭录像

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "object": "摄像头",
        "cammode": "录像",
        "action": "关闭"
    }
}
```

### 示例 4
**用户输入**: 关闭行车记录仪录像

```json
{
    "api": "sys.car.crl",
    "param": {
        "cammode": "录像",
        "part": "摄像头模式",
        "customInnerType": "nativeCommand",
        "object": "摄像头",
        "action": "关闭"
    }
}
```

### 示例 5
**用户输入**: 结束录像

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "行车记录仪",
        "customInnerType": "nativeCommand",
        "part": "摄像头模式",
        "object": "行车记录仪",
        "cammode": "录像",
        "action": "关闭"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
