---
name: ControlAutoFront
description: Toggle front combination light/external light/headlight (前组合灯/外部灯光/大灯关闭/打开)
---

## 功能说明
- 前组合灯/外部灯光/大灯关闭/打开
- 前组合灯/外部灯光/大灯切换为自动/近光灯/位置灯
- 打开/关闭前组合灯设置页
- 打开/关闭前组合灯（默认AUTO）
- 打开/切换/关闭位置灯/示廓灯
- 打开/切换/关闭近光灯

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
        "object": "前组合灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object` | string | object | `前组合灯` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭位置灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object": "前组合灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭前组合灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "近光灯",
        "customInnerType": "nativeCommand",
        "light_type_outside": "近光灯",
        "object": "车外灯"
    }
}
```

### 示例 3
**用户输入**: 关闭前组合灯设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "车灯",
        "object": "车灯",
        "action": "打开",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 关闭示廓灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "object_raw": "车灯",
        "object": "车灯",
        "action": "关闭",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 关闭车灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "切换",
        "object_raw": "近光灯",
        "customInnerType": "nativeCommand",
        "light_type_outside": "近光灯",
        "object": "车外灯"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
