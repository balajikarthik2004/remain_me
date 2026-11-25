import os
from PIL import Image, ImageTk

assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites_aligned")
if not os.path.exists(assets_dir):
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "sprites_aligned")

print("Checking assets_dir:", assets_dir)
files = ['idle.png', 'walking.png', 'happy.png', 'sleeping.png', 'dancing.png', 'thinking.png', 'stretch.png']
for f in files:
    p = os.path.join(assets_dir, f)
    if os.path.exists(p):
        im = Image.open(p).convert("RGBA")
        print(f"Loaded {f}: size={im.size}, mode={im.mode}")
    else:
        print(f"Missing {f}")
