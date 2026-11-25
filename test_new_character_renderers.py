import os
import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def test_sprites():
    root = tk.Tk()
    root.withdraw()

    cat_path = "assets/shadow_soldiers/cat_hq.png"
    spidey_path = "assets/shadow_soldiers/spiderman_hq.png"
    spidey_action_path = "assets/shadow_soldiers/spiderman_action_hq.png"

    assert os.path.exists(cat_path), "cat_hq.png missing"
    assert os.path.exists(spidey_path), "spiderman_hq.png missing"
    assert os.path.exists(spidey_action_path), "spiderman_action_hq.png missing"

    cat_img = Image.open(cat_path).convert("RGBA")
    spidey_img = Image.open(spidey_path).convert("RGBA")
    spidey_action_img = Image.open(spidey_action_path).convert("RGBA")

    print(f"Cat sprite: {cat_img.size}")
    print(f"Spiderman sprite: {spidey_img.size}")
    print(f"Spiderman Action sprite: {spidey_action_img.size}")

    root.destroy()
    print("ALL SPRITE ASSETS LOADED SUCCESSFULLY!")

if __name__ == "__main__":
    test_sprites()
