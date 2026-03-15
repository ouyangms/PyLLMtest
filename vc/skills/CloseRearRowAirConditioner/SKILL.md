---
name: CloseRearRowAirConditioner
description: Close safety and service settings (关闭安全与服务设置)
---

## 功能说明
- 关闭安全与服务设置
- 关闭安全与服务页面
- 关闭系统设置页面
- 关闭系统页面/界面/窗口
- 打开安全与服务设置
- 打开安全与服务页面
- 打开系统设置页面
- 打开系统页面/界面/窗口

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
        "action": "关闭",
        "feature": "空调锁",
        "position": "后排",
        "object": "空调",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `关闭` |
| `feature` | string | feature | `空调锁` |
| `position` | string | position | `后排` |
| `object` | string | object | `空调` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭后排空调锁

```json
{
    "api": "sys.car.crl",
    "param": {
        "page_function": "语言与音色",
        "page": "设置",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭安全与服务设置

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "page_function": "安全与服务",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 关闭安全与服务页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "设置",
        "page_function": "安全与服务",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 关闭开用户直连/关闭语音直连

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "page_function": "安全与服务",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 关闭系统设置页面

```json
{
    "api": "sys.car.crl",
    "param": {
        "page": "页面",
        "page_function": "安全与服务",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
