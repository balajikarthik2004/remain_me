import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math

class TestSpidermanRenderer:
    """
    Spider-Man Renderer:
    - Red & Blue suit with black web pattern
    - Iconic expressive white angular eyes with black rims
    - Black chest spider insignia
    - Poses:
      - stand / idle (classic heroic pose)
      - web_swing (holding web line above, legs tucked, swinging)
      - wall_crawl (hands & feet splayed, crawling along the side of the monitor)
      - upside_down (hanging upside-down on a web strand)
      - thwip (web shooting pose with web lines extending outward)
    """
    AA = 4
    RED = (220, 20, 45, 255)
    RED_DARK = (165, 12, 32, 255)
    BLUE = (20, 65, 185, 255)
    BLUE_DARK = (12, 40, 120, 255)
    EYE_WHITE = (255, 255, 255, 255)
    EYE_BLACK = (10, 10, 15, 255)
    WEB_BLACK = (25, 15, 20, 230)
    WEB_WHITE = (245, 250, 255, 255)

    def __init__(self, w=96, h=96, tcolor="#FF00FF"):
        self.w, self.h = w, h
        self.tcolor = tcolor
        self.aw, self.ah = w * self.AA, h * self.AA
        self.direction = 1
        self.sx = self.w / 160.0
        self.sy = self.h / 160.0

    def _s(self, v): return int(v * self.AA)
    def _mx(self, x):
        m = x * self.sx
        if self.direction == -1: m = self.w - m
        return self._s(m)
    def _my(self, y): return self._s(y * self.sy)

    def _ell(self, d, cx, cy, rx, ry, fill, outline=None, width=1):
        mcx, mcy = self._mx(cx), self._my(cy)
        mrx, mry = self._s(rx * self.sx), self._s(ry * self.sy)
        d.ellipse([mcx - mrx, mcy - mry, mcx + mrx, mcy + mry], fill=fill, outline=outline, width=max(1, self._s(width)))

    def _pol(self, d, pts, fill, outline=None, width=1):
        mapped = [(self._mx(x), self._my(y)) for x, y in pts]
        d.polygon(mapped, fill=fill)
        if outline:
            mapped_c = mapped + [mapped[0]]
            d.line(mapped_c, fill=outline, width=max(1, self._s(width)))

    def _draw_spidey_mask(self, d, cx, cy, rx=24, ry=26):
        # Red Head Base
        self._ell(d, cx, cy, rx, ry, self.RED, outline=self.RED_DARK, width=1.2)

        # Webbing grid on mask
        mcx, mcy = self._mx(cx), self._my(cy)
        # Vertical webbing
        for ox in (-12, -5, 5, 12):
            d.line([(self._mx(cx + ox * 0.7), self._my(cy - ry + 4)),
                    (self._mx(cx + ox), self._my(cy + ry - 4))], fill=self.WEB_BLACK, width=max(1, self._s(0.8)))
        # Horizontal arcs
        for oy in (-10, 0, 10):
            d.line([(self._mx(cx - rx + 4), self._my(cy + oy)),
                    (self._mx(cx + rx - 4), self._my(cy + oy))], fill=self.WEB_BLACK, width=max(1, self._s(0.8)))

        # Iconic White Angular Eyes with Thick Black Rims
        eye_l_pts = [(cx - 18, cy - 8), (cx - 4, cy - 1), (cx - 5, cy + 9), (cx - 19, cy + 3)]
        eye_r_pts = [(cx + 4, cy - 1), (cx + 18, cy - 8), (cx + 19, cy + 3), (cx + 5, cy + 9)]

        self._pol(d, eye_l_pts, self.EYE_WHITE, outline=self.EYE_BLACK, width=2.4)
        self._pol(d, eye_r_pts, self.EYE_WHITE, outline=self.EYE_BLACK, width=2.4)

    def draw_idle(self, frame):
        img = Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = 80
        breath = math.sin(frame * 0.25) * 1.5

        # Shadow
        self._ell(d, cx, 148, 36, 7, (20, 20, 35, 60))

        # Legs (Blue with Red Boots)
        # Left Leg
        self._ell(d, cx - 14, 115, 7, 18, self.BLUE, outline=self.BLUE_DARK, width=1)
        self._ell(d, cx - 14, 138, 8, 10, self.RED, outline=self.RED_DARK, width=1)
        # Right Leg
        self._ell(d, cx + 14, 115, 7, 18, self.BLUE, outline=self.BLUE_DARK, width=1)
        self._ell(d, cx + 14, 138, 8, 10, self.RED, outline=self.RED_DARK, width=1)

        # Torso (Red & Blue with Spider Emblem)
        by = 88 + breath
        self._ell(d, cx, by, 22, 22, self.RED, outline=self.RED_DARK, width=1)
        # Blue sides
        self._ell(d, cx - 16, by + 4, 8, 14, self.BLUE)
        self._ell(d, cx + 16, by + 4, 8, 14, self.BLUE)

        # Black Spider Emblem
        self._ell(d, cx, by - 2, 3.5, 5, (10, 10, 15, 255))
        for leg_y in (-3, 0, 3):
            d.line([(self._mx(cx - 7), self._my(by + leg_y)), (self._mx(cx + 7), self._my(by + leg_y))], fill=(10, 10, 15, 255), width=self._s(1.2))

        # Arms (Red gloves)
        arm_bob = math.sin(frame * 0.3) * 2
        self._ell(d, cx - 22, by + 6 + arm_bob, 6, 15, self.RED)
        self._ell(d, cx + 22, by + 6 - arm_bob, 6, 15, self.RED)

        # Head & Mask
        hy = 52 + breath * 0.7
        self._draw_spidey_mask(d, cx, hy)

        return img

    def draw_web_swing(self, frame):
        img = Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = 80
        swing_angle = math.sin(frame * 0.35) * 25
        rad = math.radians(swing_angle)

        # Taut Web line going up to ceiling
        web_anchor_x = cx + math.sin(rad) * 40
        hand_x = cx + 8
        hand_y = 35
        d.line([(self._mx(web_anchor_x), self._my(0)), (self._mx(hand_x), self._my(hand_y))], fill=self.WEB_WHITE, width=self._s(2.2))
        d.line([(self._mx(web_anchor_x), self._my(0)), (self._mx(hand_x), self._my(hand_y))], fill=(200, 225, 255, 200), width=self._s(1.0))

        # Dynamic Acrobat Spidey in air
        by = 78
        # Arm reaching up holding web
        self._ell(d, hand_x, hand_y + 10, 5, 14, self.RED)

        # Tucked Legs
        self._ell(d, cx - 18, by + 22, 9, 14, self.BLUE)
        self._ell(d, cx - 22, by + 34, 8, 9, self.RED)
        self._ell(d, cx + 12, by + 24, 9, 14, self.BLUE)
        self._ell(d, cx + 16, by + 36, 8, 9, self.RED)

        # Torso
        self._ell(d, cx, by, 20, 20, self.RED)
        self._ell(d, cx - 12, by + 4, 7, 12, self.BLUE)
        self._ell(d, cx + 12, by + 4, 7, 12, self.BLUE)

        # Head tilted into the swing
        self._draw_spidey_mask(d, cx - 2, 54)

        return img

    def draw_wall_crawl(self, frame):
        img = Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = 80
        step = (frame % 8)
        crawl_shift = math.sin(step * math.pi / 4) * 4

        # Splayed wall crawl hands and feet sticking to the wall
        # Left wall contact
        self._ell(d, 35, 55 + crawl_shift, 6, 8, self.RED)  # Top hand
        self._ell(d, 35, 105 - crawl_shift, 6, 8, self.RED) # Bottom hand
        self._ell(d, 48, 65, 8, 16, self.BLUE)
        self._ell(d, 48, 95, 8, 16, self.BLUE)

        # Torso flat against wall
        self._ell(d, 70, 80, 18, 22, self.RED)
        self._ell(d, 70, 80, 14, 18, self.BLUE)

        # Back limbs
        self._ell(d, 96, 60 - crawl_shift, 7, 14, self.BLUE)
        self._ell(d, 108, 55 - crawl_shift, 6, 7, self.RED)
        self._ell(d, 96, 100 + crawl_shift, 7, 14, self.BLUE)
        self._ell(d, 108, 105 + crawl_shift, 6, 7, self.RED)

        # Head turned facing user
        self._draw_spidey_mask(d, 70, 48)

        # Little suction web splats on contact points
        d.line([(self._mx(35), self._my(55)), (self._mx(20), self._my(55))], fill=self.WEB_WHITE, width=self._s(1.5))
        d.line([(self._mx(35), self._my(105)), (self._mx(20), self._my(105))], fill=self.WEB_WHITE, width=self._s(1.5))

        return img

    def draw_thwip(self, frame):
        img = Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = 80

        # Heroic shooting pose
        # Torso & Legs
        self._ell(d, cx - 14, 120, 8, 18, self.BLUE)
        self._ell(d, cx + 14, 120, 8, 18, self.BLUE)
        self._ell(d, cx, 88, 22, 22, self.RED)

        # Arm extended forward shooting web
        arm_end_x = cx + 38
        arm_end_y = 80
        self._ell(d, cx + 22, 84, 18, 6, self.RED)

        # Dynamic Web Blast line expanding outward
        web_reach = min(150, 40 + (frame % 15) * 8)
        d.line([(self._mx(arm_end_x), self._my(arm_end_y)), (self._mx(arm_end_x + web_reach), self._my(arm_end_y - 20))], fill=self.WEB_WHITE, width=self._s(2.5))
        d.line([(self._mx(arm_end_x), self._my(arm_end_y)), (self._mx(arm_end_x + web_reach - 10), self._my(arm_end_y - 30))], fill=self.WEB_WHITE, width=self._s(1.2))
        d.line([(self._mx(arm_end_x), self._my(arm_end_y)), (self._mx(arm_end_x + web_reach - 10), self._my(arm_end_y - 10))], fill=self.WEB_WHITE, width=self._s(1.2))

        # Head
        self._draw_spidey_mask(d, cx, 52)

        return img

root = tk.Tk()
root.withdraw()
spidey = TestSpidermanRenderer()
i1 = spidey.draw_idle(0)
i2 = spidey.draw_web_swing(0)
i3 = spidey.draw_wall_crawl(0)
i4 = spidey.draw_thwip(0)
print("Spider-Man test SUCCESS, all 4 poses rendered!")
