import os
import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class StudioCuteCatRenderer:
    def __init__(self, w=110, h=105, tcolor="#FF00FF"):
        self.w, self.h = w, h
        self.tcolor = tcolor
        self.direction = 1
        self.base_path = "assets/shadow_soldiers/cat_hq.png"
        self.raw_sprite = Image.open(self.base_path).convert("RGBA") if os.path.exists(self.base_path) else None

    def set_size(self, w, h):
        self.w, self.h = w, h

    def _composite(self, img_rgba):
        tc = self.tcolor.lstrip('#')
        rt, gt, bt = tuple(int(tc[i:i+2], 16) for i in (0, 2, 4))
        bg = Image.new("RGBA", (self.w, self.h), (rt, gt, bt, 255))
        alpha = img_rgba.split()[-1]
        clean_mask = alpha.point(lambda p: 255 if p >= 50 else 0)
        final = Image.composite(img_rgba.convert("RGB"), bg.convert("RGB"), clean_mask)
        return ImageTk.PhotoImage(final)

    def draw_sit(self, frame):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx, cy = self.w // 2, self.h // 2 + 6

        # Soft ground shadow
        d.ellipse([cx - 30, self.h - 14, cx + 30, self.h - 4], fill=(30, 20, 40, 60))

        if self.raw_sprite:
            breath = math.sin(frame * 0.22) * 1.8
            sw = int(self.w * 0.82)
            sh = int(self.h * 0.84)
            sprite = self.raw_sprite.resize((sw, sh), Image.LANCZOS)
            if self.direction == -1:
                sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            
            # Paste with breath offset
            px = cx - sw // 2
            py = cy - sh // 2 + int(breath)
            canvas.alpha_composite(sprite, (px, py))

        return self._composite(canvas)

    def draw_purr(self, frame):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx, cy = self.w // 2, self.h // 2 + 6

        # Soft ground shadow
        d.ellipse([cx - 30, self.h - 14, cx + 30, self.h - 4], fill=(30, 20, 40, 60))

        if self.raw_sprite:
            purr_rumble = math.sin(frame * 0.9) * 1.2
            sw = int(self.w * 0.82)
            sh = int(self.h * 0.84)
            sprite = self.raw_sprite.resize((sw, sh), Image.LANCZOS)
            if self.direction == -1:
                sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            
            px = cx - sw // 2
            py = cy - sh // 2 + int(purr_rumble)
            canvas.alpha_composite(sprite, (px, py))

        # Floating heart particles
        for i, off in enumerate([-18, 18]):
            hy = (frame * 3 + i * 14) % 36
            alpha = int(max(0, 255 - hy * 6.5))
            hx = cx + off + int(math.sin((frame + i * 5) * 0.3) * 6)
            d.text((hx - 4, cy - 26 - hy), "♡", fill=(255, 90, 150, alpha))

        return self._composite(canvas)

    def draw_walk(self, frame):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx, cy = self.w // 2, self.h // 2 + 6

        step_bob = abs(math.sin(frame * 0.55)) * 3.0
        tilt = math.sin(frame * 0.55) * 4.0

        # Walking shadow
        d.ellipse([cx - 28, self.h - 14, cx + 28, self.h - 5], fill=(30, 20, 40, 55))

        if self.raw_sprite:
            sw = int(self.w * 0.82)
            sh = int(self.h * 0.84)
            sprite = self.raw_sprite.resize((sw, sh), Image.LANCZOS)
            if self.direction == -1:
                sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            if abs(tilt) > 0.5:
                sprite = sprite.rotate(-tilt * self.direction, resample=Image.BICUBIC, expand=True)

            px = cx - sprite.width // 2
            py = cy - sprite.height // 2 - int(step_bob)
            canvas.alpha_composite(sprite, (px, py))

        return self._composite(canvas)

class StudioSpidermanRenderer:
    def __init__(self, w=110, h=105, tcolor="#FF00FF"):
        self.w, self.h = w, h
        self.tcolor = tcolor
        self.direction = 1
        self.idle_path = "assets/shadow_soldiers/spiderman_hq.png"
        self.action_path = "assets/shadow_soldiers/spiderman_action_hq.png"
        self.raw_idle = Image.open(self.idle_path).convert("RGBA") if os.path.exists(self.idle_path) else None
        self.raw_action = Image.open(self.action_path).convert("RGBA") if os.path.exists(self.action_path) else None

    def set_size(self, w, h):
        self.w, self.h = w, h

    def _composite(self, img_rgba):
        tc = self.tcolor.lstrip('#')
        rt, gt, bt = tuple(int(tc[i:i+2], 16) for i in (0, 2, 4))
        bg = Image.new("RGBA", (self.w, self.h), (rt, gt, bt, 255))
        alpha = img_rgba.split()[-1]
        clean_mask = alpha.point(lambda p: 255 if p >= 50 else 0)
        final = Image.composite(img_rgba.convert("RGB"), bg.convert("RGB"), clean_mask)
        return ImageTk.PhotoImage(final)

    def draw_idle(self, frame):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx, cy = self.w // 2, self.h // 2 + 4

        # Heroic ground shadow
        d.ellipse([cx - 26, self.h - 13, cx + 26, self.h - 4], fill=(20, 20, 35, 75))

        if self.raw_idle:
            breath = math.sin(frame * 0.25) * 1.6
            sw = int(self.w * 0.72)
            sh = int(self.h * 0.90)
            sprite = self.raw_idle.resize((sw, sh), Image.LANCZOS)
            if self.direction == -1:
                sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            
            px = cx - sw // 2
            py = cy - sh // 2 + int(breath)
            canvas.alpha_composite(sprite, (px, py))

        # Spider-Sense tingling aura
        if (frame % 30) < 14:
            arc_alpha = int(180 + math.sin(frame * 0.8) * 70)
            for side in (-1, 1):
                ax = cx + side * 24
                ay = cy - 30
                d.line([ax, ay - 6, ax + side * 6, ay - 14], fill=(255, 220, 30, arc_alpha), width=2)
                d.line([ax + side * 6, ay - 14, ax + side * 12, ay - 10], fill=(255, 60, 40, arc_alpha), width=2)

        return self._composite(canvas)

    def draw_web_swing(self, frame, flight_tilt=0.0):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx, cy = self.w // 2, self.h // 2 + 10

        # Pendulum swing angle
        swing_angle = math.sin(frame * 0.35) * 20.0 + flight_tilt * 0.8

        # Draw Dynamic Taut Web Line from top screen boundary (y=0) down to hand
        hand_x = cx + int(14 * self.direction)
        hand_y = cy - 14
        top_anchor_x = cx - int(swing_angle * 1.5)
        
        # Braided glowing web line
        d.line([top_anchor_x, 0, hand_x, hand_y], fill=(210, 240, 255, 140), width=3)
        d.line([top_anchor_x, 0, hand_x, hand_y], fill=(255, 255, 255, 240), width=1)

        # Web anchor spark at ceiling
        d.ellipse([top_anchor_x - 3, 0, top_anchor_x + 3, 5], fill=(255, 255, 255, 220))

        # Use action sprite rotated along swing arc
        sprite_base = self.raw_action or self.raw_idle
        if sprite_base:
            sw = int(self.w * 0.82)
            sh = int(self.h * 0.84)
            sprite = sprite_base.resize((sw, sh), Image.LANCZOS)
            if self.direction == -1:
                sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            if abs(swing_angle) > 0.5:
                sprite = sprite.rotate(-swing_angle, resample=Image.BICUBIC, expand=True)
            
            px = cx - sprite.width // 2
            py = cy - sprite.height // 2
            canvas.alpha_composite(sprite, (px, py))

        return self._composite(canvas)

    def draw_wall_crawl(self, frame):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx, cy = self.w // 2, self.h // 2

        # Vertical crawl step bob
        crawl_bob = math.sin(frame * 0.45) * 3.5

        # Wall crawl contact points at screen border
        wall_edge_x = 4 if self.direction == -1 else self.w - 4
        d.line([wall_edge_x, 10, wall_edge_x, self.h - 10], fill=(255, 255, 255, 160), width=2)
        # Suction web contact dots
        for wy in [cy - 24, cy - 8, cy + 12, cy + 28]:
            d.ellipse([wall_edge_x - 3, wy - 3, wall_edge_x + 3, wy + 3], fill=(255, 255, 255, 220))

        sprite_base = self.raw_action or self.raw_idle
        if sprite_base:
            sw = int(self.w * 0.82)
            sh = int(self.h * 0.84)
            sprite = sprite_base.resize((sw, sh), Image.LANCZOS)
            # Wall crawl orientation: rotated 75-90 degrees against the wall
            rot_angle = 75 if self.direction == 1 else -75
            sprite = sprite.rotate(rot_angle, resample=Image.BICUBIC, expand=True)

            px = cx - sprite.width // 2 + (8 if self.direction == 1 else -8)
            py = cy - sprite.height // 2 + int(crawl_bob)
            canvas.alpha_composite(sprite, (px, py))

        return self._composite(canvas)

    def draw_thwip(self, frame):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx, cy = self.w // 2, self.h // 2 + 4

        # Heroic pose
        sprite_base = self.raw_action or self.raw_idle
        if sprite_base:
            sw = int(self.w * 0.82)
            sh = int(self.h * 0.84)
            sprite = sprite_base.resize((sw, sh), Image.LANCZOS)
            if self.direction == -1:
                sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            px = cx - sw // 2
            py = cy - sh // 2
            canvas.alpha_composite(sprite, (px, py))

        # Thwip Web Blast expanding across the screen
        blast_dir = self.direction
        wrist_x = cx + int(24 * blast_dir)
        wrist_y = cy - 2
        tip_x = wrist_x + int(42 * blast_dir)
        tip_y = wrist_y - 8

        # Web projectile lines
        d.line([wrist_x, wrist_y, tip_x, tip_y], fill=(255, 255, 255, 250), width=2)
        d.line([wrist_x, wrist_y, tip_x, tip_y + 12], fill=(240, 250, 255, 220), width=1)
        d.line([wrist_x, wrist_y, tip_x - int(10 * blast_dir), tip_y - 12], fill=(240, 250, 255, 220), width=1)

        # Concentric web web-net arcs
        d.arc([tip_x - 14, tip_y - 14, tip_x + 14, tip_y + 14], 0, 360, fill=(255, 255, 255, 240), width=2)
        d.arc([tip_x - 22, tip_y - 22, tip_x + 22, tip_y + 22], 0, 360, fill=(230, 245, 255, 180), width=1)

        # Comic THWIP! label
        thwip_x = tip_x - (10 if blast_dir == 1 else 30)
        d.text((thwip_x, tip_y - 22), "THWIP!", fill=(255, 240, 60, 240))

        return self._composite(canvas)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    cat_rend = StudioCuteCatRenderer(110, 105)
    sit_img = cat_rend.draw_sit(0)
    purr_img = cat_rend.draw_purr(5)
    walk_img = cat_rend.draw_walk(3)
    print("Cat poses rendered:", sit_img.width(), "x", sit_img.height())

    spidey_rend = StudioSpidermanRenderer(110, 105)
    idle_img = spidey_rend.draw_idle(0)
    swing_img = spidey_rend.draw_web_swing(10, 5.0)
    crawl_img = spidey_rend.draw_wall_crawl(4)
    thwip_img = spidey_rend.draw_thwip(2)
    print("Spidey poses rendered:", idle_img.width(), "x", idle_img.height())

    root.destroy()
    print("ALL STUDIO RENDERERS PASSED WITH FLYING COLORS!")
