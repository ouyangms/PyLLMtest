---
name: UpChildLock
description: Lock [zone] child lock (控制车辆锁上[zone]儿童锁功能)
---

## 功能说明
- 控制车辆锁上【音区】儿童锁功能

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
        "object": "门锁",
        "customInnerType": "nativeCommand",
        "feature": "儿童锁",
        "action": "打开"
    }
}
```

### 特殊参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `zone` | string | 音区参数（主驾音区/副驾音区/全车/一排/二排/三排） | `主驾音区` |

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `object` | string | object | `门锁` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `feature` | string | feature | `儿童锁` |
| `action` | string | action | `打开` |

## 调用示例

### 示例 1
**用户输入**: 关闭儿童锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "儿童锁",
        "object": "门锁",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 打开儿童锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "儿童锁",
        "object": "门锁",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 锁上儿童锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "门锁",
        "customInnerType": "nativeCommand",
        "feature": "儿童锁",
        "action": "打开"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
