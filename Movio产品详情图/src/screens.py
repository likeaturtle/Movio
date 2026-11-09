# -*- coding: utf-8 -*-
"""Screen content for the Movio Taobao detail page. All copy is derived from
《Movio_产品说明书》 and 《Movio_快速上手指南》."""

W = 750

def nav(light=False, right="SEAMLESS KVM · 双机键鼠切换器"):
    return f'''<div class="pad rel" style="padding-top:44px">
  <div class="nav">
    <div class="wordmark">MOVIO</div>
    <div class="meta">{right}</div>
  </div>
</div>'''

def head(no, tag, title, lead=None, size=None):
    s = f'font-size:{size}px;' if size else ''
    out = f'''<div class="pad rel" style="margin-top:56px">
  <div class="kicker">{no} — {tag}</div>
  <h2 style="margin-top:22px;{s}">{title}</h2>'''
    if lead:
        out += f'<p class="lead" style="margin-top:24px">{lead}</p>'
    return out + '</div>'

def kbd(*keys, cls=""):
    parts = []
    for i, k in enumerate(keys):
        if i: parts.append('<span class="plus">+</span>')
        parts.append(f'<span class="kbd {cls}">{k}</span>')
    return '<div class="keyrow">' + "".join(parts) + '</div>'

def screen(slug, height, body, cls="", css=""):
    return dict(slug=slug, height=height, body=f'<div class="screen {cls}" style="height:{height}px">{body}</div>', css=css)

S = []

# ------------------------------------------------------------------ 01 cover
S.append(screen("00_封面", 1000, f'''
{nav(right="OPEN-SOURCE HARDWARE")}
<div style="position:absolute;left:0;right:0;top:0;height:780px;background:radial-gradient(640px 420px at 86% 2%, rgba(255,106,0,.15), rgba(255,106,0,0) 64%)"></div>
<div class="pad rel" style="margin-top:62px">
  <div style="display:inline-flex;align-items:center;gap:12px;font-size:18px;letter-spacing:.2em;color:#FF6A00;font-weight:600">
    <span class="dot"></span>双机键鼠切换器 · SEAMLESS KVM
  </div>
  <h2 style="font-size:84px;line-height:1.16;margin-top:30px;letter-spacing:-2.5px;font-weight:600">
    一套键鼠<br><span class="accent">两台电脑</span>
  </h2>
  <p style="margin-top:30px;font-size:27px;line-height:1.7;color:#565D66;letter-spacing:.02em">
    鼠标穿屏 · 键盘跟随 · 免安装任何软件
  </p>
  <div style="display:flex;gap:10px;margin-top:34px">
    <span class="tag">双 RP2040</span><span class="tag">2kV 隔离</span><span class="tag">免驱</span><span class="tag">开源硬件</span>
  </div>
</div>
<div class="pad rel" style="position:absolute;left:0;right:0;bottom:36px">
  <div class="photo" style="height:398px;border:1px solid #E9E1D5;box-shadow:0 18px 44px rgba(120,88,56,.12)">
    <img src="../assets/hero_render.jpg" style="object-position:56% 48%">
  </div>
</div>
'''))

# ------------------------------------------------------------------ 02 pain
S.append(screen("01_痛点", 960, f'''
{nav()}
{head("01", "先看一个日常", '桌面上，<br>永远多出的一套键鼠。',
      '两台电脑，往往意味着两套外设、两条线，以及每天几十次“伸手换设备”的动作。')}
<div class="pad rel" style="margin-top:44px;display:flex;gap:20px">
  <div style="width:308px;background:#EFE8DD;border-radius:18px;padding:28px 26px 26px">
    <div style="font-size:18px;letter-spacing:.18em;color:#8E867A;font-weight:600">过去 · 两套外设</div>
    <div style="margin-top:22px;font-size:22px;line-height:1.55;color:#6B645A">
      <div style="padding:14px 0;border-top:1px solid #E0D6C6">两套键盘，两个鼠标</div>
      <div style="padding:14px 0;border-top:1px solid #E0D6C6">抬手换一套设备</div>
      <div style="padding:14px 0;border-top:1px solid #E0D6C6">桌面被线材占满</div>
      <div style="padding:14px 0;border-top:1px solid #E0D6C6">每次切换使用不同键鼠</div>
    </div>
  </div>
  <div style="width:308px;background:#fff;border:1px solid #FFD6B8;border-radius:18px;padding:28px 26px 26px;box-shadow:0 10px 30px rgba(255,106,0,.08)">
    <div style="font-size:18px;letter-spacing:.18em;color:#FF6A00;font-weight:600">现在 · 一套键鼠</div>
    <div style="margin-top:22px;font-size:22px;line-height:1.55;color:#2C3138;font-weight:500">
      <div style="padding:14px 0;border-top:1px solid #F2E7DC">一套键盘，一个鼠标</div>
      <div style="padding:14px 0;border-top:1px solid #F2E7DC">光标推过屏幕边缘</div>
      <div style="padding:14px 0;border-top:1px solid #F2E7DC">一台巴掌大的小盒子</div>
      <div style="padding:14px 0;border-top:1px solid #F2E7DC">键盘跟着光标走，不用找</div>
    </div>
  </div>
</div>
<div class="pad rel" style="margin-top:34px">
  <p class="small">Movio 解决的问题很具体：<span style="color:#15171C">让两台电脑共用同一套键盘和鼠标</span>，并且切换时不打断你手上的动作。</p>
</div>
'''))

# ------------------------------------------------------------------ 03 definition
S.append(screen("02_产品定义", 990, f'''
{nav()}
{head("02", "产品定义", '把两台电脑，<br>用成一台。',
      'Movio 通过一套键鼠控制两台电脑。它不采集视频信号，也不需要在任何一台电脑上安装软件——插上，就能用。')}
<div class="pad rel" style="margin-top:30px;display:flex;gap:10px">
  <span class="tag">无需驱动</span><span class="tag">无需软件</span><span class="tag">不采集画面</span><span class="tag">本地运行</span>
</div>
<div class="pad rel" style="margin-top:56px">
<div style="position:relative;height:296px">
  <div style="position:absolute;left:0;top:36px;width:278px;height:184px;border:2px solid #2F3A45;border-radius:14px;background:#fff;padding:9px">
    <div style="width:100%;height:100%;border-radius:7px;background:#F1EDE6;display:flex;align-items:flex-end;justify-content:center;padding-bottom:16px;font-size:21px;color:#8A8F97;letter-spacing:.1em">B 主屏</div>
  </div>
  <div style="position:absolute;right:0;top:36px;width:278px;height:184px;border:2px solid #FF6A00;border-radius:14px;background:#fff;padding:9px">
    <div style="width:100%;height:100%;border-radius:7px;background:#FFF1E6;display:flex;align-items:flex-end;justify-content:center;padding-bottom:16px;font-size:21px;color:#C56A2C;letter-spacing:.1em">A 主屏</div>
  </div>
  <div style="position:absolute;left:50%;top:36px;height:184px;border-left:2px dashed #FF6A00"></div>
  <div style="position:absolute;left:50%;top:0;transform:translateX(-50%);background:#FF6A00;color:#fff;font-size:15px;letter-spacing:.1em;padding:4px 13px;border-radius:11px;white-space:nowrap">共享边缘</div>
  <div style="position:absolute;left:66px;right:80px;top:128px;border-top:2px dashed rgba(255,106,0,.5)"></div>
  <div style="position:absolute;left:66px;top:120px;width:0;height:0;border-top:9px solid transparent;border-bottom:9px solid transparent;border-right:13px solid rgba(255,106,0,.8)"></div>
  <div style="position:absolute;left:430px;top:104px">
    <svg width="30" height="34" viewBox="0 0 24 24"><path d="M4 2 L20 12 L12.6 13.4 L16.6 21 L13.6 22.5 L9.6 15 L4 20 Z" fill="#15171C" stroke="#fff" stroke-width="1.6"/></svg>
  </div>
  <div style="position:absolute;left:0;top:240px;width:278px;text-align:center;font-size:18px;color:#8A8F97">电脑 B（左侧）</div>
  <div style="position:absolute;right:0;top:240px;width:278px;text-align:center;font-size:18px;color:#8A8F97">电脑 A（右侧 · 默认活动输出）</div>
</div>
</div>
<div class="pad rel" style="margin-top:6px">
  <p class="caption">默认布局为 A 在右、B 在左；光标推过共享边缘即完成切换，键盘输入同时跟随。屏幕位置只支持左右，不支持上下堆叠。</p>
</div>
'''))

# ------------------------------------------------------------------ 04 not a video KVM
S.append(screen("03_不是视频KVM", 860, f'''
{nav()}
{head("03", "产品边界", '它不是视频 KVM。',
      '显示器、音箱、摄像头、移动硬盘，仍然直连各自的电脑。Movio 只负责键盘和鼠标。')}
<div class="pad rel" style="margin-top:42px;display:flex;gap:20px">
  <div style="width:308px;background:#fff;border:1px solid #E5DCCF;border-radius:18px;padding:26px">
    <div style="display:flex;align-items:center;gap:10px;font-size:19px;font-weight:600;color:#8A8F97;letter-spacing:.06em">
      <span style="width:26px;height:26px;border-radius:50%;background:#EFE9E0;color:#9C9488;display:inline-flex;align-items:center;justify-content:center;font-size:16px">✕</span>不经过 Movio
    </div>
    <div style="margin-top:18px;font-size:22px;line-height:1.5;color:#5C636B">
      <div style="padding:12px 0;border-top:1px solid #EFE8DD">视频 / 画面</div>
      <div style="padding:12px 0;border-top:1px solid #EFE8DD">音频</div>
      <div style="padding:12px 0;border-top:1px solid #EFE8DD">USB 存储、摄像头</div>
    </div>
  </div>
  <div style="width:308px;background:#fff;border:1px solid #FFD6B8;border-radius:18px;padding:26px">
    <div style="display:flex;align-items:center;gap:10px;font-size:19px;font-weight:600;color:#FF6A00;letter-spacing:.06em">
      <span style="width:26px;height:26px;border-radius:50%;background:#FF6A00;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:15px">✓</span>由 Movio 切换
    </div>
    <div style="margin-top:18px;font-size:22px;line-height:1.5;color:#2C3138">
      <div style="padding:12px 0;border-top:1px solid #F4E9DE">键盘输入</div>
      <div style="padding:12px 0;border-top:1px solid #F4E9DE">鼠标输入</div>
      <div style="padding:12px 0;border-top:1px solid #F4E9DE">跨机切换与快捷键</div>
    </div>
  </div>
</div>
<div class="rel" style="margin:30px 56px 0;background:#F6EDE2;border-radius:16px;padding:26px 28px">
  <p style="font-size:22px;line-height:1.8;color:#4C525A">
    画面不经过 Movio，因此<span style="color:#15171C;font-weight:600">不影响分辨率、刷新率、HDR 与色彩</span>；两台电脑的显示器各接各的，音视频互不干扰。
  </p>
</div>
'''))

# ------------------------------------------------------------------ 05 support matrix
S.append(screen("04_支持与不支持", 1450, f'''
{nav()}
{head("04", "能力清单", '能做什么，<br>不能做什么。',
      '一张清单看清边界：六条支持，五条不支持。买之前，先确认与你的使用场景一致。')}
<div class="rel" style="margin:34px 56px 0">
  <div style="display:flex;align-items:center;gap:10px">
    <span style="width:26px;height:26px;border-radius:50%;background:#FF6A00;color:#fff;font-size:15px;display:inline-flex;align-items:center;justify-content:center;flex:none">✓</span>
    <span style="font-size:23px;font-weight:600">支持</span>
    <span style="font-size:15px;color:#A79F93;letter-spacing:.12em">6 项</span>
  </div>
  <div class="card" style="margin-top:14px;padding:4px 24px">
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #EFE8DD">
      <span class="num" style="font-size:14px;color:#FF6A00;width:20px;flex:none">01</span>
      <span style="font-size:20px;line-height:1.5;color:#22262C">双机键盘鼠标穿越</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #EFE8DD">
      <span class="num" style="font-size:14px;color:#FF6A00;width:20px;flex:none">02</span>
      <span style="font-size:20px;line-height:1.5;color:#22262C">Windows / macOS / Linux / Android</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #EFE8DD">
      <span class="num" style="font-size:14px;color:#FF6A00;width:20px;flex:none">03</span>
      <span style="font-size:20px;line-height:1.5;color:#22262C">鼠标最高 1000Hz 回报率</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #EFE8DD">
      <span class="num" style="font-size:14px;color:#FF6A00;width:20px;flex:none">04</span>
      <span style="font-size:20px;line-height:1.5;color:#22262C">部分键盘鼠标支持自定义按键</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #EFE8DD">
      <span class="num" style="font-size:14px;color:#FF6A00;width:20px;flex:none">05</span>
      <span style="font-size:20px;line-height:1.5;color:#22262C">二合一键盘鼠标接收器<br><span style="color:#6B7178">含罗技 Unifying 优联接收器</span></span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0">
      <span class="num" style="font-size:14px;color:#FF6A00;width:20px;flex:none">06</span>
      <span style="font-size:20px;line-height:1.5;color:#22262C">办公及日常使用</span>
    </div>
  </div>
</div>
<div class="rel" style="margin:26px 56px 0">
  <div style="display:flex;align-items:center;gap:10px">
    <span style="width:26px;height:26px;border-radius:50%;background:#E6DED2;color:#8C857A;font-size:14px;display:inline-flex;align-items:center;justify-content:center;flex:none">✕</span>
    <span style="font-size:23px;font-weight:600">不支持</span>
    <span style="font-size:15px;color:#A79F93;letter-spacing:.12em">5 项</span>
  </div>
  <div style="margin-top:14px;background:#EFE8DD;border:1px solid #E2D9CB;border-radius:18px;padding:4px 24px">
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #E2D9CB">
      <span class="num" style="font-size:14px;color:#9C9488;width:20px;flex:none">01</span>
      <span style="font-size:20px;line-height:1.5;color:#5F594F">跨机复制粘贴</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #E2D9CB">
      <span class="num" style="font-size:14px;color:#9C9488;width:20px;flex:none">02</span>
      <span style="font-size:20px;line-height:1.5;color:#5F594F">文件拖拽跨屏</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #E2D9CB">
      <span class="num" style="font-size:14px;color:#9C9488;width:20px;flex:none">03</span>
      <span style="font-size:20px;line-height:1.5;color:#5F594F">高于 1000Hz 回报率的鼠标</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0;border-bottom:1px solid #E2D9CB">
      <span class="num" style="font-size:14px;color:#9C9488;width:20px;flex:none">04</span>
      <span style="font-size:20px;line-height:1.5;color:#5F594F">蓝牙键盘鼠标</span>
    </div>
    <div style="display:flex;gap:14px;align-items:baseline;padding:16px 0">
      <span class="num" style="font-size:14px;color:#9C9488;width:20px;flex:none">05</span>
      <span style="font-size:20px;line-height:1.5;color:#5F594F">游戏及对操作精度、延迟要求极高的场景</span>
    </div>
  </div>
</div>
<div class="rel" style="margin:24px 56px 0">
  <p class="caption">回报率指鼠标的 USB 轮询率；实际表现与键鼠型号、系统版本相关，键鼠需为 USB 有线或带 USB 接收器。</p>
</div>
'''))
# ------------------------------------------------------------------ 05 wiring
S.append(screen("05_接线", 1200, f'''
{nav()}
{head("05", "接线", '四根线，<br>十分钟完成第一次穿屏。',
      '两根 USB-C 数据线接电脑，键盘和鼠标接两个 USB-A 口。方向只有一个：键鼠进，电脑出。')}
<div class="pad rel" style="margin-top:34px;display:grid;grid-template-columns:1fr 1fr;gap:16px">
  <div class="card" style="padding:24px 24px 22px">
    <div class="num" style="font-size:17px;color:#FF6A00;letter-spacing:.14em">01</div>
    <div style="font-size:24px;font-weight:600;margin-top:8px">连接键盘</div>
    <div style="font-size:20px;line-height:1.65;color:#5C636B;margin-top:8px">插入带键盘图标的 USB-A 口；无线键盘把接收器插在这里。</div>
  </div>
  <div class="card" style="padding:24px 24px 22px">
    <div class="num" style="font-size:17px;color:#FF6A00;letter-spacing:.14em">02</div>
    <div style="font-size:24px;font-weight:600;margin-top:8px">连接鼠标</div>
    <div style="font-size:20px;line-height:1.65;color:#5C636B;margin-top:8px">插入带鼠标图标的 USB-A 口；键鼠合一接收器插任一口通常都可以。</div>
  </div>
  <div class="card" style="padding:24px 24px 22px">
    <div class="num" style="font-size:17px;color:#FF6A00;letter-spacing:.14em">03</div>
    <div style="font-size:24px;font-weight:600;margin-top:8px">A 端 → 电脑 A</div>
    <div style="font-size:20px;line-height:1.65;color:#5C636B;margin-top:8px">用一根 USB-C 数据线连接 A 端与电脑 A 的 USB 口。</div>
  </div>
  <div class="card" style="padding:24px 24px 22px">
    <div class="num" style="font-size:17px;color:#FF6A00;letter-spacing:.14em">04</div>
    <div style="font-size:24px;font-weight:600;margin-top:8px">B 端 → 电脑 B</div>
    <div style="font-size:20px;line-height:1.65;color:#5C636B;margin-top:8px">用另一根 USB-C 数据线连接 B 端与电脑 B 的 USB 口。</div>
  </div>
</div>
<div class="pad rel" style="margin-top:24px">
  <div style="border-left:3px solid #FF6A00;padding-left:20px">
    <p style="font-size:20px;line-height:1.8;color:#565D66">
      两根线都必须支持数据传输——仅充电线无法建立 USB 连接；A / B 两路分别由对应电脑供电，<span style="color:#15171C;font-weight:600">两台电脑都要开机</span>。
    </p>
  </div>
</div>
<div class="pad rel" style="margin-top:30px">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <div style="width:164px">
      <div style="height:46px;border:1px solid #E5DCCF;background:#fff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#4E545C">键盘 · USB-A</div>
      <div style="height:46px;border:1px solid #E5DCCF;background:#fff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#4E545C;margin-top:10px">鼠标 · USB-A</div>
    </div>
    <div style="width:38px;text-align:center;color:#FF6A00;font-size:20px">→</div>
    <div style="width:184px;height:120px;border:2px solid #FF6A00;border-radius:14px;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px">
      <div style="font-family:'Avenir Next';font-size:17px;letter-spacing:.24em;color:#15171C">MOVIO</div>
      <div style="font-size:15px;color:#8A8F97">双机键鼠切换</div>
    </div>
    <div style="width:38px;text-align:center;color:#FF6A00;font-size:20px">→</div>
    <div style="width:164px">
      <div style="height:46px;border:1px solid #E5DCCF;background:#fff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#4E545C">电脑 A · A 端</div>
      <div style="height:46px;border:1px solid #E5DCCF;background:#fff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#4E545C;margin-top:10px">电脑 B · B 端</div>
    </div>
  </div>
  <div class="caption" style="text-align:center">键鼠进，电脑出：USB-A 是主机输入口，A / B 端是设备输出口。</div>
</div>
'''))

# ------------------------------------------------------------------ 06 interactions
S.append(screen("06_三种操作", 1215, f'''
{nav()}
{head("06", "交互", '三种切换方式，<br>覆盖日常全部场景。',
      '不需要记复杂的组合——最自然的方式，就是把光标推过去。')}
<div class="pad rel" style="margin-top:40px">
  <div style="display:flex;gap:22px;align-items:flex-start;padding:26px 0;border-top:1px solid #E6DED2">
    <div class="num" style="width:64px;font-size:44px;color:#E8DFD2;line-height:1;padding-top:4px">01</div>
    <div style="flex:1">
      <div style="font-size:28px;font-weight:600">鼠标穿屏<span style="font-size:18px;font-weight:400;color:#FF6A00;margin-left:10px">默认</span></div>
      <p style="font-size:21px;line-height:1.7;color:#5C636B;margin-top:8px">光标移到屏幕边缘继续外推，就会出现在另一台电脑上，键盘同时跟随。不用按键，也不用手动切换。</p>
    </div>
  </div>
  <div style="display:flex;gap:22px;align-items:flex-start;padding:26px 0;border-top:1px solid #E6DED2">
    <div class="num" style="width:64px;font-size:44px;color:#E8DFD2;line-height:1;padding-top:4px">02</div>
    <div style="flex:1">
      <div style="font-size:28px;font-weight:600">快捷键切换</div>
      <p style="font-size:21px;line-height:1.7;color:#5C636B;margin-top:8px">不必移动光标，直接把键鼠整体切到另一台；切换瞬间会释放所有按键，避免按键“卡”在另一台电脑上。</p>
      <div style="margin-top:14px">{kbd("左 Ctrl", "Caps Lock")}</div>
    </div>
  </div>
  <div style="display:flex;gap:22px;align-items:flex-start;padding:26px 0;border-top:1px solid #E6DED2;border-bottom:1px solid #E6DED2">
    <div class="num" style="width:64px;font-size:44px;color:#E8DFD2;line-height:1;padding-top:4px">03</div>
    <div style="flex:1">
      <div style="font-size:28px;font-weight:600">临时锁定</div>
      <p style="font-size:21px;line-height:1.7;color:#5C636B;margin-top:8px">需要在一台电脑上专注时，禁止鼠标穿屏和快捷键切换；再按一次解锁，重启后自动失效。</p>
      <div style="margin-top:14px">{kbd("右 Ctrl", "K")}</div>
    </div>
  </div>
</div>
<div class="pad rel" style="margin-top:22px">
  <p class="caption">在共享边缘按住鼠标按键时，跨电脑切换会被阻止——避免拖拽窗口或文件时误切换。</p>
</div>
'''))

# ------------------------------------------------------------------ 07 hardware
S.append(screen("07_硬件", 1490, f'''
{nav()}
{head("07", "硬件", '两颗 RP2040，<br>一条 2kV 隔离带。',
      '两颗芯片分别面向一台电脑，通过 UART 心跳通信；信号侧做 2kV 数字隔离，各自独立供电。')}
<div class="pad rel" style="margin-top:28px">
  <div class="photo" style="height:352px;border:1px solid #E9E1D5;box-shadow:0 12px 30px rgba(120,88,56,.10)"><img src="../assets/pcb.jpg" style="object-position:50% 50%"></div>
</div>
<div class="pad rel" style="margin-top:14px">
  <div class="photo" style="height:228px;border:1px solid #E9E1D5;box-shadow:0 12px 30px rgba(120,88,56,.10)"><img src="../assets/ports_front.jpg" style="object-position:50% 64%"></div>
  <p class="caption">正面视角：A / B 端（3、4）接电脑；4 个圆孔中，上方两个为状态 LED（6），下方两个为 BOOTSEL 按键（5）。按住 BOOTSEL 再插入 USB-C，可进入 RPI-RP2 引导模式。</p>
</div>
<div class="pad rel" style="margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:7px 24px">
  <div style="display:flex;gap:12px;align-items:baseline;font-size:18px;color:#4A5058"><span class="num" style="color:#FF6A00;font-size:16px">1</span>键盘 USB-A 口</div>
  <div style="display:flex;gap:12px;align-items:baseline;font-size:18px;color:#4A5058"><span class="num" style="color:#FF6A00;font-size:16px">2</span>鼠标 USB-A 口</div>
  <div style="display:flex;gap:12px;align-items:baseline;font-size:18px;color:#4A5058"><span class="num" style="color:#FF6A00;font-size:16px">3</span>A 端电脑连接</div>
  <div style="display:flex;gap:12px;align-items:baseline;font-size:18px;color:#4A5058"><span class="num" style="color:#FF6A00;font-size:16px">4</span>B 端电脑连接</div>
  <div style="display:flex;gap:12px;align-items:baseline;font-size:18px;color:#4A5058"><span class="num" style="color:#FF6A00;font-size:16px">5</span>BOOTSEL 按键 ×2</div>
  <div style="display:flex;gap:12px;align-items:baseline;font-size:18px;color:#4A5058"><span class="num" style="color:#FF6A00;font-size:16px">6</span>板载状态 LED ×2</div>
  <div style="display:flex;gap:12px;align-items:baseline;font-size:18px;color:#4A5058"><span class="num" style="color:#FF6A00;font-size:16px">7</span>板载电源 LED ×2</div>
</div>
<div class="pad rel" style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap">
  <span class="tag">双 RP2040</span><span class="tag">UART + 2kV 隔离</span><span class="tag">USB-C ×2</span><span class="tag">USB-A ×2</span><span class="tag">无独立电源</span>
</div>
<div class="pad rel" style="margin-top:14px"><p class="caption">主板与外壳为示意图，实物以最终版本为准。</p></div>
'''))

# ------------------------------------------------------------------ 08 compatibility
S.append(screen("08_兼容", 1110, f'''
{nav()}
{head("08", "兼容", '标准 USB HID，<br>插上就是键鼠。',
      '电脑把 Movio 识别为标准 HID 键鼠设备：不装驱动，也不会多出磁盘、网卡或未知设备。')}
<div class="pad rel" style="margin-top:34px">
  <div class="rows">
    <div class="row" style="padding:16px 0">
      <div style="width:210px;font-size:21px;font-weight:600;color:#2C3138">Windows 10 / 11</div>
      <div style="width:86px;font-size:19px;color:#FF6A00">支持</div>
      <div style="flex:1;font-size:19px;line-height:1.6;color:#6B7178">多屏使用兼容模式</div>
    </div>
    <div class="row" style="padding:16px 0">
      <div style="width:210px;font-size:21px;font-weight:600;color:#2C3138">macOS</div>
      <div style="width:86px;font-size:19px;color:#FF6A00">支持</div>
      <div style="flex:1;font-size:19px;line-height:1.6;color:#6B7178">多屏为实验性；锁定快捷键 Ctrl + Cmd + Q</div>
    </div>
    <div class="row" style="padding:16px 0">
      <div style="width:210px;font-size:21px;font-weight:600;color:#2C3138">Linux</div>
      <div style="width:86px;font-size:19px;color:#FF6A00">支持</div>
      <div style="flex:1;font-size:19px;line-height:1.6;color:#6B7178">多屏建议屏幕数量设为 1，由桌面环境管理</div>
    </div>
    <div class="row" style="padding:16px 0">
      <div style="width:210px;font-size:21px;font-weight:600;color:#2C3138">Android</div>
      <div style="width:86px;font-size:19px;color:#FF6A00">支持</div>
      <div style="flex:1;font-size:19px;line-height:1.6;color:#6B7178">需要 OTG；建议单屏，必要时用游戏模式</div>
    </div>
    <div class="row" style="padding:16px 0">
      <div style="width:210px;font-size:21px;font-weight:600;color:#2C3138">BIOS / UEFI<br>BitLocker</div>
      <div style="width:86px;font-size:19px;color:#FF6A00">视主板</div>
      <div style="flex:1;font-size:19px;line-height:1.6;color:#6B7178">部分主板需开启“强制键盘启动协议”</div>
    </div>
  </div>
</div>
<div class="rel" style="margin:28px 56px 0;background:#F6EDE2;border-radius:16px;padding:24px 26px">
  <p style="font-size:20px;line-height:1.8;color:#555C64">
    未列出的系统（iOS / iPadOS、ChromeOS 等）未经验证，不建议依赖。视频不经过 Movio，因此不影响分辨率、刷新率、HDR 与色彩。
  </p>
</div>
'''))

# ------------------------------------------------------------------ 09 hotkeys
S.append(screen("09_快捷键", 1370, f'''
{nav()}
{head("09", "快捷键", '十一个组合键，<br>记住三个就够用。',
      '全部由键盘直接触发，不装驱动；除“慢速鼠标”外，组合都会被 Movio 拦截，不会输入到电脑。')}
<div class="pad rel" style="margin-top:38px">
  <div style="font-size:18px;letter-spacing:.18em;color:#FF6A00;font-weight:600">配置类 · 进入设置与校准</div>
  <div style="margin-top:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;padding:14px 0;border-top:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">进入 / 退出配置模式</div>
      {kbd("左 Ctrl", "右 Shift", "C", "O", cls="sm")}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;padding:14px 0;border-top:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">重置配置（无二次确认）</div>
      {kbd("右 Shift", "F12", "D", cls="sm")}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;padding:14px 0;border-top:1px solid #E6DED2;border-bottom:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">保存屏幕高度</div>
      {kbd("右 Shift", "F12", "Y", cls="sm")}
    </div>
  </div>
  <div style="font-size:18px;letter-spacing:.18em;color:#FF6A00;font-weight:600;margin-top:34px">使用类 · 日常操作</div>
  <div style="margin-top:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;padding:13px 0;border-top:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">切换输出</div>
      {kbd("左 Ctrl", "Caps Lock", cls="sm")}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;padding:13px 0;border-top:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">游戏模式</div>
      {kbd("左 Ctrl", "右 Shift", "G", cls="sm")}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;padding:13px 0;border-top:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">慢速鼠标</div>
      {kbd("右 Ctrl", "右 Alt", cls="sm")}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;padding:13px 0;border-top:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">切换锁定</div>
      {kbd("右 Ctrl", "K", cls="sm")}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;padding:13px 0;border-top:1px solid #E6DED2">
      <div style="font-size:21px;color:#2C3138">锁定两台电脑</div>
      {kbd("右 Ctrl", "L", cls="sm")}
    </div>
  </div>
  <div style="margin-top:18px;padding:16px 18px;border:1px dashed #DED3C3;border-radius:12px;background:#FFFFFF;font-size:18px;line-height:1.7;color:#6B7178">
    屏幕保护另有三个组合：<b style="color:#22262C;font-weight:500">左 Ctrl + 右 Shift + S / J / X</b>（弹球 / 抖动 / 关闭），只对当前活动输出生效，不写入 Flash。
  </div>
</div>
<div class="pad rel" style="margin-top:24px"><p class="caption">快捷键目前不能在 Web 配置页中修改；如需更改，需要在源码 user_config.h 中重新定义并编译固件。</p></div>
'''))

# ------------------------------------------------------------------ 10 config page
S.append(screen("10_配置页", 1250, f'''
{nav()}
{head("10", "配置", '配置，在一个<br>不联网的网页里。',
      '配置页是随设备提供的一个本地 HTML 文件，通过 WebHID 直接读写设备，不加载外部脚本，也不上传任何数据。')}
<div class="pad rel" style="margin-top:30px">
  <div style="border:1px solid #E4DBCE;border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 14px 34px rgba(90,70,45,.10)">
    <div style="height:46px;background:#F4EFE7;border-bottom:1px solid #E7DFD3;display:flex;align-items:center;padding:0 16px;gap:8px">
      <span style="width:10px;height:10px;border-radius:50%;background:#E0D5C5"></span>
      <span style="width:10px;height:10px;border-radius:50%;background:#E0D5C5"></span>
      <span style="width:10px;height:10px;border-radius:50%;background:#E0D5C5"></span>
      <div style="flex:1;margin-left:14px;height:26px;border-radius:13px;background:#fff;border:1px solid #E7DFD3;display:flex;align-items:center;padding:0 12px;font-size:14px;color:#9A938A;letter-spacing:.04em">MOVIO 盘 / config.htm　·　Chrome WebHID</div>
    </div>
    <div style="height:470px;overflow:hidden;position:relative">
      <img src="../assets/config_page_small.jpg" style="width:100%;display:block;margin-top:-6px">
      <div style="position:absolute;left:0;right:0;bottom:0;height:70px;background:linear-gradient(180deg,rgba(255,255,255,0),#fff)"></div>
    </div>
  </div>
</div>
<div class="pad rel" style="margin-top:26px">
  <div style="display:flex;gap:16px;padding:13px 0;border-top:1px solid #E6DED2"><span style="width:92px;font-size:19px;font-weight:600;color:#15171C;white-space:nowrap;flex:none">完全本地</span><span style="font-size:19px;line-height:1.6;color:#565D66">不联网、不加载外部脚本、不上传配置</span></div>
  <div style="display:flex;gap:16px;padding:13px 0;border-top:1px solid #E6DED2"><span style="width:92px;font-size:19px;font-weight:600;color:#15171C;white-space:nowrap;flex:none">即时下发</span><span style="font-size:19px;line-height:1.6;color:#565D66">改值立刻生效，点击“保存”才写入 Flash</span></div>
  <div style="display:flex;gap:16px;padding:13px 0;border-top:1px solid #E6DED2"><span style="width:92px;font-size:19px;font-weight:600;color:#15171C;white-space:nowrap;flex:none">自动退出</span><span style="font-size:19px;line-height:1.6;color:#565D66">约 5 分钟无操作自动重启回正常模式</span></div>
  <div style="display:flex;gap:16px;padding:13px 0;border-top:1px solid #E6DED2;border-bottom:1px solid #E6DED2"><span style="width:92px;font-size:19px;font-weight:600;color:#15171C;white-space:nowrap;flex:none">浏览器</span><span style="font-size:19px;line-height:1.6;color:#565D66">仅 Chrome / Chromium / Edge 支持 WebHID</span></div>
</div>
'''))

# ------------------------------------------------------------------ 11 four features
S.append(screen("11_四个功能", 1160, f'''
{nav()}
{head("11", "日常功能", '四个不显眼，<br>但每天都会用到的功能。',
      '它们都不需要额外软件，用快捷键就能随时开关。')}
<div class="pad rel" style="margin-top:38px;display:grid;grid-template-columns:1fr 1fr;gap:16px">
  <div class="card" style="padding:24px">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div style="font-size:23px;font-weight:600">游戏模式</div>
      <div style="font-size:14px;color:#FF6A00;letter-spacing:.1em">GAME</div>
    </div>
    <div style="margin-top:12px">{kbd("左 Ctrl", "右 Shift", "G", cls="sm")}</div>
    <p style="font-size:19px;line-height:1.7;color:#5C636B;margin-top:12px">鼠标切为相对模式，到边缘不再穿屏；适合游戏、虚拟机、远程桌面。</p>
  </div>
  <div class="card" style="padding:24px">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div style="font-size:23px;font-weight:600">慢速鼠标</div>
      <div style="font-size:14px;color:#FF6A00;letter-spacing:.1em">PRECISE</div>
    </div>
    <div style="margin-top:12px">{kbd("右 Ctrl", "右 Alt", cls="sm")}</div>
    <p style="font-size:19px;line-height:1.7;color:#5C636B;margin-top:12px">速度约为原来的 1/4，适合精确拖动时间轴、修图、绘图。</p>
  </div>
  <div class="card" style="padding:24px">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div style="font-size:23px;font-weight:600">切换锁定</div>
      <div style="font-size:14px;color:#FF6A00;letter-spacing:.1em">HOLD</div>
    </div>
    <div style="margin-top:12px">{kbd("右 Ctrl", "K", cls="sm")}</div>
    <p style="font-size:19px;line-height:1.7;color:#5C636B;margin-top:12px">临时禁止穿屏与快捷键切换，专注一台电脑；重启后失效。</p>
  </div>
  <div class="card" style="padding:24px">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div style="font-size:23px;font-weight:600">屏幕保护</div>
      <div style="font-size:14px;color:#FF6A00;letter-spacing:.1em">AWAKE</div>
    </div>
    <div style="margin-top:12px">{kbd("左 Ctrl", "右 Shift", "S", cls="sm")}</div>
    <p style="font-size:19px;line-height:1.7;color:#5C636B;margin-top:12px">发送极小的鼠标移动，防止休眠与锁屏；不点击、不按键。</p>
  </div>
</div>
<div class="pad rel" style="margin-top:26px">
  <div style="background:#fff;border:1px dashed #DED3C3;border-radius:14px;padding:20px 24px">
    <div style="font-size:15px;color:#FF6A00;letter-spacing:.12em;font-weight:600">屏幕保护还有三种模式</div>
    <div style="font-size:19px;line-height:1.7;color:#5C636B;margin-top:8px">弹球 <b style="font-weight:500;color:#15171C">左 Ctrl + 右 Shift + S</b>　·　抖动 <b style="font-weight:500;color:#15171C">+ J</b>　·　关闭 <b style="font-weight:500;color:#15171C">+ X</b>，只对当前输出生效，不写入 Flash。</div>
  </div>
</div>
'''))

# ------------------------------------------------------------------ 12 multi-screen
S.append(screen("12_多屏", 900, f'''
{nav()}
{head("12", "多屏", '只支持左右并排，<br>把主屏放在共享边缘。',
      '每台电脑的主屏紧邻另一台电脑，扩展屏向外侧延伸；不支持上下堆叠布局。')}
<div class="pad rel" style="margin-top:34px">
  <div style="display:flex;align-items:flex-end;gap:8px">
    <div style="width:98px;height:66px;border:1px solid #D8CDBD;border-radius:8px;background:#EFE8DD;display:flex;align-items:center;justify-content:center;font-size:15px;color:#8A8378">B3</div>
    <div style="width:98px;height:66px;border:1px solid #D8CDBD;border-radius:8px;background:#EFE8DD;display:flex;align-items:center;justify-content:center;font-size:15px;color:#8A8378">B2</div>
    <div style="width:98px;height:88px;border:2px solid #2F3A45;border-radius:8px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:15px;color:#2F3A45;font-weight:600">B1</div>
    <div style="width:8px;height:88px;display:flex;align-items:center;justify-content:center">
      <div style="width:2px;height:88px;border-left:2px dashed #FF6A00"></div>
    </div>
    <div style="width:98px;height:88px;border:2px solid #FF6A00;border-radius:8px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:15px;color:#C25A16;font-weight:600">A1</div>
    <div style="width:98px;height:66px;border:1px solid #FFD6B8;border-radius:8px;background:#FFF1E6;display:flex;align-items:center;justify-content:center;font-size:15px;color:#C58A5E">A2</div>
    <div style="width:98px;height:66px;border:1px solid #FFD6B8;border-radius:8px;background:#FFF1E6;display:flex;align-items:center;justify-content:center;font-size:15px;color:#C58A5E">A3</div>
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:10px;font-size:16px;color:#8A8F97">
    <div style="width:310px;text-align:center">电脑 B　扩展 · 扩展 · 主屏</div>
    <div style="width:310px;text-align:center">电脑 A　主屏 · 扩展 · 扩展</div>
  </div>
</div>
<div class="pad rel" style="margin-top:26px">
  <div style="display:flex;gap:16px">
    <div style="flex:1;border-top:2px solid #FF6A00;padding-top:14px">
      <div style="font-size:20px;font-weight:600">Windows / macOS</div>
      <p style="font-size:18px;line-height:1.7;color:#6B7178;margin-top:6px">多屏使用兼容模式，手感与单屏略有不同。</p>
    </div>
    <div style="flex:1;border-top:2px solid #2F3A45;padding-top:14px">
      <div style="font-size:20px;font-weight:600">Linux</div>
      <p style="font-size:18px;line-height:1.7;color:#6B7178;margin-top:6px">由桌面环境管理，屏幕数量建议设为 1。</p>
    </div>
  </div>
</div>
<div class="rel" style="margin:26px 56px 0;background:#F6EDE2;border-radius:16px;padding:24px 26px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <div style="font-size:21px;font-weight:600">显示器高度不一致？校准一次。</div>
      <p style="font-size:18px;line-height:1.7;color:#6B7178;margin-top:6px">把光标停在较小屏幕的顶边 / 底边高度，各按一次。</p>
    </div>
    {kbd("右 Shift", "F12", "Y", cls="sm")}
  </div>
</div>
'''))

# ------------------------------------------------------------------ 13 firmware
S.append(screen("13_固件升级", 1060, f'''
{nav()}
{head("13", "固件", '一个 UF2，<br>两颗芯片自动同步。',
      '两颗 RP2040 使用同一个 movio.uf2，芯片角色由硬件自动探测。只需写入一颗，另一颗会通过 UART 自动拉取并写入。')}
<div class="pad rel" style="margin-top:38px;display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px">
  <div style="background:#fff;border:1px solid #E9E1D5;border-radius:14px;padding:18px 14px">
    <div class="num" style="width:30px;height:30px;border-radius:15px;background:#FF6A00;color:#fff;font-size:15px;display:flex;align-items:center;justify-content:center">1</div>
    <div style="font-size:19px;font-weight:600;margin-top:12px;line-height:1.4">下载固件</div>
    <div style="font-size:16px;line-height:1.6;color:#7A8087;margin-top:6px">movio.uf2<br>核对版本</div>
  </div>
  <div style="background:#fff;border:1px solid #E9E1D5;border-radius:14px;padding:18px 14px">
    <div class="num" style="width:30px;height:30px;border-radius:15px;background:#FF6A00;color:#fff;font-size:15px;display:flex;align-items:center;justify-content:center">2</div>
    <div style="font-size:19px;font-weight:600;margin-top:12px;line-height:1.4">进入配置模式</div>
    <div style="font-size:16px;line-height:1.6;color:#7A8087;margin-top:6px">快捷键<br>C + O</div>
  </div>
  <div style="background:#fff;border:1px solid #E9E1D5;border-radius:14px;padding:18px 14px">
    <div class="num" style="width:30px;height:30px;border-radius:15px;background:#FF6A00;color:#fff;font-size:15px;display:flex;align-items:center;justify-content:center">3</div>
    <div style="font-size:19px;font-weight:600;margin-top:12px;line-height:1.4">复制固件</div>
    <div style="font-size:16px;line-height:1.6;color:#7A8087;margin-top:6px">拖入 MOVIO 盘<br>根目录</div>
  </div>
  <div style="background:#fff;border:1px solid #E9E1D5;border-radius:14px;padding:18px 14px">
    <div class="num" style="width:30px;height:30px;border-radius:15px;background:#2F3A45;color:#fff;font-size:15px;display:flex;align-items:center;justify-content:center">4</div>
    <div style="font-size:19px;font-weight:600;margin-top:12px;line-height:1.4">自动同步</div>
    <div style="font-size:16px;line-height:1.6;color:#7A8087;margin-top:6px">两颗芯片依次<br>写入并重启</div>
  </div>
</div>
<div class="pad rel" style="margin-top:28px">
  <div style="background:#F6EDE2;border-radius:16px;padding:24px 26px">
    <div style="display:flex;gap:12px;margin-bottom:10px"><span style="font-size:17px;color:#FF6A00;font-weight:600;letter-spacing:.1em;white-space:nowrap">只升级</span><p style="font-size:18px;line-height:1.7;color:#5C636B">自动同步只在“对方版本更新”时触发，不会降级。</p></div>
    <div style="display:flex;gap:12px;margin-bottom:10px"><span style="font-size:17px;color:#FF6A00;font-weight:600;letter-spacing:.1em;white-space:nowrap">救砖</span><p style="font-size:18px;line-height:1.7;color:#5C636B">全新主板或升级失败，按住 BOOTSEL 上电进入 RPI-RP2，分别刷写两颗。</p></div>
    <div style="display:flex;gap:12px"><span style="font-size:17px;color:#FF6A00;font-weight:600;letter-spacing:.1em;white-space:nowrap">勿断电</span><p style="font-size:18px;line-height:1.7;color:#5C636B">升级期间保持两台电脑供电与 USB 连接，不要拔线或强制重启。</p></div>
  </div>
</div>
<div class="pad rel" style="margin-top:22px">
  <p class="caption">设备不会自动联网检查更新；请从项目发布页下载 UF2，并在升级后确认两颗芯片的版本与校验值一致。</p>
</div>
'''))

# ------------------------------------------------------------------ 14 privacy
S.append(screen("14_隐私安全", 1100, f'''
{nav()}
{head("14", "安全", '只转发键鼠，<br>不搬运数据。',
      '它没有无线、没有网口、没有遥测，也不会因为某台电脑的请求而主动生成按键。')}
<div class="rel" style="margin:36px 56px 0;display:grid;grid-template-columns:1fr 1fr;gap:14px">
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">不传输数据</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">不支持复制粘贴、文件传输或剪贴板共享。</p></div>
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">不保留输入历史</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">不记录按键内容、鼠标轨迹或使用日志。</p></div>
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">只转发标准 HID</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">键鼠报告只发给当前活动输出。</p></div>
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">无无线通信</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">没有 Wi-Fi、蓝牙、以太网或互联网连接。</p></div>
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">配置全本地</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">网页不联网、不加载外部脚本、不上传数据。</p></div>
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">访问受控</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">配置需快捷键主动进入，WebHID 需明确授权。</p></div>
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">固定长度数据包</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">两颗芯片之间通信固定长度，配置项白名单。</p></div>
  <div style="background:#FFFFFF;border:1px solid #E9E1D5;border-radius:14px;padding:22px 24px"><div style="font-size:20px;font-weight:600;color:#15171C">不信任电脑</div><p style="font-size:16px;line-height:1.65;color:#6B7178;margin-top:6px">升级只能由用户在配置模式或物理 BOOTSEL 触发。</p></div>
</div>
<div class="pad rel" style="margin-top:24px">
  <p class="caption">Movio 是键鼠切换器，不能替代安全隔离设备。2kV 隔离用于信号侧电气隔离，不构成市电安全隔离等级。</p>
</div>
'''))

# ------------------------------------------------------------------ 15 limits
S.append(screen("15_使用边界", 1040, f'''
{nav()}
{head("15", "使用边界", '这些是设计边界，<br>不是故障。',
      '下单前，请先确认下面这些限制与你的使用场景一致。')}
<div class="pad rel" style="margin-top:34px">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px 26px">
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">只切键鼠</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">不切视频、音频、USB 存储或摄像头。</p></div>
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">两台都要供电</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">只接一台电脑时，另一路没有供电。</p></div>
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">仅左右并排</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">不支持上下堆叠的屏幕布局。</p></div>
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">不能跨机拖拽</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">无文件拖拽、复制粘贴、剪贴板共享。</p></div>
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">按住鼠标键不切换</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">避免拖窗口时误切到另一台。</p></div>
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">高级键鼠功能有限</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">旋钮、额外按键、厂商宏、RGB 可能无法转发。</p></div>
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">不支持蓝牙键鼠</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">需带 USB 接收器才能使用。</p></div>
    <div style="border-top:2px solid #E6DED2;padding-top:14px"><div style="font-size:20px;font-weight:600">快捷键不可网页修改</div><p style="font-size:17px;line-height:1.65;color:#6B7178;margin-top:5px">需改源码重新编译固件。</p></div>
  </div>
</div>
<div class="rel" style="margin:28px 56px 0;background:#fff;border:1px solid #E9E1D5;border-radius:16px;padding:24px 26px">
  <p style="font-size:19px;line-height:1.8;color:#5C636B">
    <b style="color:#15171C;font-weight:600">适合你，如果：</b>两台电脑并排摆放，需要共用一套键鼠，在意画面不被二次处理、电脑上不装任何软件。
  </p>
</div>
'''))

# ------------------------------------------------------------------ 16 specs + close
S.append(screen("16_参数", 1270, f'''
{nav()}
{head("16", "规格", '产品参数')}
<div class="pad rel" style="margin-top:26px">
  <div class="rows" style="border-top:none">
    {"".join(f'''<div class="row" style="padding:15px 0"><div style="width:190px;font-size:18px;color:#8A8F97;letter-spacing:.04em">{k}</div><div style="flex:1;font-size:19px;line-height:1.55;color:#22262C">{v}</div></div>''' for k, v in [
      ("产品名称", "Movio 双机键鼠切换器（开源硬件 KVM）"),
      ("产品型号", "Movio，基于 DeskHop 项目衍生"),
      ("硬件平台", "双 RP2040 主板，芯片角色硬件自动探测"),
      ("电气隔离", "信号侧 2kV 数字隔离"),
      ("键鼠接口", "USB-A ×2：键盘口 / 鼠标口"),
      ("电脑接口", "USB-C ×2：A 端 / B 端"),
      ("供电", "由两台电脑的 USB 口分别供电，无独立电源"),
      ("固件", "movio.uf2 · v0.80 · 写入后 CRC32 校验"),
      ("配置方式", "本地 WebHID 网页，Chrome / Chromium / Edge"),
      ("系统兼容", "Windows、macOS、Linux、Android；BIOS / UEFI / BitLocker 视主板"),
    ])}
  </div>
</div>
<div class="pad rel" style="margin-top:44px;border-top:1px solid #E6DED2;padding-top:36px">
  <div style="display:flex;align-items:flex-start;justify-content:space-between">
    <div>
      <div class="wordmark" style="font-size:34px;letter-spacing:.34em">MOVIO</div>
      <div style="font-size:22px;color:#4A5058;margin-top:16px;letter-spacing:.02em">鼠标穿屏，键盘跟随</div>
    </div>
    <div style="text-align:right;font-size:15px;line-height:1.9;color:#8A8F97;padding-top:4px">
      文档 V1.0<br>适用固件 v0.80
    </div>
  </div>
  <div style="font-size:16px;color:#8A8F97;margin-top:18px;letter-spacing:.05em">OPEN-SOURCE HARDWARE　·　GNU GPL v3　·　likeaturtle/Movio</div>
  <p style="font-size:15px;line-height:1.85;color:#8A8F97;margin-top:26px">
    本页文案整理自《Movio 产品说明书》V1.0 与《Movio 快速上手指南》V1.0。产品规格、固件行为与配置项可能随版本更新，请以项目最新代码与发布说明为准；外观与主板为示意图，实物以最终版本为准。
  </p>
</div>
'''))

SCREENS = S
