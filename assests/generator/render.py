"""Render an SVG at a given animation time: wraps it inline in HTML, pauses SMIL, seeks, screenshots."""
import sys, os, subprocess
svg, out, t = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0
body = open(svg, encoding="utf-8").read().split("?>", 1)[-1]
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#888}}</style></head>
<body>{body}<script>
const s=document.querySelector('svg'); s.pauseAnimations(); s.setCurrentTime({t});
</script></body></html>"""
wrapper = out + ".html"; open(wrapper, "w", encoding="utf-8").write(html)
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1180,610",
                "--screenshot=" + out, "file://" + os.path.abspath(wrapper)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
os.remove(wrapper); print(out, os.path.getsize(out))
