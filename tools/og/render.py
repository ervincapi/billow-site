"""Renders img/og-<lang>.png (1200x630) share cards with headless Chrome. Run from the repo root:
    python3 tools/og/render.py
"""
import pathlib, subprocess, sys, html, json
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
src = (ROOT / "tools" / "build_site.py").read_text()
ns = {"__file__": str(ROOT / "tools" / "build_site.py")}
exec(src.split("\nfor lang in LANGS:")[0].replace('SITE = pathlib.Path(sys.argv[1])', 'SITE = pathlib.Path(%r)' % str(ROOT)).replace('STYLE = theme_aware(pathlib.Path(sys.argv[2]).read_text())', 'STYLE = ""'), ns)
T, LANGS = ns["T"], ns["LANGS"]
TEMPLATE = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{font:400 16px -apple-system,BlinkMacSystemFont,"SF Pro Display","Inter","Segoe UI",Roboto,sans-serif;color:#EAF6F9;background:linear-gradient(135deg,#06202A 0%,#0B3C4A 55%,#0E7490 130%);position:relative;-webkit-font-smoothing:antialiased}
.glow{position:absolute;inset:-30%;background:radial-gradient(40% 50% at 20% 30%,rgba(125,211,230,.45),transparent 62%),radial-gradient(36% 46% at 82% 22%,rgba(34,184,209,.5),transparent 60%),radial-gradient(28% 36% at 68% 95%,rgba(251,191,36,.22),transparent 62%);filter:blur(60px)}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.5px,transparent 1.6px);background-size:28px 28px;-webkit-mask-image:linear-gradient(180deg,rgba(0,0,0,.7),transparent 85%)}
.wrap{position:absolute;inset:0;display:grid;grid-template-columns:1.1fr .9fr;align-items:center;padding:0 72px;gap:40px}
.brand{display:flex;align-items:center;gap:14px;font-weight:700;font-size:28px;letter-spacing:-.02em;margin-bottom:28px}
.brand img{width:48px;height:48px;border-radius:12px;box-shadow:0 8px 20px rgba(0,0,0,.35)}
h1{font-size:64px;line-height:1.02;letter-spacing:-.035em;font-weight:800;margin:0 0 22px;color:#fff;text-wrap:balance}
h1 span{background:linear-gradient(92deg,#7DD3E6,#A7F3D0);-webkit-background-clip:text;background-clip:text;color:transparent}
p{font-size:24px;line-height:1.4;color:#B9D7DF;margin:0;max-width:30ch}
.url{position:absolute;left:72px;bottom:44px;font-size:20px;font-weight:600;color:#9ED9E6;letter-spacing:.01em}
.phone{justify-self:center;width:290px;border-radius:46px;padding:10px;background:#0B1117;box-shadow:0 50px 100px -30px rgba(0,0,0,.7),0 0 0 2px #1B2630;position:relative;transform:rotate(-4deg) translateY(40px)}
.phone::before{content:"";position:absolute;top:20px;left:50%;transform:translateX(-50%);width:28%;height:23px;border-radius:999px;background:#0B1117;z-index:1}
.phone img{display:block;width:100%;border-radius:36px}
</style></head><body><div class="glow"></div><div class="dots"></div>
<div class="wrap"><div><div class="brand"><img src="{icon}" alt="">Billow</div><h1>{h1a} <span>{h1b}</span></h1><p>{lead}</p></div>
<div class="phone"><img src="{home}" alt=""></div></div>
<div class="url">billow-app.org</div></body></html>"""
out_dir = ROOT / "img"; tmp = ROOT / "tools" / "og" / "tmp"; tmp.mkdir(exist_ok=True)
for lang in LANGS:
    t = T[lang]
    page = TEMPLATE.replace("{lang}", lang).replace("{icon}", (ROOT / "img" / "icon.png").as_uri()).replace("{home}", (ROOT / "img" / "home.jpg").as_uri()) \
        .replace("{h1a}", html.escape(t["h1a"])).replace("{h1b}", html.escape(t["h1b"])).replace("{lead}", html.escape(t["lead"]))
    f = tmp / f"og-{lang}.html"; f.write_text(page)
    out = out_dir / f"og-{lang}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1200,630",
                    f"--screenshot={out}", f.as_uri()], check=True, capture_output=True, timeout=60)
    print(out.name, out.stat().st_size, "bytes")
