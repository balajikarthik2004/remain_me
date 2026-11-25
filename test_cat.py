import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math

class TestCatRenderer:
    """Cute Cat Renderer with pointy ears, whiskers, emerald eyes, and fluffy tail."""
    AA = 4
    FUR_BASE = (255, 235, 210, 255)       # Cream fur
    FUR_ORANGE = (235, 140, 60, 255)      # Calico ginger patch
    FUR_DARK = (60, 45, 40, 255)          # Dark patch
    EAR_INNER = (255, 180, 190, 255)      # Soft pink ear
    EYE_EMERALD = (40, 190, 120, 255)     # Glowing emerald eyes
    EYE_PUPIL = (15, 25, 20, 255)
    NOSE_PINK = (255, 140, 160, 255)
    WHISKER_COLOR = (90, 75, 70, 200)

    def __init__(self, w=96, h=88, tcolor="#FF00FF"):
        self.w, self.h = w, h
        self.tcolor = tcolor
        self.aw, self.ah = w * self.AA, h * self.AA
        self.direction = 1
        self.sx = self.w / 160.0
        self.sy = self.h / 140.0

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

    def draw_sit(self, frame):
        img = Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = 80
        breath = math.sin(frame * 0.25) * 1.5
        tail_swish = math.sin(frame * 0.35) * 14

        # Ground contact shadow
        self._ell(d, cx, 126, 38, 7.5, (30, 30, 45, 50))

        # Fluffy curved cat tail
        bx, by = cx + 24, 108
        tx = bx + math.sin(math.radians(tail_swish)) * 26 + 14
        ty = by - 18 + math.cos(math.radians(tail_swish)) * 6
        self._ell(d, tx, ty, 6.5, 7, self.FUR_ORANGE)
        self._ell(d, (bx + tx) / 2, (by + ty) / 2, 7.5, 9, self.FUR_BASE)
        self._ell(d, bx, by, 8, 10, self.FUR_BASE)

        # Body
        body_y = 86 + breath
        self._ell(d, cx, body_y, 28, 25, self.FUR_BASE)
        # Ginger Calico patch on back
        self._ell(d, cx + 12, body_y - 2, 14, 16, self.FUR_ORANGE)
        self._ell(d, cx - 14, body_y + 4, 10, 12, self.FUR_DARK)
        # Cream chest
        self._ell(d, cx - 4, body_y + 4, 14, 18, (255, 255, 255, 245))

        # Front paws tucked neatly
        self._ell(d, cx - 10, 119, 7.5, 5.5, (255, 255, 255, 255), outline=(220, 200, 190, 255), width=1)
        self._ell(d, cx + 10, 119, 7.5, 5.5, (255, 255, 255, 255), outline=(220, 200, 190, 255), width=1)

        # Head
        hy = 52 + breath * 0.6
        # Pointy Cat Ears
        ear_l = [(cx - 24, hy + 2), (cx - 18, hy - 24), (cx - 4, hy - 8)]
        ear_r = [(cx + 4, hy - 8), (cx + 18, hy - 24), (cx + 24, hy + 2)]
        self._pol(d, ear_l, self.FUR_BASE, outline=(210, 180, 160, 255), width=1)
        self._pol(d, ear_r, self.FUR_ORANGE, outline=(200, 110, 40, 255), width=1)

        inner_l = [(cx - 20, hy - 2), (cx - 17, hy - 18), (cx - 8, hy - 8)]
        inner_r = [(cx + 8, hy - 8), (cx + 17, hy - 18), (cx + 20, hy - 2)]
        self._pol(d, inner_l, self.EAR_INNER)
        self._pol(d, inner_r, self.EAR_INNER)

        # Head sphere
        self._ell(d, cx, hy, 27, 22, self.FUR_BASE)
        self._ell(d, cx + 10, hy - 6, 12, 10, self.FUR_ORANGE)

        # Big Emerald Cat Eyes with slit specular pupils
        blink_cycle = (frame % 40)
        is_blink = 36 <= blink_cycle <= 38
        if is_blink:
            # Closed happy curved eye
            d.line([(self._mx(cx - 15), self._my(hy - 2)), (self._mx(cx - 5), self._my(hy - 2))], fill=(40, 30, 25, 255), width=self._s(2))
            d.line([(self._mx(cx + 5), self._my(hy - 2)), (self._mx(cx + 15), self._my(hy - 2))], fill=(40, 30, 25, 255), width=self._s(2))
        else:
            self._ell(d, cx - 10, hy - 2, 6.5, 7, self.EYE_EMERALD)
            self._ell(d, cx - 10, hy - 2, 2.4, 5.5, self.EYE_PUPIL)
            self._ell(d, cx - 12, hy - 4, 2.0, 2.0, (255, 255, 255, 255))

            self._ell(d, cx + 10, hy - 2, 6.5, 7, self.EYE_EMERALD)
            self._ell(d, cx + 10, hy - 2, 2.4, 5.5, self.EYE_PUPIL)
            self._ell(d, cx + 8, hy - 4, 2.0, 2.0, (255, 255, 255, 255))

        # Tiny Pink Button Nose & Mouth
        self._pol(d, [(cx - 3, hy + 5), (cx + 3, hy + 5), (cx, hy + 8)], self.NOSE_PINK)
        # Whiskers
        for wy in (-2, 2):
            d.line([(self._mx(cx - 12), self._my(hy + 7 + wy)), (self._mx(cx - 32), self._my(hy + 6 + wy * 2))], fill=self.WHISKER_COLOR, width=self._s(1))
            d.line([(self._mx(cx + 12), self._my(hy + 7 + wy)), (self._mx(cx + 32), self._my(hy + 6 + wy * 2))], fill=self.WHISKER_COLOR, width=self._s(1))

        return img

root = tk.Tk()
root.withdraw()
cat = TestCatRenderer()
res = cat.draw_sit(0)
print("Cat renderer test SUCCESS, size:", res.size)
