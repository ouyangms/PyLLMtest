---
name: SetHUDMode
description: Set HUD to AR/minimal/2D/3D/map/multi-lane (HUD设置为AR/极简/2D/3D/地图/多车道)
---

## 功能说明
- HUD设置为AR/极简/2D/3D/地图/多车道
- 切换/上一个/下一个HUD模式
- 切换/上一个/下一个HUD视图

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
        "action_concrete": "true",
        "mode": "AR",
        "part": "模式",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `action_concrete` | string | action_concrete | `true` |
| `mode` | string | mode | `AR` |
| `part` | string | part | `模式` |
| `object` | string | object | `HUD` |
| `object_raw` | string | object_raw | `HUD` |
| `customInnerType` | string | customInnerType | `nativeCommand` |

## 调用示例

### 示例 1
**用户输入**: HUD模式设为地图模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "mode": "极简",
        "part": "模式",
        "object": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 2
**用户输入**: HUD模式设为多车道模式

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "mode": "2D",
        "part": "模式",
        "object": "HUD",
        "object_raw": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 3
**用户输入**: HUD设置为2D

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "mode": "3D",
        "part": "模式",
        "object": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 4
**用户输入**: HUD设置为3D

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "mode": "导航",
        "part": "模式",
        "object": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```

### 示例 5
**用户输入**: HUD设置为AR

```json
{
    "api": "sys.car.crl",
    "param": {
        "action_concrete": "true",
        "mode": "多车道",
        "part": "模式",
        "object": "HUD",
        "customInnerType": "nativeCommand"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
