---
name: QueryVolume
description: Query multimedia volume (查询多媒体音量)
---

## 功能说明
- 查询多媒体音量
- 查询导航音量
- 查询语音音量
- 查询车外扬声器音量
- 查询通话音量
- 查询铃声音量

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
        "function": "查询当前音量",
        "action": "查看",
        "module": "多媒体"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `function` | string | function | `查询当前音量` |
| `action` | string | action | `查看` |
| `module` | string | module | `多媒体` |

## 调用示例

### 示例 1
**用户输入**: 多媒体音量是多少

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "查询当前音量",
        "action": "查看",
        "module": "导航"
    }
}
```

### 示例 2
**用户输入**: 导航音量是多少

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "查询当前音量",
        "action": "查看",
        "module": "语音"
    }
}
```

### 示例 3
**用户输入**: 语音音量是多少

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "查询当前音量",
        "action": "查看",
        "module": "电话"
    }
}
```

### 示例 4
**用户输入**: 车外扬声器音量是多少

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "function": "查询当前音量",
        "action": "查看",
        "module": "来电"
    }
}
```

### 示例 5
**用户输入**: 通话音量是多少

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "position": "车外",
        "action": "查看",
        "function": "查询当前音量",
        "object": "扬声器"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
