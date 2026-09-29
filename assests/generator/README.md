# Banner generator

Scripts that build `../dark.svg` and `../light.svg` (the animated profile hero).

Requirements: Python 3 and Pillow (`pip3 install Pillow`). The screenshot helper also needs Google Chrome on macOS.

```bash
# 1. (only when the photo changes) photo -> character grid; the photo itself is not committed
python3 portrait.py /path/to/headshot.png

# 2. regenerate both banners from portrait.json + the DATA block in gen.py
python3 gen.py

# 3. optional: preview a frame of the animation (seconds), e.g. 6 s
python3 render.py ../dark.svg preview.png 6
```

Everything the banner says (name, headline, roles, info rows, stack pills, projects, links) lives in the `DATA` block at the top of `gen.py`. Running `gen.py` overwrites the two SVGs, so hand edits to the SVGs are lost.
