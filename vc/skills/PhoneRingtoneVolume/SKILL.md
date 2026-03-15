---
name: PhoneRingtoneVolume
description: Close custom frequency settings (关闭自定义调频设置)
---

## 功能说明
- 关闭自定义调频设置
- 打开/关闭电话铃声音量设置
- 打开自定义调频设置
- 打开设置页
- 打开高中低音设置
- 电话铃声音量调低0
- 电话铃声音量调低一点
- 电话铃声音量调到12
- 电话铃声音量调到最大
- 电话铃声音量调到最小
- 电话铃声音量调高0
- 电话铃声音量调高一点
- 电话音量调低1
- 电话音量调低一点
- 电话音量调到13
- 电话音量调到最大
- 电话音量调到最小
- 电话音量调高1
- 电话音量调高一点

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
        "module": "来电",
        "customInnerType": "nativeCommand",
        "part": "音量",
        "part_raw": "音量",
        "object": "屏幕"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `page` | string | page | `设置` |
| `module` | string | module | `来电` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `音量` |
| `part_raw` | string | part_raw | `音量` |
| `object` | string | object | `屏幕` |

## 调用示例

### 示例 1
**用户输入**: 关闭电话铃声音量设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "page": "设置",
        "module": "来电",
        "customInnerType": "nativeCommand",
        "part": "音量",
        "part_raw": "音量",
        "object": "屏幕"
    }
}
```

### 示例 2
**用户输入**: 关闭自定义调频设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "value": "13",
        "module": "来电",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part_raw": "音量",
        "object": "屏幕"
    }
}
```

### 示例 3
**用户输入**: 打开中音设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "value": "max",
        "module": "来电",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part_raw": "音量",
        "object": "屏幕"
    }
}
```

### 示例 4
**用户输入**: 打开低音设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "value": "min",
        "module": "来电",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part_raw": "音量",
        "object": "屏幕"
    }
}
```

### 示例 5
**用户输入**: 打开电话铃声音量设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "音量",
        "module": "来电",
        "value": "+1",
        "object": "屏幕",
        "part_raw": "音量",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
