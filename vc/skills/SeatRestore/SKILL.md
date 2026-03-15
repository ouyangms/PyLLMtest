---
name: SeatRestore
description: Restore seat position (座椅位置恢复)
---

## 功能说明
- 座椅位置恢复

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
        "part": "座椅记忆位置",
        "action": "还原",
        "object": "座椅"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `part` | string | part | `座椅记忆位置` |
| `action` | string | action | `还原` |
| `object` | string | object | `座椅` |

## 调用示例

### 示例 1
**用户输入**: 座椅记忆调到一

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "座椅记忆位置",
        "action": "还原",
        "position": "主驾",
        "object": "座椅"
    }
}
```

### 示例 2
**用户输入**: 恢复主驾座椅位置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "memlocation": "1",
        "part": "座椅记忆位置",
        "action_concrete": "true",
        "object": "座椅"
    }
}
```

### 示例 3
**用户输入**: 恢复座椅位置

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "part": "座椅记忆位置",
        "action": "还原",
        "object": "座椅"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
