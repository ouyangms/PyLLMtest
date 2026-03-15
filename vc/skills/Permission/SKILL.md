---
name: Permission
description: Close sensitive permission usage (关闭敏感权限使用)
---

## 功能说明
- 关闭敏感权限使用
- 打开敏感权限使用

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
        "action": "打开",
        "page_function": "敏感权限"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `action` | string | action | `打开` |
| `page_function` | string | page_function | `敏感权限` |

## 调用示例

### 示例 1
**用户输入**: 关闭敏感权限

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page_function": "敏感权限"
    }
}
```

### 示例 2
**用户输入**: 关闭敏感权限使用

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "page_function": "敏感权限"
    }
}
```

### 示例 3
**用户输入**: 打开敏感权限

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "关闭",
        "page_function": "敏感权限"
    }
}
```

### 示例 4
**用户输入**: 打开敏感权限使用

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "action": "打开",
        "page_function": "敏感权限"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
