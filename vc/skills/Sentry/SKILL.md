---
name: Sentry
description: View sentry mode videos (/)
---

## 功能说明
- /

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
        "action": "查看",
        "part": "摄像头模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "cammode": "哨兵录像"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `查看` |
| `part` | string | part | `摄像头模式` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `整车` |
| `cammode` | string | cammode | `哨兵录像` |

## 调用示例

### 示例 1
**用户输入**: 打开哨兵模式视频

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "查看",
        "part": "摄像头模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "cammode": "哨兵录像"
    }
}
```

### 示例 2
**用户输入**: 查看哨兵模式视频

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "查看",
        "part": "摄像头模式",
        "customInnerType": "nativeCommand",
        "object": "整车",
        "cammode": "哨兵录像"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
