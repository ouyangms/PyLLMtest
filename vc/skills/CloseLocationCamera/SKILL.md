---
name: CloseLocationCamera
description: Close [location] camera (控制车辆关闭[location]相机功能)
---

## 功能说明
- 控制车辆关闭【位置】相机功能

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
        "position": "车前",
        "object": "摄像头",
        "object_raw": "相机",
        "action": "关闭"
    }
}
```

### 特殊参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `position` | string | 位置参数（主驾/副驾/一排/二排/三排/前排/后排/全车） | `主驾` |

### 参数说明

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `customInnerType` | string | customInnerType | `nativeCommand` |
| `position` | string | position | `车前` |
| `object` | string | object | `摄像头` |
| `object_raw` | string | object_raw | `相机` |
| `action` | string | action | `关闭` |

## 调用示例

### 示例 1
**用户输入**: 关闭车前相机

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "object": "摄像头",
        "action": "打开",
        "position": "后排"
    }
}
```

### 示例 2
**用户输入**: 打开后排相机

```json
{
    "api": "sys.car.crl",
    "param": {
        "customInnerType": "nativeCommand",
        "position": "车前",
        "object": "摄像头",
        "object_raw": "相机",
        "action": "关闭"
    }
}
```


## Implementation
com.flyme.superagent.agent.skills.impl.VehicleControlSkill
