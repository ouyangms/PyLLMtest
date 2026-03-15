---
name: Middle
description: Close central lock (将中控锁设置项开关关闭)
---

## 功能说明
- 将中控锁设置项开关关闭
- 将中控锁设置项开关开启
- 解锁中控锁

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
        "feature": "中控锁",
        "action": "关闭",
        "object": "门锁",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `feature` | string | feature | `中控锁` |
| `action` | string | action | `关闭` |
| `object` | string | object | `门锁` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭中控锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "中控锁",
        "action": "打开",
        "object": "门锁",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 开启中控锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "中控锁",
        "object": "门锁",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 打开中控锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "中控锁",
        "action": "关闭",
        "object": "门锁",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 解锁中控锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "feature": "中控锁",
        "action": "关闭",
        "object": "门锁",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
