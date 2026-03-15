---
name: HeadrestBrightness
description: Adjust [passenger headrest screen brightness lower 30%] (把[副驾头枕屏亮度调低 30%])
---

## 功能说明
- 把【副驾头枕屏亮度调低 30%】
- 把【副驾头枕屏亮度调低一点】（一点=10%）
- 把【副驾头枕屏亮度调到最低】
- 把【副驾头枕屏亮度调到最高】
- 把【副驾头枕屏亮度调高 30%】
- 把【副驾头枕屏亮度调高一点】（一点=10%）
- 把【头枕屏亮度调低 30%】
- 把【头枕屏亮度调低一点】（一点=10%）
- 把【头枕屏亮度调高 30%】
- 把【头枕屏亮度调高一点】（一点=10%）
- 把【头枕屏调到最亮】
- 把【头枕屏调到最暗】
- 把【将主驾头枕屏亮度模式设置为白天】
- 把【将头枕屏亮度模式设置为白天】

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
        "part": "亮度",
        "customInnerType": "nativeCommand",
        "object": "头枕屏",
        "value": "+"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `part` | string | part | `亮度` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `object` | string | object | `头枕屏` |
| `value` | string | value | `+` |

## 调用示例

### 示例 1
**用户输入**: 把副驾头枕屏亮度调低30%

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕屏",
        "part_raw": "亮度",
        "object_raw": "头枕屏",
        "customInnerType": "nativeCommand",
        "value": "-",
        "part": "亮度"
    }
}
```

### 示例 2
**用户输入**: 把副驾头枕屏亮度调低一点

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕屏",
        "part_raw": "亮度",
        "object_raw": "头枕屏",
        "customInnerType": "nativeCommand",
        "value": "+",
        "part": "亮度",
        "position": "副驾"
    }
}
```

### 示例 3
**用户输入**: 把副驾头枕屏亮度调到最低

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕屏",
        "part_raw": "亮度",
        "object_raw": "头枕屏",
        "customInnerType": "nativeCommand",
        "value": "-",
        "part": "亮度",
        "position": "副驾"
    }
}
```

### 示例 4
**用户输入**: 把副驾头枕屏亮度调到最高

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕屏",
        "part_raw": "亮度",
        "object_raw": "头枕屏",
        "customInnerType": "nativeCommand",
        "value": "+30/100",
        "part": "亮度"
    }
}
```

### 示例 5
**用户输入**: 把副驾头枕屏亮度调高30%

```json
{
    "api": "sys.car.crl",
    "param": {
        "object": "头枕屏",
        "part_raw": "亮度",
        "object_raw": "头枕屏",
        "customInnerType": "nativeCommand",
        "value": "-30/100",
        "part": "亮度"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
