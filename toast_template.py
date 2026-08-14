# -*- coding: utf-8 -*-
"""
ToastKit - Windows 全功能富通知模板
基于 Windows Toast 原生 XML，支持：标题栏 / 大图 / 图片 / 圆形裁剪 / 进度条(含动画) / 归属文本 / 按钮 / 循环声音 / 高优先级
默认值 = 演示版 V2 的实际效果，可通过参数覆盖。
"""
import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom

# ============ 默认配置（演示版 V2 实际值） ============
DEFAULTS = {
    # 基础
    "app_id": "Marvis.Notification",          # 应用名（AUMID）
    "title": "Marvis 全功能动效版 V2",        # 通知标题
    "message": "老板，新增：圆形裁剪图片 + 来电铃声，其余元素不变",  # 通知正文

    # 视觉
    "header_title": "Marvis 通知中心",        # 顶部标题栏（空=不显示）
    "hero_image": "file:///C:/Windows/Web/Wallpaper/Spotlight/img14.jpg",   # 顶部大图
    "inline_image": "file:///C:/Windows/Web/Wallpaper/ThemeA/img20.jpg",    # 正文图片
    "image_crop": "circle",                   # 图片裁剪: circle / round / none
    "progress_value": "indeterminate",        # 进度条: 0~1 或 indeterminate(动画)
    "progress_title": "处理中...",            # 进度条标题
    "progress_status": "正在处理",            # 进度条状态文本
    "attribution": "来自 Marvis 通知",        # 底部归属文本

    # 交互
    "actions": [                              # 按钮列表 [{label, launch}]
        {"label": "打开百度", "launch": "https://www.baidu.com"},
        {"label": "打开壁纸", "launch": "file:///C:/Windows/Web/Wallpaper/ThemeA/img20.jpg"},
        {"label": "关闭", "launch": "dismiss"},   # launch="dismiss" 表示系统关闭按钮
    ],
    "launch": "https://www.baidu.com",        # 点击通知默认跳转

    # 声音
    "audio": "call",                          # default / alarm / call / silent
    "audio_loop": True,                       # 是否循环播放

    # 行为
    "duration": "long",                       # short / long
    "scenario": "reminder",                   # default / reminder / alarm / incomingCall
    "priority": "high",                       # default / high
}

AUDIO_MAP = {
    "default": "ms-winsoundevent:Notification.Default",
    "alarm": "ms-winsoundevent:Notification.Looping.Alarm",
    "call": "ms-winsoundevent:Notification.Looping.Call",
    "silent": "silent",
}

PRIORITY_MAP = {
    "default": notifications.ToastNotificationPriority.DEFAULT,
    "high": notifications.ToastNotificationPriority.HIGH,
}


def build_xml(cfg):
    """根据配置构建 Toast XML 字符串"""
    parts = []
    toast_attrs = f'activationType="protocol" launch="{cfg["launch"]}" duration="{cfg["duration"]}"'
    if cfg.get("scenario") and cfg["scenario"] != "default":
        toast_attrs += f' scenario="{cfg["scenario"]}"'
    parts.append(f"<toast {toast_attrs}>")

    if cfg.get("header_title"):
        parts.append(f'<header id="headerId" title="{cfg["header_title"]}" arguments="dismiss"/>')

    parts.append('<visual><binding template="ToastGeneric">')
    parts.append(f'<text>{cfg["title"]}</text>')
    parts.append(f'<text>{cfg["message"]}</text>')

    if cfg.get("hero_image"):
        parts.append(f'<image placement="hero" src="{cfg["hero_image"]}"/>')

    if cfg.get("inline_image"):
        crop = f' hint-crop="{cfg["image_crop"]}"' if cfg.get("image_crop") and cfg["image_crop"] != "none" else ""
        parts.append(f'<image src="{cfg["inline_image"]}"{crop}/>')

    if cfg.get("progress_value"):
        parts.append(f'<progress title="{cfg["progress_title"]}" value="{cfg["progress_value"]}" status="{cfg["progress_status"]}"/>')

    if cfg.get("attribution"):
        parts.append(f'<text placement="attribution">{cfg["attribution"]}</text>')

    parts.append("</binding></visual>")

    if cfg.get("actions"):
        parts.append("<actions>")
        for act in cfg["actions"]:
            if act["launch"] == "dismiss":
                parts.append(f'<action content="{act["label"]}" activationType="system" arguments="dismiss"/>')
            else:
                parts.append(f'<action content="{act["label"]}" activationType="protocol" arguments="{act["launch"]}"/>')
        parts.append("</actions>")

    audio = AUDIO_MAP.get(cfg.get("audio", "default"), AUDIO_MAP["default"])
    if audio == "silent":
        parts.append('<audio silent="true"/>')
    else:
        loop = ' loop="true"' if cfg.get("audio_loop") else ""
        parts.append(f'<audio src="{audio}"{loop}/>')

    parts.append("</toast>")
    return "".join(parts)


def send_toast(**overrides):
    """发送富通知。传入字段覆盖默认值，未传字段用默认值。"""
    cfg = {**DEFAULTS, **overrides}
    xml = build_xml(cfg)

    notifier = notifications.ToastNotificationManager.create_toast_notifier(cfg["app_id"])
    doc = dom.XmlDocument()
    doc.load_xml(xml)
    toast = notifications.ToastNotification(doc)
    toast.tag = "marvis-toast"
    toast.group = "marvis"
    toast.priority = PRIORITY_MAP.get(cfg.get("priority", "default"), notifications.ToastNotificationPriority.DEFAULT)
    notifier.show(toast)
    return xml


if __name__ == "__main__":
    # 默认效果（演示版 V2）
    send_toast()
    print("已发送默认富通知")
