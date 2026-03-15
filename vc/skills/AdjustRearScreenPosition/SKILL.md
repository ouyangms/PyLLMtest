---
name: AdjustRearScreenPosition
description: Adjust rear screen position forward/backward (后排屏位置向前/向后调节)
---

## 功能说明
- 后排屏位置向前/向后调节
- 后排屏角度向外/向里调节
- 后排屏调到最前|最后
- 打开/关闭后排屏调节页

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
        "page": "页面",
        "position": "后排",
        "object": "屏幕",
        "object_raw": "屏",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action` | string | action | `打开` |
| `page` | string | page | `页面` |
| `position` | string | position | `后排` |
| `object` | string | object | `屏幕` |
| `object_raw` | string | object_raw | `屏` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: 关闭后排屏设置页

```json
{
    "api": "sys.car.crl",
    "param": {
        "action": "关闭",
        "page": "设置",
        "position": "后排",
        "object": "屏幕",
        "object_raw": "屏",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: 后排屏位置向前调节

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "外",
        "position": "后排",
        "object": "屏幕",
        "part": "方向",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: 后排屏位置向后调节

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "内",
        "position": "后排",
        "object": "屏幕",
        "part": "方向",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: 后排屏角度向外调节

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "前",
        "position": "后排",
        "object": "屏幕",
        "part": "方向",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: 后排屏角度向里调节

```json
{
    "api": "sys.car.crl",
    "param": {
        "value": "后",
        "position": "后排",
        "object": "屏幕",
        "part": "方向",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
