---
name: QueryCurrentTirePressureStatus
description: Query current tire pressure status (whole vehicle) (当前胎压状态查询（全车）)
---

## 功能说明
- 当前胎压状态查询（全车）

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
        "function": "查询胎压状态",
        "action": "查看",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `function` | string | function | `查询胎压状态` |
| `action` | string | action | `查看` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 现在胎压正常吗

```json
{
    "api": "sys.car.crl",
    "param": {
        "function": "查询胎压状态",
        "action": "查看",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
