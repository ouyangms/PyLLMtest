---
name: ControlReadingLight
description: Close reading lights (关闭主驾、副驾、二排左、二排右、三排/后排左、三排/后排右的阅读灯（根据实车配置）)
---

## 功能说明
- 关闭主驾、副驾、二排左、二排右、三排/后排左、三排/后排右的阅读灯（根据实车配置）
- 关闭全部、所有、全车阅读灯
- 打开主驾、副驾、二排左、二排右、三排/后排左、三排/后排右的阅读灯（根据实车配置）
- 打开全部、所有、全车阅读灯

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
        "object_raw": "阅读灯",
        "customInnerType": "nativeCommand",
        "position": "all",
        "object": "车内灯",
        "light_type_inside": "车顶灯"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `object_raw` | string | object_raw | `阅读灯` |
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `position` | string | position | `all` |
| `object` | string | object | `车内灯` |
| `light_type_inside` | string | light_type_inside | `车顶灯` |

## 调用示例

### 示例 1
**用户输入**: 关闭三排右的阅读灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "阅读灯",
        "object": "车内灯",
        "light_type_inside": "车顶灯",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 关闭三排左的阅读灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "阅读灯",
        "customInnerType": "nativeCommand",
        "position": "all",
        "object": "车内灯",
        "light_type_inside": "车顶灯"
    }
}
```

### 示例 3
**用户输入**: 关闭主驾的阅读灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "阅读灯",
        "customInnerType": "nativeCommand",
        "position": "all",
        "object": "车内灯",
        "light_type_inside": "车顶灯"
    }
}
```

### 示例 4
**用户输入**: 关闭二排右的阅读灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "打开",
        "object_raw": "阅读灯",
        "customInnerType": "nativeCommand",
        "object": "车内灯",
        "light_type_inside": "车顶灯"
    }
}
```

### 示例 5
**用户输入**: 关闭二排左的阅读灯

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "object_raw": "阅读灯",
        "customInnerType": "nativeCommand",
        "position": "all",
        "object": "车内灯",
        "light_type_inside": "车顶灯"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
