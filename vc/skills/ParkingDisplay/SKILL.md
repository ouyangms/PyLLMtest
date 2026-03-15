---
name: ParkingDisplay
description: Close cute gaze switch (关闭可爱注视开关)
---

## 功能说明
- 关闭可爱注视开关
- 关闭车外语音联动开关
- 关闭迎宾欢送灯效开关
- 关闭驻车信息显示开关
- 关闭驻车图案动效开关
- 打开可爱注视开关
- 打开车外语音联动开关
- 打开迎宾欢送灯效开关,默认播放第一个
- 打开驻车信息显示开关
- 打开驻车图案动效开关

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
        "customInnerType": "nativeCommand",
        "function": "迎宾欢送灯效",
        "object": "科技带灯",
        "page": "开关"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `迎宾欢送灯效` |
| `object` | string | object | `科技带灯` |
| `page` | string | page | `开关` |

## 调用示例

### 示例 1
**用户输入**: 关闭可爱注视

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "迎宾欢送灯效",
        "object": "科技带灯",
        "page": "开关"
    }
}
```

### 示例 2
**用户输入**: 关闭车外语音联动开关

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "驻车信息显示",
        "object": "科技带灯",
        "page": "开关"
    }
}
```

### 示例 3
**用户输入**: 关闭迎宾欢送灯效开关

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "驻车信息显示",
        "object": "科技带灯",
        "page": "开关"
    }
}
```

### 示例 4
**用户输入**: 关闭驻车信息显示开关

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "customInnerType": "nativeCommand",
        "function": "驻车图案动效",
        "object": "科技带灯"
    }
}
```

### 示例 5
**用户输入**: 关闭驻车图案动效

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "function": "驻车图案动效",
        "object": "科技带灯"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
