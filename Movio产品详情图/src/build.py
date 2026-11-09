#!/usr/bin/env python3
"""Render the Movio Taobao detail-page screens from HTML to PNG/JPG."""
import os, subprocess, sys, shutil, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
WORK = ROOT / "_work"
OUT = ROOT / "out"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = WORK / "chrome-profile"

sys.path.insert(0, str(SRC))
from screens import SCREENS  # noqa: E402

THEME = (SRC / "theme.css").read_text(encoding="utf-8")

def build_html(name, css, body):
    return (
        "<!doctype html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">\n"
        f"<title>{name}</title>\n<style>{THEME}</style>\n<style>{css}</style>\n"
        f"</head><body>{body}</body></html>"
    )

def render(screen, keep_png=False):
    slug, height, body, css = screen["slug"], screen["height"], screen["body"], screen.get("css", "")
    html_path = WORK / f"{slug}.html"
    html_path.write_text(build_html(slug, css, body), encoding="utf-8")
    png = WORK / f"{slug}.png"
    cmd = [
        CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-breakpad",
        "--disable-crash-reporter", "--no-first-run", "--disable-dev-shm-usage",
        "--hide-scrollbars", f"--user-data-dir={PROFILE}",
        "--force-device-scale-factor=2", f"--window-size=750,{height}",
        f"--screenshot={png}", f"file://{html_path}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not png.exists():
        print(r.stderr[-2000:])
        raise SystemExit(f"render failed: {slug}")
    from PIL import Image
    im = Image.open(png).convert("RGB")
    out = OUT / f"{slug}.jpg"
    im.save(out, quality=93, subsampling=1, optimize=True)
    print(f"  {slug}.jpg  {im.width}x{im.height}  {out.stat().st_size/1024:.0f} KB")
    return im

def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    OUT.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    for s in SCREENS:
        if only and not any(o in s["slug"] for o in only):
            continue
        print(f"render {s['slug']}")
        render(s)
    if not only:
        build_overview()
        package()

def build_overview():
    from PIL import Image
    files = sorted(OUT.glob("*.jpg"))
    width = 1500
    scaled = []
    for f in files:
        im = Image.open(f)
        h = int(im.height * width / im.width)
        scaled.append(im if im.width == width else im.resize((width, h), Image.LANCZOS))
    total = sum(i.height for i in scaled) + 16 * (len(scaled) - 1)
    canvas = Image.new("RGB", (width, total), (255, 255, 255))
    y = 0
    for im in scaled:
        canvas.paste(im, (0, y)); y += im.height + 16
    prev = OUT / "预览"; prev.mkdir(exist_ok=True)
    canvas.save(prev / "全页长图.jpg", quality=86, optimize=True)
    print(f"  overview {canvas.width}x{canvas.height}")

def package():
    import glob, zipfile, html, shutil
    files = [f for f in sorted(glob.glob(str(OUT / "*.jpg")))]
    names = [os.path.basename(f) for f in files]
    updir = OUT / "upload_1500"; updir.mkdir(exist_ok=True)
    for n in names:
        shutil.copy2(OUT / n, updir / n)
    prev = OUT / "预览"; prev.mkdir(exist_ok=True)
    items = "\n".join(
        f'<figure><img src="../upload_1500/{html.escape(n)}" alt="{html.escape(n)}" loading="lazy"><figcaption>{html.escape(n)}</figcaption></figure>'
        for n in names)
    (prev / "index.html").write_text(f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Movio 淘宝详情页 · 预览</title>
<style>
  body{{margin:0;background:#e9e5df;font-family:"PingFang SC",sans-serif;color:#15171C}}
  header{{padding:40px 24px 24px;max-width:750px;margin:0 auto}}
  h1{{font-size:24px;margin:0 0 8px}}
  p{{font-size:14px;color:#5c636b;margin:0}}
  main{{max-width:750px;margin:0 auto 80px;display:flex;flex-direction:column;gap:12px;padding:0 24px}}
  figure{{margin:0;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.08)}}
  img{{width:100%;display:block}}
  figcaption{{font-size:12px;color:#8a8f97;padding:8px 12px}}
</style></head>
<body>
<header>
  <h1>Movio · 淘宝店铺产品详情图</h1>
  <p>共 {len(names)} 屏 · 1500px 宽 · 单屏高度 ≤ 2980px</p>
</header>
<main>
{items}
</main>
</body></html>""", encoding="utf-8")
    zp = ROOT / "Movio_详情图_1500px.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.write(updir / n, f"upload_1500/{n}")
        z.write(prev / "index.html", "预览/index.html")
        z.write(ROOT / "README.md", "说明.md")
    print(f"  package: {len(names)} images, zip {zp.stat().st_size//1024} KB")

if __name__ == "__main__":
    main()
