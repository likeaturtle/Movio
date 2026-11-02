from pathlib import Path
import cairosvg

OUT = Path('/home/fujd/Desktop/Movio/misc/manual_assets')
OUT.mkdir(parents=True, exist_ok=True)
FONT = "'Noto Sans CJK SC','Microsoft YaHei','Source Han Sans SC',sans-serif"
ORANGE = '#FF6600'
DARK = '#2B2B2B'
GRAY = '#7C7C7C'
SLATE = '#3D4B59'
LIGHT = '#FFF4EA'
BORDER = '#E6DED7'

def connection_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="760" viewBox="0 0 1600 760">
<defs>
  <marker id="ar" markerWidth="12" markerHeight="12" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="{ORANGE}"/></marker>
  <marker id="ar2" markerWidth="12" markerHeight="12" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="{SLATE}"/></marker>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.08"/></filter>
</defs>
<rect width="1600" height="760" fill="#ffffff"/>

<!-- input devices -->
<g font-family="{FONT}">
  <rect x="70" y="150" width="290" height="150" rx="18" fill="#FAFAFA" stroke="{BORDER}" stroke-width="3"/>
  <rect x="92" y="174" width="246" height="102" rx="9" fill="#ffffff" stroke="{DARK}" stroke-width="3"/>
  <g stroke="{GRAY}" stroke-width="3" opacity="0.8">
    <line x1="112" y1="198" x2="318" y2="198"/><line x1="112" y1="222" x2="318" y2="222"/>
    <line x1="112" y1="246" x2="318" y2="246"/>
  </g>
  <text x="215" y="345" text-anchor="middle" font-size="26" fill="{DARK}" font-weight="600">USB 键盘</text>

  <rect x="70" y="470" width="290" height="190" rx="18" fill="#FAFAFA" stroke="{BORDER}" stroke-width="3"/>
  <rect x="165" y="492" width="100" height="140" rx="48" fill="#ffffff" stroke="{DARK}" stroke-width="3"/>
  <line x1="215" y1="515" x2="215" y2="570" stroke="{DARK}" stroke-width="3"/>
  <ellipse cx="215" cy="648" rx="58" ry="12" fill="{LIGHT}" stroke="{ORANGE}" stroke-width="2.5"/>
  <text x="215" y="705" text-anchor="middle" font-size="26" fill="{DARK}" font-weight="600">USB 鼠标</text>
</g>

<!-- arrows to movio -->
<line x1="380" y1="235" x2="585" y2="300" stroke="{ORANGE}" stroke-width="5" marker-end="url(#ar)"/>
<line x1="380" y1="555" x2="585" y2="470" stroke="{ORANGE}" stroke-width="5" marker-end="url(#ar)"/>
<text x="443" y="245" font-family="{FONT}" font-size="20" fill="{GRAY}" transform="rotate(12 443 245)">USB-A</text>
<text x="437" y="552" font-family="{FONT}" font-size="20" fill="{GRAY}" transform="rotate(-14 437 552)">USB-A</text>

<!-- movio -->
<g filter="url(#sh)">
  <rect x="600" y="190" width="400" height="390" rx="28" fill="#ffffff" stroke="{BORDER}" stroke-width="3"/>
  <rect x="600" y="190" width="400" height="76" rx="28" fill="{ORANGE}"/>
  <rect x="600" y="238" width="400" height="28" fill="{ORANGE}"/>
</g>
<text x="800" y="241" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="700" fill="#ffffff">MOVIO</text>
<text x="800" y="315" text-anchor="middle" font-family="{FONT}" font-size="24" fill="{GRAY}">双机键鼠切换器</text>

<!-- ports on movio -->
<g font-family="{FONT}">
  <rect x="640" y="350" width="90" height="56" rx="8" fill="#F3F3F3" stroke="{GRAY}" stroke-width="2"/>
  <text x="685" y="386" text-anchor="middle" font-size="20" fill="{DARK}">输入</text>
  <rect x="870" y="350" width="90" height="56" rx="8" fill="#F3F3F3" stroke="{GRAY}" stroke-width="2"/>
  <text x="915" y="386" text-anchor="middle" font-size="20" fill="{DARK}">输入</text>
  <text x="800" y="458" text-anchor="middle" font-size="21" fill="{GRAY}">键盘 / 鼠标 USB 口</text>
  <line x1="670" y1="500" x2="930" y2="500" stroke="{BORDER}" stroke-width="2"/>
  <text x="800" y="528" text-anchor="middle" font-size="19" fill="{GRAY}">两颗 RP2040 之间</text>
  <text x="800" y="558" text-anchor="middle" font-size="19" fill="{GRAY}">UART + 2kV 隔离</text>
</g>

<!-- arrows to PCs -->
<line x1="1015" y1="300" x2="1205" y2="255" stroke="{ORANGE}" stroke-width="5" marker-end="url(#ar)"/>
<line x1="1015" y1="470" x2="1205" y2="515" stroke="{SLATE}" stroke-width="5" marker-end="url(#ar2)"/>
<text x="1050" y="258" font-family="{FONT}" font-size="20" fill="{GRAY}" transform="rotate(-13 1050 258)">A 端</text>
<text x="1050" y="520" font-family="{FONT}" font-size="20" fill="{GRAY}" transform="rotate(13 1050 520)">B 端</text>

<!-- computers -->
<g font-family="{FONT}">
  <rect x="1220" y="155" width="300" height="190" rx="14" fill="#FAFAFA" stroke="{ORANGE}" stroke-width="4"/>
  <rect x="1244" y="179" width="252" height="118" rx="6" fill="#ffffff" stroke="{BORDER}" stroke-width="2"/>
  <rect x="1330" y="345" width="80" height="12" rx="4" fill="{ORANGE}"/>
  <rect x="1280" y="357" width="180" height="14" rx="7" fill="{ORANGE}"/>
  <circle cx="1370" cy="240" r="26" fill="{LIGHT}"/>
  <text x="1370" y="249" text-anchor="middle" font-size="28" font-weight="700" fill="{ORANGE}">A</text>
  <text x="1370" y="418" text-anchor="middle" font-size="27" font-weight="600" fill="{DARK}">电脑 A</text>

  <rect x="1220" y="455" width="300" height="190" rx="14" fill="#FAFAFA" stroke="{SLATE}" stroke-width="4"/>
  <rect x="1244" y="479" width="252" height="118" rx="6" fill="#ffffff" stroke="{BORDER}" stroke-width="2"/>
  <rect x="1330" y="645" width="80" height="12" rx="4" fill="{SLATE}"/>
  <rect x="1280" y="657" width="180" height="14" rx="7" fill="{SLATE}"/>
  <circle cx="1370" cy="540" r="26" fill="#EEF1F4"/>
  <text x="1370" y="549" text-anchor="middle" font-size="28" font-weight="700" fill="{SLATE}">B</text>
  <text x="1370" y="718" text-anchor="middle" font-size="27" font-weight="600" fill="{DARK}">电脑 B</text>
</g>

<text x="800" y="730" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{GRAY}">两台电脑均需通过 USB 为 Movio 供电，并保持数据线连接</text>
</svg>'''

def mouse_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="620" viewBox="0 0 1600 620">
<defs>
  <marker id="ar" markerWidth="14" markerHeight="14" refX="10" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ORANGE}"/></marker>
</defs>
<rect width="1600" height="620" fill="#ffffff"/>
<g font-family="{FONT}">
  <!-- screens -->
  <rect x="90" y="120" width="650" height="380" rx="16" fill="#FAFAFA" stroke="{SLATE}" stroke-width="5"/>
  <rect x="114" y="144" width="602" height="332" rx="6" fill="#F3F5F7"/>
  <text x="415" y="73" text-anchor="middle" font-size="28" font-weight="600" fill="{DARK}">电脑 B（左侧）</text>
  <text x="415" y="430" text-anchor="middle" font-size="24" fill="{GRAY}">B 主屏</text>

  <rect x="860" y="120" width="650" height="380" rx="16" fill="#FFF9F4" stroke="{ORANGE}" stroke-width="5"/>
  <rect x="884" y="144" width="602" height="332" rx="6" fill="{LIGHT}"/>
  <text x="1185" y="73" text-anchor="middle" font-size="28" font-weight="600" fill="{DARK}">电脑 A（右侧）</text>
  <text x="1185" y="430" text-anchor="middle" font-size="24" fill="{GRAY}">A 主屏</text>

  <!-- shared edge -->
  <line x1="800" y1="95" x2="800" y2="535" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="12 10"/>
  <text x="800" y="580" text-anchor="middle" font-size="22" font-weight="600" fill="{ORANGE}">共享边缘（切换发生在这里）</text>

  <!-- path -->
  <path d="M 1200 300 L 815 300" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-dasharray="16 12" marker-end="url(#ar)"/>
  <path d="M 785 300 L 420 300" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-dasharray="16 12" marker-end="url(#ar)" opacity="0.55"/>

  <!-- cursor -->
  <g transform="translate(1060,265) rotate(-12)">
    <path d="M0,0 L0,38 L11,29 L18,47 L28,43 L21,25 L35,24 Z" fill="#ffffff" stroke="{DARK}" stroke-width="2.5"/>
  </g>

  <!-- y preserved -->
  <line x1="760" y1="300" x2="840" y2="300" stroke="{DARK}" stroke-width="2"/>
  <circle cx="800" cy="300" r="7" fill="{ORANGE}" stroke="#fff" stroke-width="3"/>
  <rect x="680" y="338" width="240" height="38" rx="8" fill="#ffffff"/><text x="800" y="365" text-anchor="middle" font-size="20" fill="{GRAY}">Y 坐标保持不变</text>

  <!-- labels -->
  <rect x="1040" y="180" width="266" height="58" rx="29" fill="#ffffff" stroke="{ORANGE}" stroke-width="2"/>
  <text x="1173" y="217" text-anchor="middle" font-size="21" font-weight="600" fill="{ORANGE}">继续向左移动</text>

  <text x="800" y="28" text-anchor="middle" font-size="24" font-weight="600" fill="{DARK}">默认布局：A 在右、B 在左</text>
</g>
</svg>'''

def upgrade_svg():
    steps = [
        ("1", "下载固件", "获取 movio.uf2\n并核对版本"),
        ("2", "进入配置模式", "左 Ctrl + 右 Shift\n+ C + O"),
        ("3", "复制到 MOVIO 盘", "把 UF2 文件拖入\n虚拟盘根目录"),
        ("4", "自动升级双 RP2040", "两颗芯片依次写入\n完成后自动重启"),
    ]
    blocks = []
    for i, (num, title, desc) in enumerate(steps):
        x = 55 + i * 390
        color = ORANGE if i < 3 else SLATE
        blocks.append(f'''
        <g>
          <rect x="{x}" y="105" width="320" height="285" rx="20" fill="#ffffff" stroke="{BORDER}" stroke-width="3"/>
          <circle cx="{x+160}" cy="105" r="34" fill="{color}"/>
          <text x="{x+160}" y="117" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="#ffffff">{num}</text>
          <text x="{x+160}" y="205" text-anchor="middle" font-family="{FONT}" font-size="27" font-weight="600" fill="{DARK}">{title}</text>
          <text x="{x+160}" y="260" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{GRAY}">{desc.split(chr(10))[0]}</text>
          <text x="{x+160}" y="293" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{GRAY}">{desc.split(chr(10))[1]}</text>
        </g>''')
        if i < 3:
            blocks.append(f'<line x1="{x+325}" y1="247" x2="{x+380}" y2="247" stroke="{ORANGE}" stroke-width="5" marker-end="url(#ar)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="500" viewBox="0 0 1600 500">
<defs><marker id="ar" markerWidth="12" markerHeight="12" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="{ORANGE}"/></marker></defs>
<rect width="1600" height="500" fill="#ffffff"/>
<text x="800" y="50" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="600" fill="{DARK}">通过 MOVIO 配置盘升级的标准流程</text>
{''.join(blocks)}
<text x="800" y="455" text-anchor="middle" font-family="{FONT}" font-size="21" fill="{GRAY}">升级期间请保持两台电脑供电和 USB 连接，不要拔出线缆或断电</text>
</svg>'''


def _chip(cx, cy, badge, color):
    """Draw a stylised RP2040 QFN package with pins."""
    pins = []
    for i in range(7):
        off = -78 + i * 26
        pins.append(f'<rect x="{cx-118}" y="{cy+off-5}" width="18" height="10" rx="2" fill="#C9CDD2"/>')
        pins.append(f'<rect x="{cx+100}" y="{cy+off-5}" width="18" height="10" rx="2" fill="#C9CDD2"/>')
        pins.append(f'<rect x="{cx+off-5}" y="{cy-118}" width="10" height="18" rx="2" fill="#C9CDD2"/>')
        pins.append(f'<rect x="{cx+off-5}" y="{cy+100}" width="10" height="18" rx="2" fill="#C9CDD2"/>')
    return f"""
    <g>
      {''.join(pins)}
      <rect x="{cx-102}" y="{cy-102}" width="204" height="204" rx="12" fill="#171717" stroke="#3A3A3A" stroke-width="3"/>
      <circle cx="{cx-78}" cy="{cy-78}" r="7" fill="#5A5A5A"/>
      <text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="{FONT}" font-size="37" font-weight="700" fill="#FFFFFF">RP2040</text>
      <text x="{cx}" y="{cy+44}" text-anchor="middle" font-family="{FONT}" font-size="21" fill="#A9A9A9">双核 · 133 MHz</text>
      <circle cx="{cx+92}" cy="{cy-92}" r="27" fill="{color}"/>
      <text x="{cx+92}" y="{cy-82}" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="#FFFFFF">{badge}</text>
    </g>"""


def board_svg():
    a = _chip(470, 470, "A", ORANGE)
    b = _chip(1210, 470, "B", SLATE)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1100" viewBox="0 0 2000 1100">
<defs>
  <linearGradient id="pcb" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#237A4B"/><stop offset="1" stop-color="#145735"/>
  </linearGradient>
  <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#E7EAED"/><stop offset="1" stop-color="#B8BEC4"/>
  </linearGradient>
</defs>
<rect width="2000" height="1100" fill="#FFFFFF"/>
<rect x="112" y="152" width="1696" height="800" rx="34" fill="#000000" opacity="0.07"/>
<rect x="100" y="140" width="1700" height="800" rx="34" fill="url(#pcb)" stroke="#0E3F28" stroke-width="8"/>
<rect x="122" y="162" width="1656" height="756" rx="24" fill="none" stroke="#3E9B6B" stroke-width="2" opacity="0.65"/>

<g fill="#E9E2D8" stroke="#0E3F28" stroke-width="3">
  <circle cx="152" cy="192" r="20"/><circle cx="1748" cy="192" r="20"/>
  <circle cx="152" cy="888" r="20"/><circle cx="1748" cy="888" r="20"/>
</g>
<g fill="#1A1A1A">
  <circle cx="152" cy="192" r="10"/><circle cx="1748" cy="192" r="10"/>
  <circle cx="152" cy="888" r="10"/><circle cx="1748" cy="888" r="10"/>
</g>

<g fill="none" stroke="#D9A441" stroke-width="4" opacity="0.6" stroke-linejoin="round" stroke-linecap="round">
  <path d="M 285 355 H 330 V 410 H 360"/>
  <path d="M 285 625 H 330 V 780 H 1100 V 625 H 1100"/>
  <path d="M 580 420 H 760 V 470 H 900"/>
  <path d="M 1060 470 H 1100"/>
  <path d="M 580 520 V 270 H 1530 V 372 H 1600"/>
  <path d="M 1320 520 V 760 H 1530 V 642 H 1600"/>
</g>

<g>
  <rect x="135" y="310" width="150" height="92" rx="10" fill="url(#metal)" stroke="#7C858D" stroke-width="3"/>
  <rect x="150" y="334" width="120" height="44" rx="4" fill="#1B1B1B"/>
  <rect x="158" y="344" width="104" height="8" rx="2" fill="#4A4A4A"/>
  <text x="210" y="448" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="600" fill="#FFFFFF">键盘</text>
  <rect x="135" y="580" width="150" height="92" rx="10" fill="url(#metal)" stroke="#7C858D" stroke-width="3"/>
  <rect x="150" y="604" width="120" height="44" rx="4" fill="#1B1B1B"/>
  <rect x="158" y="614" width="104" height="8" rx="2" fill="#4A4A4A"/>
  <text x="210" y="718" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="600" fill="#FFFFFF">鼠标</text>
</g>

{a}
{b}

<g>
  <rect x="900" y="420" width="160" height="100" rx="7" fill="#171717" stroke="#3A3A3A" stroke-width="3"/>
  <g fill="#C9CDD2">
    <rect x="912" y="530" width="10" height="18" rx="2"/><rect x="936" y="530" width="10" height="18" rx="2"/>
    <rect x="960" y="530" width="10" height="18" rx="2"/><rect x="984" y="530" width="10" height="18" rx="2"/>
    <rect x="1008" y="530" width="10" height="18" rx="2"/><rect x="1032" y="530" width="10" height="18" rx="2"/>
    <rect x="912" y="392" width="10" height="18" rx="2"/><rect x="936" y="392" width="10" height="18" rx="2"/>
    <rect x="960" y="392" width="10" height="18" rx="2"/><rect x="984" y="392" width="10" height="18" rx="2"/>
    <rect x="1008" y="392" width="10" height="18" rx="2"/><rect x="1032" y="392" width="10" height="18" rx="2"/>
  </g>
  <text x="980" y="478" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="600" fill="#FFFFFF">ISO7721</text>
  <text x="980" y="612" text-anchor="middle" font-family="{FONT}" font-size="24" fill="#D8F3E3">数字隔离器</text>
</g>

<line x1="980" y1="220" x2="980" y2="390" stroke="#FFB27A" stroke-width="3" stroke-dasharray="14 12"/>
<line x1="980" y1="545" x2="980" y2="590" stroke="#FFB27A" stroke-width="3" stroke-dasharray="14 12"/>
<rect x="890" y="250" width="180" height="42" rx="21" fill="#145735"/>
<text x="980" y="279" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="600" fill="#FFD8BC">2kV 隔离</text>

<g>
  <rect x="1590" y="348" width="152" height="52" rx="22" fill="url(#metal)" stroke="#7C858D" stroke-width="3"/>
  <rect x="1610" y="364" width="112" height="20" rx="9" fill="#1B1B1B"/>
  <text x="1666" y="330" text-anchor="middle" font-family="{FONT}" font-size="25" font-weight="600" fill="#FFFFFF">A 端</text>
  <rect x="1590" y="618" width="152" height="52" rx="22" fill="url(#metal)" stroke="#7C858D" stroke-width="3"/>
  <rect x="1610" y="634" width="112" height="20" rx="9" fill="#1B1B1B"/>
  <text x="1666" y="600" text-anchor="middle" font-family="{FONT}" font-size="25" font-weight="600" fill="#FFFFFF">B 端</text>
</g>

<text x="470" y="655" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="600" fill="#FFFFFF">控制器 A</text>
<text x="1210" y="655" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="600" fill="#FFFFFF">控制器 B</text>
<circle cx="710" cy="330" r="9" fill="#FF6600" stroke="#FFD8BC" stroke-width="3"/>
<text x="730" y="338" font-family="{FONT}" font-size="21" fill="#FFD8BC">LED A</text>
<circle cx="1450" cy="330" r="9" fill="#3D4B59" stroke="#C9D5DF" stroke-width="3"/>
<text x="1470" y="338" font-family="{FONT}" font-size="21" fill="#D7E1E8">LED B</text>

<text x="950" y="820" text-anchor="middle" font-family="{FONT}" font-size="40" font-weight="700" fill="#FFFFFF" letter-spacing="8">MOVIO</text>
<text x="950" y="860" text-anchor="middle" font-family="{FONT}" font-size="24" fill="#A9D9BE">双 RP2040 主板</text>

<text x="1790" y="382" font-family="{FONT}" font-size="24" fill="#4A4A4A">→ 电脑 A</text>
<text x="1790" y="652" font-family="{FONT}" font-size="24" fill="#4A4A4A">→ 电脑 B</text>
</svg>"""


def cover_svg():
    a = _chip(760, 570, "A", "#FF6600")
    b = _chip(1240, 570, "B", "#3D4B59")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="900" viewBox="0 0 2000 900">
<defs>
  <linearGradient id="red" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F05A44"/><stop offset="1" stop-color="#D93622"/>
  </linearGradient>
  <linearGradient id="pcb2" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#237A4B"/><stop offset="1" stop-color="#145735"/>
  </linearGradient>
  <linearGradient id="metal2" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#E7EAED"/><stop offset="1" stop-color="#B8BEC4"/>
  </linearGradient>
</defs>


<rect x="320" y="86" width="1360" height="252" rx="34" fill="#B92A19" opacity="0.18"/>
<rect x="300" y="70" width="1400" height="250" rx="34" fill="url(#red)" stroke="#B92A19" stroke-width="4"/>
<rect x="326" y="96" width="1348" height="198" rx="24" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.35"/>
<g stroke="#FFFFFF" stroke-width="6" fill="none" opacity="0.95">
  <rect x="470" y="145" width="210" height="100" rx="12"/>
  <line x1="500" y1="175" x2="650" y2="175"/><line x1="500" y1="200" x2="650" y2="200"/>
  <line x1="500" y1="225" x2="650" y2="225"/>
</g>
<g stroke="#FFFFFF" stroke-width="6" fill="none" opacity="0.95">
  <rect x="790" y="132" width="82" height="126" rx="40"/>
  <line x1="831" y1="150" x2="831" y2="192"/>
</g>
<text x="1120" y="220" text-anchor="middle" font-family="{FONT}" font-size="66" font-weight="700" fill="#FFFFFF" letter-spacing="10">MOVIO</text>
<text x="1580" y="180" text-anchor="middle" font-family="{FONT}" font-size="60" font-weight="700" fill="#FFFFFF">A</text>
<text x="1450" y="145" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="700" fill="#FFFFFF">B</text>

<g stroke="#C9B8AA" stroke-width="4" stroke-dasharray="10 8" opacity="0.9">
  <line x1="400" y1="320" x2="400" y2="400"/>
  <line x1="1600" y1="320" x2="1600" y2="400"/>
</g>

<ellipse cx="1000" cy="820" rx="620" ry="34" fill="#000000" opacity="0.10"/>
<rect x="360" y="400" width="1280" height="380" rx="28" fill="url(#pcb2)" stroke="#0E3F28" stroke-width="6"/>
<rect x="382" y="422" width="1236" height="336" rx="18" fill="none" stroke="#3E9B6B" stroke-width="2" opacity="0.6"/>

<g>
  <rect x="392" y="458" width="112" height="70" rx="9" fill="url(#metal2)" stroke="#7C858D" stroke-width="2"/>
  <rect x="404" y="476" width="88" height="34" rx="4" fill="#1B1B1B"/>
  <rect x="392" y="600" width="112" height="70" rx="9" fill="url(#metal2)" stroke="#7C858D" stroke-width="2"/>
  <rect x="404" y="618" width="88" height="34" rx="4" fill="#1B1B1B"/>
  <rect x="1496" y="470" width="112" height="40" rx="18" fill="url(#metal2)" stroke="#7C858D" stroke-width="2"/>
  <rect x="1512" y="482" width="80" height="16" rx="8" fill="#1B1B1B"/>
  <rect x="1496" y="642" width="112" height="40" rx="18" fill="url(#metal2)" stroke="#7C858D" stroke-width="2"/>
  <rect x="1512" y="654" width="80" height="16" rx="8" fill="#1B1B1B"/>
</g>

{a}
{b}

<g>
  <rect x="950" y="540" width="100" height="62" rx="5" fill="#171717" stroke="#3A3A3A" stroke-width="2"/>
  <text x="1000" y="578" text-anchor="middle" font-family="{FONT}" font-size="15" fill="#FFFFFF">ISO</text>
</g>


<text x="1000" y="745" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="#FFFFFF" letter-spacing="6">MOVIO</text>
</svg>"""


def main():
    specs = [
        ("fig_connection", connection_svg(), 1600, 760),
        ("fig_mouse", mouse_svg(), 1600, 620),
        ("fig_upgrade", upgrade_svg(), 1600, 500),
        ("fig_board", board_svg(), 2000, 1100),
        ("fig_cover", cover_svg(), 2000, 900),
    ]
    for name, svg, w, h in specs:
        path = OUT / f"{name}.png"
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(path), output_width=w * 2, output_height=h * 2)
        if name == "fig_cover":
            from PIL import Image
            im = Image.open(path).convert("RGBA")
            bbox = im.getbbox()
            pad = 18
            box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                   min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))
            im.crop(box).save(path)
        print("saved", path)


main()

