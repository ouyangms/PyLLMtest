---
name: HeadrestAudio
description: Close headrest audio smart switch (关闭头枕音响智能切换)
---

## 功能说明
- 关闭头枕音响智能切换
- 关闭头枕音响设置
- 将头枕音响调整到驾享、共享、全车私享模式
- 将头枕音响调整到驾享、共享、私享模式
- 打开头枕音响智能切换
- 打开头枕音响设置
- 调整4个头枕音响音量（主驾、副驾、二排左、二排右）
- 轮流切换共享/驾享/私享/全车私享

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
        "part": "模式",
        "object_raw": "头枕音响",
        "mode": "驾享",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "头枕音响"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `模式` |
| `object_raw` | string | object_raw | `头枕音响` |
| `mode` | string | mode | `驾享` |
| `action_concrete` | string | action_concrete | `true` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part_raw` | string | part_raw | `模式` |
| `object` | string | object | `头枕音响` |

## 调用示例

### 示例 1
**用户输入**: 关闭全车私享

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "模式",
        "object_raw": "头枕音响",
        "mode": "共享",
        "action_concrete": "true",
        "customInnerType": "nativeCommand",
        "part_raw": "模式",
        "object": "头枕音响"
    }
}
```

### 示例 2
**用户输入**: 关闭共享

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕音响",
        "part": "模式",
        "mode": "全车私享",
        "action_concrete": "true",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭头枕音响智能切换

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕音响",
        "part": "模式",
        "action": "切换",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 关闭头枕音响设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕音响",
        "part": "模式",
        "action": "打开",
        "mode": "共享",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 关闭私享

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕音响",
        "part": "模式",
        "action": "打开",
        "mode": "驾享",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
