---
name: OpenWindowSettings
description: Close window lock settings (车窗锁设置关闭)
---

## 功能说明
- 车窗锁设置关闭
- 车窗锁设置打开

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
        "page": "设置",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "feature": "车窗锁"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `page` | string | page | `设置` |
| `action` | string | action | `打开` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `车窗` |
| `feature` | string | feature | `车窗锁` |

## 调用示例

### 示例 1
**用户输入**: 车窗锁设置关闭

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "action": "关闭",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "feature": "车窗锁"
    }
}
```

### 示例 2
**用户输入**: 车窗锁设置打开

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "action": "打开",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "feature": "车窗锁"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
