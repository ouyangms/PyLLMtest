---
name: SeatMemory
description: Previous/next (上一个/下一个)
---

## 功能说明
- 上一个/下一个
- 将当前座椅保存到当前记忆位置
- 将当前座椅保存到某个记忆位置
- 把【座椅位置】+【记忆】（下来）
- 调节至位置1、位置2、位置3

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
        "part": "座椅记忆位置",
        "action": "保存",
        "customInnerType": "nativeCommand",
        "object": "座椅"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `座椅记忆位置` |
| `action` | string | action | `保存` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `座椅` |

## 调用示例

### 示例 1
**用户输入**: 上一个座椅记忆模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "座椅记忆位置",
        "action": "保存",
        "customInnerType": "nativeCommand",
        "object": "座椅"
    }
}
```

### 示例 2
**用户输入**: 下一个座椅记忆模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "座椅记忆位置",
        "action": "保存",
        "customInnerType": "nativeCommand",
        "object": "座椅",
        "action_concrete": "true",
        "memlocation": "1"
    }
}
```

### 示例 3
**用户输入**: 保存座椅参数

```json
{
    "api": "sys.car.crl",
    "param": {
        "part": "座椅记忆位置",
        "action": "保存",
        "customInnerType": "nativeCommand",
        "object": "座椅"
    }
}
```

### 示例 4
**用户输入**: 切换座椅记忆位置

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "memlocation": "1",
        "customInnerType": "nativeCommand",
        "part": "座椅记忆位置",
        "object": "座椅"
    }
}
```

### 示例 5
**用户输入**: 座椅保存到位置1

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "memlocation": "2",
        "customInnerType": "nativeCommand",
        "part": "座椅记忆位置",
        "object": "座椅"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
