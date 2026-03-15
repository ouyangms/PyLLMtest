---
name: Window
description: Open/close window (打开/关闭车窗)
---

## 功能说明
- 打开/关闭车窗

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
        "action": "打开",
        "object": "车窗",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object` | string | object | `车窗` |
| `object_raw` | string | object_raw | `车窗` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭主驾车窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "action": "打开",
        "position": "副驾"
    }
}
```

### 示例 2
**用户输入**: 关闭右后车窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "action": "打开",
        "position": "副驾"
    }
}
```

### 示例 3
**用户输入**: 关闭左后车窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "action": "打开",
        "position": "右后"
    }
}
```

### 示例 4
**用户输入**: 关闭车窗

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "车窗",
        "object_raw": "车窗",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 副驾驶车窗开启

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "车窗",
        "customInnerType": "nativeCommand",
        "object": "车窗",
        "action": "关闭",
        "position": "主驾"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
