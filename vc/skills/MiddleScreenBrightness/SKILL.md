---
name: MiddleScreenBrightness
description: Close central screen auto brightness (关闭中控自动调节亮度)
---

## 功能说明
- 关闭中控自动调节亮度
- 关闭主屏
- 关闭亮度调节设置
- 关闭副屏
- 关闭负一屏
- 屏幕/中控亮度调亮3
- 屏幕/中控亮度调亮30%
- 屏幕/中控亮度调低点
- 屏幕/中控亮度调到3
- 屏幕/中控亮度调到30%
- 屏幕/中控亮度调到最亮
- 屏幕/中控亮度调到最暗
- 屏幕/中控亮度调暗3
- 屏幕/中控亮度调暗30%
- 屏幕/中控亮度调高点
- 打开中控自动调节亮度
- 打开亮度调节设置
- 打开负一屏

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
        "part": "亮度",
        "part_raw": "亮度",
        "customInnerType": "nativeCommand",
        "value": "+",
        "object_raw": "屏幕",
        "object": "屏幕"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `亮度` |
| `part_raw` | string | part_raw | `亮度` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `value` | string | value | `+` |
| `object_raw` | string | object_raw | `屏幕` |
| `object` | string | object | `屏幕` |

## 调用示例

### 示例 1
**用户输入**: 中控亮度调亮3

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+",
        "object": "屏幕",
        "object_raw": "屏幕",
        "customInnerType": "nativeCommand",
        "part": "亮度"
    }
}
```

### 示例 2
**用户输入**: 中控亮度调亮31%

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "+",
        "object": "屏幕",
        "object_raw": "中控屏",
        "customInnerType": "nativeCommand",
        "part": "亮度"
    }
}
```

### 示例 3
**用户输入**: 中控亮度调低点

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "customInnerType": "nativeCommand",
        "value": "+",
        "object_raw": "中控",
        "object": "屏幕"
    }
}
```

### 示例 4
**用户输入**: 中控亮度调到3

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "customInnerType": "nativeCommand",
        "value": "-",
        "object_raw": "中控",
        "object": "屏幕"
    }
}
```

### 示例 5
**用户输入**: 中控亮度调到31%

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "亮度",
        "part_raw": "亮度",
        "customInnerType": "nativeCommand",
        "value": "-",
        "object_raw": "屏幕",
        "object": "屏幕"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
