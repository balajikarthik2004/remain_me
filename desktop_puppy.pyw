"""
🐾 Desktop Puppy — Real Cute Puppy Desktop Companion & Stealth Anti-Idle Widget
A delightful, animated desktop puppy companion with undetectable Win32 anti-idle utilities.

Features:
- Real Cute Puppy: 4x supersampled, anti-aliased golden puppy with soulful eyes,
  floppy bouncy ears, wet button nose, chubby cheeks, fluffy wagging tail & paws.
- 4 Expressive Poses: Sit/Idle (blinking & breathing), Walk (bouncy trot), Wag (ecstatic joy with hearts), Sleep (cozy donut with Zzz).
- Interactive Kawaii Speech Bubble: Friendly thoughts, woofs, and status updates above puppy.
- Modern Windows 11 UI: Glassmorphic notification slider, sleek capsule status badge, high-res tray icon.
- Undetectable Anti-Idle: Native Win32 SendInput (ctypes), hardware scancodes, smooth Bezier curves.
- Global Hotkeys: Ctrl+B (Toggle Awake), Ctrl+Shift+Q (Hide/Show Puppy).
- Customizable Size: Small (default 92px - compact), Tiny (76px), Medium (110px).

Requirements: pip install Pillow pystray
"""

import tkinter as tk
import random
import math
import time
import threading
import ctypes
import ctypes.wintypes
import sys
import os
import hashlib

# ══════════════════════════════════════════════════════════════════════
#  SINGLE INSTANCE — mutex prevents duplicates
# ══════════════════════════════════════════════════════════════════════

MUTEX_NAME = "Global\\WinSvcHelper_" + hashlib.md5(
    os.path.abspath(__file__).encode()).hexdigest()[:12]

def ensure_single_instance():
    k32 = ctypes.windll.kernel32
    mutex = k32.CreateMutexW(None, True, MUTEX_NAME)
    if k32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        try:
            import subprocess
            subprocess.Popen('taskkill /F /IM pythonw.exe 2>nul',
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1.5)
            k32.CloseHandle(mutex)
            mutex = k32.CreateMutexW(None, True, MUTEX_NAME)
        except Exception:
            pass
    return mutex

INSTANCE_MUTEX = ensure_single_instance()

# ══════════════════════════════════════════════════════════════════════
#  DEPENDENCIES — install silently if missing
# ══════════════════════════════════════════════════════════════════════

def _pip(pkg):
    os.system(f'"{sys.executable}" -m pip install {pkg} --quiet')

try:
    from PIL import Image, ImageDraw, ImageTk, ImageFont
except ImportError:
    _pip("Pillow")
    from PIL import Image, ImageDraw, ImageTk, ImageFont

try:
    import pystray
except ImportError:
    _pip("pystray")
    import pystray


# ══════════════════════════════════════════════════════════════════════
#  NATIVE WIN32 INPUT — direct ctypes, no automation libraries
# ══════════════════════════════════════════════════════════════════════

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

ES_CONTINUOUS       = 0x80000000
ES_SYSTEM_REQUIRED  = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def prevent_sleep():
    kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)

def allow_sleep():
    kernel32.SetThreadExecutionState(ES_CONTINUOUS)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
MOUSEEVENTF_MOVE = 0x0001
KEYEVENTF_KEYUP  = 0x0002
KEYEVENTF_SCANCODE = 0x0008

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("union", INPUT_UNION)]

def _send(inputs):
    n = len(inputs)
    arr = (INPUT * n)(*inputs)
    user32.SendInput(n, ctypes.byref(arr), ctypes.sizeof(INPUT))

def get_cursor_pos():
    pt = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def get_screen_size():
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def move_mouse_relative(dx, dy):
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.union.mi.dx = dx
    inp.union.mi.dy = dy
    inp.union.mi.dwFlags = MOUSEEVENTF_MOVE
    inp.union.mi.mouseData = 0
    inp.union.mi.time = 0
    inp.union.mi.dwExtraInfo = None
    _send([inp])

def move_mouse_smooth(dx, dy, steps=None):
    dist = math.sqrt(dx*dx + dy*dy)
    if steps is None:
        steps = max(4, min(18, int(dist / 2)))
    cx_off = random.uniform(-3, 3)
    cy_off = random.uniform(-3, 3)
    px, py = 0.0, 0.0
    for i in range(1, steps + 1):
        t = i / steps
        bx = 2*(1-t)*t*cx_off + t*t*dx
        by = 2*(1-t)*t*cy_off + t*t*dy
        sx, sy = round(bx - px), round(by - py)
        if sx or sy:
            move_mouse_relative(sx, sy)
        px += sx
        py += sy
        time.sleep(random.uniform(0.008, 0.025))

def press_key_scancode(scan):
    down = INPUT(); down.type = INPUT_KEYBOARD
    down.union.ki.wVk = 0; down.union.ki.wScan = scan
    down.union.ki.dwFlags = KEYEVENTF_SCANCODE
    down.union.ki.time = 0; down.union.ki.dwExtraInfo = None
    up = INPUT(); up.type = INPUT_KEYBOARD
    up.union.ki.wVk = 0; up.union.ki.wScan = scan
    up.union.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
    up.union.ki.time = 0; up.union.ki.dwExtraInfo = None
    _send([down])
    time.sleep(random.uniform(0.03, 0.08))
    _send([up])

def press_harmless_key():
    press_key_scancode(random.choice([0x2A, 0x36, 0x1D]))  # Shift/Ctrl

WM_HOTKEY     = 0x0312
MOD_CONTROL   = 0x0002
MOD_SHIFT     = 0x0004
HOTKEY_TOGGLE = 1
HOTKEY_HIDE   = 2


# ══════════════════════════════════════════════════════════════════════
#  REAL CUTE PUPPY RENDERER — 4× Supersampled Anti-Aliasing
# ══════════════════════════════════════════════════════════════════════

class PuppyRenderer:
    """
    Renders an adorable, real-looking cute puppy with rich fur shading,
    soulful puppy-dog eyes with specular highlights, floppy bouncy ears,
    cute button nose, chubby cheeks, soft paws, and expressive animations.
    Uses 4x supersampling (anti-aliasing) and Lanczos downsampling.
    """
    AA = 4

    # Palette: Warm Golden / Honey Puppy
    FUR_BASE      = (242, 172, 98, 255)     # Warm golden honey fur
    FUR_LIGHT     = (255, 218, 168, 255)    # Top head & forehead highlight
    FUR_SHADOW    = (205, 128, 56, 255)     # Underbody & ear depth
    FUR_DEEP      = (164, 94, 34, 255)      # Crease shadows
    MUZZLE_BASE   = (255, 246, 235, 255)    # Soft cream muzzle & chest
    MUZZLE_SHADOW = (238, 220, 202, 255)    # Muzzle underside
    EAR_OUTER     = (214, 138, 62, 255)     # Floppy ear fur
    EAR_INNER     = (255, 188, 170, 255)    # Soft warm peach inside ear
    EAR_SHADOW    = (175, 102, 40, 255)     # Behind ear depth
    
    EYE_DARK      = (26, 14, 8, 255)        # Deep espresso pupil
    EYE_IRIS      = (65, 34, 16, 255)       # Rich warm brown iris
    EYE_RIM       = (110, 58, 24, 255)      # Soft warm lower iris reflection
    EYE_WHITE     = (255, 255, 255, 255)    # Eye sparkle highlights
    
    NOSE_BASE     = (34, 22, 18, 255)       # Soft rounded black button nose
    NOSE_SHINE    = (110, 95, 90, 255)      # Wet nose specular shine
    
    TONGUE        = (255, 118, 142, 255)    # Rosy pink tongue
    TONGUE_SHADOW = (220, 80, 104, 255)     # Tongue groove
    
    CHEEK_BLUSH   = (255, 150, 168, 140)    # Soft radial blush
    PAW_PAD       = (255, 170, 175, 255)    # Cute pink toe pads
    
    COLLAR_COLOR  = (72, 170, 245, 255)     # Sky blue collar
    COLLAR_SHADOW = (40, 120, 190, 255)
    TAG_GOLD      = (255, 215, 60, 255)     # Golden star / bell tag
    TAG_SHINE     = (255, 245, 180, 255)

    SHADOW_COLOR  = (40, 40, 60, 65)        # Soft ground contact shadow
    HEART_COLOR   = (255, 82, 120, 255)
    SPARKLE_COLOR = (255, 230, 90, 255)

    def __init__(self, w=92, h=84, tcolor="#FF00FF"):
        self.w = w
        self.h = h
        self.tcolor = tcolor
        self.aw = w * self.AA
        self.ah = h * self.AA
        self.direction = 1  # 1 = face right, -1 = face left
        # Coordinate design space: 160 x 140
        self.sx = self.w / 160.0
        self.sy = self.h / 140.0

    def set_size(self, w, h):
        self.w = w
        self.h = h
        self.aw = w * self.AA
        self.ah = h * self.AA
        self.sx = self.w / 160.0
        self.sy = self.h / 140.0

    def _new(self):
        return Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))

    def _s(self, v):
        return int(v * self.AA)

    def _mx(self, x):
        """Map x with direction mirroring."""
        x_mapped = x * self.sx
        if self.direction == -1:
            x_mapped = self.w - x_mapped
        return self._s(x_mapped)

    def _my(self, y):
        return self._s(y * self.sy)

    def _ell(self, d, cx, cy, rx, ry, fill, outline=None, width=1):
        mcx, mcy = self._mx(cx), self._my(cy)
        mrx, mry = self._s(rx * self.sx), self._s(ry * self.sy)
        box = [mcx - mrx, mcy - mry, mcx + mrx, mcy + mry]
        if outline:
            d.ellipse(box, fill=fill, outline=outline, width=max(1, self._s(width * min(self.sx, self.sy))))
        else:
            d.ellipse(box, fill=fill)

    def _cir(self, d, cx, cy, r, fill, outline=None, width=1):
        self._ell(d, cx, cy, r, r, fill, outline, width)

    def _pol(self, d, pts, fill, outline=None, width=1):
        mapped = [(self._mx(x), self._my(y)) for x, y in pts]
        d.polygon(mapped, fill=fill)
        if outline:
            mapped_closed = mapped + [mapped[0]]
            d.line(mapped_closed, fill=outline, width=max(1, self._s(width * min(self.sx, self.sy))))

    def _arc(self, d, cx, cy, rx, ry, start, end, fill, width=1.5):
        mcx, mcy = self._mx(cx), self._my(cy)
        mrx, mry = self._s(rx * self.sx), self._s(ry * self.sy)
        box = [mcx - mrx, mcy - mry, mcx + mrx, mcy + mry]
        s, e = start, end
        if self.direction == -1:
            s, e = 180 - end, 180 - start
        d.arc(box, s, e, fill=fill, width=max(1, self._s(width * min(self.sx, self.sy))))

    def _render(self, img):
        """Downscale with Lanczos and composite onto TCOLOR to prevent halo."""
        resized = img.resize((self.w, self.h), Image.LANCZOS)
        # Parse TCOLOR hex to RGB
        tc = self.tcolor.lstrip('#')
        r_t, g_t, b_t = tuple(int(tc[i:i+2], 16) for i in (0, 2, 4))
        
        bg = Image.new("RGBA", (self.w, self.h), (r_t, g_t, b_t, 255))
        alpha = resized.split()[-1]
        clean_mask = alpha.point(lambda p: 255 if p >= 70 else 0)
        
        final_img = Image.composite(resized.convert("RGB"), bg.convert("RGB"), clean_mask)
        return ImageTk.PhotoImage(final_img)

    def _ground_shadow(self, d, cx=80, cy=126, rx=40, ry=9):
        self._ell(d, cx, cy, rx, ry, (30, 30, 50, 45))
        self._ell(d, cx, cy, rx * 0.7, ry * 0.6, (20, 20, 35, 75))

    def _draw_eye(self, d, ex, ey, r=6.5, blink=0.0, happy=False):
        """Draws realistic soulful shiny puppy eyes."""
        if happy or blink > 0.7:
            self._arc(d, ex, ey + 1, r * 1.1, r * 0.8, 195, 345, self.EYE_DARK, width=2.4)
            self._arc(d, ex + (1 if self.direction == 1 else -1) * 3, ey + 2, r * 0.6, r * 0.4, 210, 330, self.EYE_DARK, width=1.8)
            return

        if blink > 0.0:
            ry = max(1.5, r * (1.0 - blink))
            self._ell(d, ex, ey, r, ry, self.EYE_DARK)
            self._cir(d, ex - 2, ey - 1, 1.8, self.EYE_WHITE)
            return

        self._cir(d, ex, ey, r, self.EYE_DARK)
        self._ell(d, ex, ey + 2, r * 0.85, r * 0.55, self.EYE_RIM)
        self._ell(d, ex, ey + 1, r * 0.7, r * 0.45, self.EYE_IRIS)
        self._cir(d, ex, ey - 0.5, r * 0.65, self.EYE_DARK)

        # Soulful light highlights
        self._cir(d, ex - 2.2, ey - 2.2, 2.5, self.EYE_WHITE)
        self._cir(d, ex + 2.0, ey + 2.0, 1.4, (255, 255, 255, 200))
        self._cir(d, ex - 1.0, ey + 2.8, 0.9, (255, 255, 255, 160))

    def _draw_muzzle_and_nose(self, d, cx, cy, open_mouth=False, tongue=False):
        """Draws the cute cream muzzle pads, shiny wet nose, and sweet smile."""
        self._ell(d, cx - 7, cy + 3, 11, 8.5, self.MUZZLE_BASE)
        self._ell(d, cx + 7, cy + 3, 11, 8.5, self.MUZZLE_BASE)
        self._ell(d, cx, cy + 4, 13, 7.5, self.MUZZLE_BASE)
        self._ell(d, cx, cy + 6, 8, 4.5, self.MUZZLE_SHADOW)

        # Cheek blush
        self._cir(d, cx - 19, cy + 2, 5.5, self.CHEEK_BLUSH)
        self._cir(d, cx + 19, cy + 2, 5.5, self.CHEEK_BLUSH)

        # Mouth & Tongue
        if tongue or open_mouth:
            self._ell(d, cx, cy + 7.5, 6, 5, (80, 20, 30, 255))
            self._ell(d, cx + 1, cy + 10, 4.8, 6.5, self.TONGUE)
            self._arc(d, cx + 1, cy + 8.5, 1.5, 4, 70, 110, self.TONGUE_SHADOW, width=1.5)
            self._cir(d, cx + 0.5, cy + 13, 1.4, (255, 200, 215, 220))
        else:
            self._arc(d, cx - 4.5, cy + 5, 5, 4.5, 15, 165, self.EYE_DARK, width=1.8)
            self._arc(d, cx + 4.5, cy + 5, 5, 4.5, 15, 165, self.EYE_DARK, width=1.8)

        # Nose bridge crease
        self._arc(d, cx, cy - 2, 1, 3, 70, 110, self.FUR_DEEP, width=1.2)

        # Button nose with wet highlight reflection
        self._ell(d, cx, cy, 6.5, 4.8, self.NOSE_BASE)
        self._ell(d, cx - 1.5, cy - 1.6, 3.2, 1.6, self.NOSE_SHINE)
        self._cir(d, cx - 2.2, cy - 2.0, 1.0, (255, 255, 255, 200))
        self._cir(d, cx - 3.2, cy + 1.2, 1.1, (15, 10, 8, 255))
        self._cir(d, cx + 3.2, cy + 1.2, 1.1, (15, 10, 8, 255))

    def _draw_floppy_ear(self, d, cx, cy, side=-1, perk=0.0):
        """Draws an adorable floppy puppy ear with natural fold."""
        s = side
        ex = cx + s * 22
        ey = cy - 14 + perk
        
        ear_pts = [
            (ex - s * 4, ey - 6),
            (ex + s * 14, ey - 4),
            (ex + s * 20, ey + 12 + perk),
            (ex + s * 16, ey + 28 + perk * 1.5),
            (ex + s * 7, ey + 32 + perk * 1.5),
            (ex - s * 2, ey + 24 + perk),
            (ex - s * 5, ey + 8),
        ]
        self._pol(d, ear_pts, self.EAR_OUTER, outline=self.EAR_SHADOW, width=1.2)

        inner_pts = [
            (ex + s * 1, ey + 4),
            (ex + s * 12, ey + 6),
            (ex + s * 15, ey + 18 + perk),
            (ex + s * 10, ey + 25 + perk),
            (ex + s * 3, ey + 18),
        ]
        self._pol(d, inner_pts, self.EAR_INNER)
        self._arc(d, ex + s * 8, ey + 6, 8, 4, 180 if s == 1 else 0, 360 if s == 1 else 180, self.FUR_LIGHT, width=1.4)

    def _draw_collar(self, d, cx, cy, wag=0.0):
        """Cute sky blue collar with a sparkling gold bell tag."""
        self._ell(d, cx, cy, 21, 6.5, self.COLLAR_COLOR, outline=self.COLLAR_SHADOW, width=1.2)
        self._arc(d, cx, cy - 1, 19, 4.5, 190, 350, (130, 210, 255, 255), width=1.5)
        
        tx = cx + wag * 0.4
        ty = cy + 6.5
        self._cir(d, tx, ty, 4.2, self.TAG_GOLD, outline=(180, 140, 20, 255), width=1.0)
        self._cir(d, tx - 1.2, ty - 1.2, 1.5, self.TAG_SHINE)
        self._cir(d, tx, ty + 1.2, 0.9, (120, 80, 10, 255))

    def _draw_fluffy_tail(self, d, cx, cy, wag_angle=0.0, happy=False):
        """Draws a cute curved fluffy puppy tail that wags with joyful physics."""
        rad = math.radians(wag_angle)
        bx, by = cx + 28, cy + 8
        tip_len = 24 if not happy else 28
        tx = bx + math.sin(rad) * tip_len + 12
        ty = by - math.cos(rad) * tip_len - 10
        mid_x = (bx + tx) / 2 + math.cos(rad) * 6
        mid_y = (by + ty) / 2 + math.sin(rad) * 4

        tail_pts = [
            (bx - 3, by + 4),
            (mid_x - 6, mid_y),
            (tx - 3, ty - 2),
            (tx + 4, ty),
            (tx + 3, ty + 5),
            (mid_x + 6, mid_y + 4),
            (bx + 4, by - 2)
        ]
        self._pol(d, tail_pts, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._cir(d, tx, ty, 5.5, self.FUR_LIGHT)
        self._cir(d, tx + 1, ty - 1, 3.5, self.MUZZLE_BASE)

    # ── SIT / IDLE ──────────────────────────────────────────
    def draw_sit(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        breath = math.sin(frame * 0.25) * 1.5
        wag = math.sin(frame * 0.5) * 18
        ear_bob = math.sin(frame * 0.25) * 1.0

        self._ground_shadow(d, cx, 126, 42, 8)
        self._draw_fluffy_tail(d, cx - 2, 82 + breath, wag_angle=20 + wag)

        # Hind legs
        self._ell(d, cx - 25, 102, 13, 16, self.FUR_SHADOW)
        self._ell(d, cx + 25, 102, 13, 16, self.FUR_SHADOW)
        self._ell(d, cx - 27, 118, 9, 6, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)
        self._ell(d, cx + 27, 118, 9, 6, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)
        self._cir(d, cx - 27, 119, 2.5, self.PAW_PAD)
        self._cir(d, cx + 27, 119, 2.5, self.PAW_PAD)

        # Body
        by = 82 + breath
        self._ell(d, cx, by, 30, 26, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._ell(d, cx, by + 4, 18, 20, self.MUZZLE_BASE)
        self._ell(d, cx, by + 12, 13, 12, (255, 255, 255, 230))

        # Front legs
        for lx in (cx - 11, cx + 11):
            self._ell(d, lx, by + 24, 6.5, 14, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)
            self._ell(d, lx, 120, 8, 5.5, self.FUR_LIGHT, outline=self.FUR_SHADOW, width=1.1)
            self._cir(d, lx - 2.5, 121, 1.2, self.FUR_DEEP)
            self._cir(d, lx + 2.5, 121, 1.2, self.FUR_DEEP)

        self._draw_collar(d, cx, by - 12, wag=wag * 0.2)

        # Head
        hy = 46 + breath * 0.6
        self._draw_floppy_ear(d, cx, hy, side=-1, perk=ear_bob)
        self._draw_floppy_ear(d, cx, hy, side=1, perk=-ear_bob)

        self._ell(d, cx, hy, 28, 25, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._ell(d, cx, hy - 8, 18, 12, self.FUR_LIGHT)
        self._ell(d, cx, hy - 13, 10, 6, (255, 245, 225, 200))

        blink_cycle = (frame % 36)
        blink = 1.0 if 32 <= blink_cycle <= 34 else 0.0
        self._draw_eye(d, cx - 11, hy - 1, r=6.5, blink=blink)
        self._draw_eye(d, cx + 11, hy - 1, r=6.5, blink=blink)

        self._ell(d, cx - 11, hy - 9, 3.8, 2.0, self.FUR_LIGHT)
        self._ell(d, cx + 11, hy - 9, 3.8, 2.0, self.FUR_LIGHT)

        tongue_out = (frame % 20 < 8)
        self._draw_muzzle_and_nose(d, cx, hy + 9, tongue=tongue_out)

        return self._render(img)

    # ── WALK ────────────────────────────────────────────────
    def draw_walk(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        f = frame % 8
        phase = math.sin(f * math.pi / 4)
        bounce = abs(math.sin(f * math.pi / 4)) * 3.5
        wag = math.sin(frame * 1.2) * 22
        ear_flop = math.sin(frame * 1.2) * 3.5

        self._ground_shadow(d, cx, 126, 38 - bounce * 0.8, 7.5)
        self._draw_fluffy_tail(d, cx - 6, 80 - bounce, wag_angle=-10 + wag, happy=True)

        by = 80 - bounce

        b_leg_l = cx - 18
        b_leg_r = cx + 16
        b_lift_l = max(0, -phase * 7)
        b_lift_r = max(0, phase * 7)

        self._ell(d, b_leg_l, by + 18 - b_lift_l, 7, 13, self.FUR_SHADOW)
        self._ell(d, b_leg_l, 120 - b_lift_l, 7.5, 5, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)

        self._ell(d, b_leg_r, by + 18 - b_lift_r, 7, 13, self.FUR_SHADOW)
        self._ell(d, b_leg_r, 120 - b_lift_r, 7.5, 5, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)

        self._ell(d, cx, by, 31, 24, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._ell(d, cx + 4, by + 2, 17, 18, self.MUZZLE_BASE)

        f_leg_l = cx - 9
        f_leg_r = cx + 14
        f_lift_l = max(0, phase * 8)
        f_lift_r = max(0, -phase * 8)

        self._ell(d, f_leg_l, by + 22 - f_lift_l, 6, 13, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)
        self._ell(d, f_leg_l, 121 - f_lift_l, 7.5, 5.5, self.FUR_LIGHT, outline=self.FUR_SHADOW, width=1.1)

        self._ell(d, f_leg_r, by + 22 - f_lift_r, 6, 13, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)
        self._ell(d, f_leg_r, 121 - f_lift_r, 7.5, 5.5, self.FUR_LIGHT, outline=self.FUR_SHADOW, width=1.1)

        self._draw_collar(d, cx + 2, by - 10, wag=wag * 0.3)

        hy = 44 - bounce * 0.8
        self._draw_floppy_ear(d, cx + 2, hy, side=-1, perk=-ear_flop)
        self._draw_floppy_ear(d, cx + 2, hy, side=1, perk=ear_flop)

        self._ell(d, cx + 2, hy, 27, 24, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._ell(d, cx + 2, hy - 7, 17, 11, self.FUR_LIGHT)

        self._draw_eye(d, cx - 8, hy - 1, r=6.5)
        self._draw_eye(d, cx + 13, hy - 1, r=6.5)

        self._draw_muzzle_and_nose(d, cx + 3, hy + 9, open_mouth=True, tongue=True)

        return self._render(img)

    # ── WAG / PETTED ────────────────────────────────────────
    def draw_wag(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        wag = math.sin(frame * 1.8) * 32
        bounce = abs(math.sin(frame * 0.9)) * 6
        ear_perk = math.sin(frame * 1.2) * 5

        self._ground_shadow(d, cx, 126, 42 - bounce * 0.7, 8)
        self._draw_fluffy_tail(d, cx - 4, 78 - bounce, wag_angle=wag, happy=True)
        if abs(wag) > 15:
            d_trail = ImageDraw.Draw(img)
            self._draw_fluffy_tail(d_trail, cx - 4, 78 - bounce, wag_angle=wag * 0.6, happy=True)

        by = 78 - bounce

        for lx in (cx - 20, cx - 7, cx + 7, cx + 20):
            self._ell(d, lx, by + 22, 6, 14, self.FUR_BASE, outline=self.FUR_SHADOW, width=1)
            self._ell(d, lx, 121, 7.5, 5.5, self.FUR_LIGHT, outline=self.FUR_SHADOW, width=1)

        self._ell(d, cx, by, 31, 25, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._ell(d, cx, by + 3, 19, 19, self.MUZZLE_BASE)

        self._draw_collar(d, cx, by - 12, wag=wag * 0.5)

        hy = 42 - bounce
        self._draw_floppy_ear(d, cx, hy, side=-1, perk=ear_perk)
        self._draw_floppy_ear(d, cx, hy, side=1, perk=-ear_perk)

        self._ell(d, cx, hy, 28, 25, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._ell(d, cx, hy - 7, 18, 12, self.FUR_LIGHT)

        # Blissful curved happy eyes: ^ ‿ ^
        self._draw_eye(d, cx - 11, hy - 1, r=7, happy=True)
        self._draw_eye(d, cx + 11, hy - 1, r=7, happy=True)

        self._draw_muzzle_and_nose(d, cx, hy + 9, open_mouth=True, tongue=True)

        # Hearts and sparkles
        h_bob = math.sin(frame * 0.5) * 4
        self._draw_heart(d, cx - 36, hy - 16 + h_bob, 9, self.HEART_COLOR)
        self._draw_heart(d, cx + 34, hy - 22 - h_bob, 7.5, (255, 120, 160, 255))
        self._draw_sparkle(d, cx + 32, hy + 6 + h_bob, 5, self.SPARKLE_COLOR)
        self._draw_sparkle(d, cx - 34, hy + 8 - h_bob, 4.5, self.SPARKLE_COLOR)

        return self._render(img)

    # ── SLEEP ───────────────────────────────────────────────
    def draw_sleep(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        breath = math.sin(frame * 0.2) * 2.2
        bob = math.sin(frame * 0.2) * 3

        self._ground_shadow(d, cx, 126, 48, 8.5)

        self._ell(d, cx + 10, 104, 38, 22 + breath, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        tail_wag = math.sin(frame * 0.3) * 3
        self._arc(d, cx + 28, 102 + breath * 0.5, 20, 16, 250 + tail_wag, 80 + tail_wag, self.FUR_BASE, width=7)
        self._cir(d, cx + 38, 114, 5.5, self.FUR_LIGHT)

        self._ell(d, cx + 14, 108, 22, 13, self.MUZZLE_BASE)

        hx = cx - 18
        hy = 100 + breath * 0.6

        self._draw_floppy_ear(d, hx - 4, hy - 2, side=-1, perk=-1)

        self._ell(d, hx, hy, 22, 19, self.FUR_BASE, outline=self.FUR_SHADOW, width=1.2)
        self._ell(d, hx - 2, hy - 5, 13, 8, self.FUR_LIGHT)

        self._arc(d, hx - 5, hy - 1, 6, 4, 195, 345, self.EYE_DARK, width=2.0)

        self._ell(d, hx + 8, hy + 4, 4.5, 3.5, self.NOSE_BASE)
        self._cir(d, hx + 7, hy + 3, 1.0, self.NOSE_SHINE)

        self._cir(d, hx - 3, hy + 5, 4.5, self.CHEEK_BLUSH)

        self._ell(d, hx + 8, 118, 7.5, 5, self.FUR_LIGHT, outline=self.FUR_SHADOW, width=1)
        self._cir(d, hx + 8, 118.5, 2.0, self.PAW_PAD)

        # Dreamy floating Zzz
        try:
            fs = ImageFont.truetype("segoeui.ttf", self._s(9))
            fm = ImageFont.truetype("segoeuib.ttf", self._s(13))
            fl = ImageFont.truetype("segoeuib.ttf", self._s(17))
        except Exception:
            fs = fm = fl = ImageFont.load_default()

        c_zzz1 = (120, 185, 230, 220)
        c_zzz2 = (85, 155, 215, 240)
        c_zzz3 = (55, 125, 195, 255)

        d.text((self._mx(cx + 10), self._my(68 + bob)), "z", fill=c_zzz1, font=fs)
        d.text((self._mx(cx + 20), self._my(52 + bob)), "Z", fill=c_zzz2, font=fm)
        if (frame % 8) < 6:
            d.text((self._mx(cx + 34), self._my(34 + bob)), "Z", fill=c_zzz3, font=fl)
            self._draw_sparkle(d, cx + 48, 30 + bob, 3.5, (255, 235, 140, 220))

        return self._render(img)

    def _draw_heart(self, d, x, y, s, c):
        self._cir(d, x - s * 0.32, y, s * 0.42, c)
        self._cir(d, x + s * 0.32, y, s * 0.42, c)
        self._pol(d, [(x - s * 0.72, y + s * 0.1), (x, y + s * 0.95), (x + s * 0.72, y + s * 0.1)], c)
        self._cir(d, x - s * 0.32, y - s * 0.15, s * 0.15, (255, 255, 255, 220))

    def _draw_sparkle(self, d, x, y, r, c):
        pts = [
            (x, y - r), (x + r * 0.28, y - r * 0.28),
            (x + r, y), (x + r * 0.28, y + r * 0.28),
            (x, y + r), (x - r * 0.28, y + r * 0.28),
            (x - r, y), (x - r * 0.28, y - r * 0.28)
        ]
        self._pol(d, pts, c)


# ══════════════════════════════════════════════════════════════════════
#  WINDOWS 11 MODERN NOTIFICATION CARD
# ══════════════════════════════════════════════════════════════════════

class NotificationManager:
    """Sleek Windows 11 rounded glass notification card with slide-in physics."""
    def __init__(self, root, sw, sh):
        self.root = root
        self.sw = sw
        self.sh = sh
        self.current = None
        self.sy = 0

    def show(self, mode_on):
        if self.current:
            try: self.current.destroy()
            except Exception: pass
        
        nw = tk.Toplevel(self.root)
        nw.overrideredirect(True)
        nw.attributes("-topmost", True)
        nw.attributes("-alpha", 0.96)
        
        cw, ch = 330, 76
        sx = self.sw - cw - 24
        self.ty = self.sh - ch - 54
        self.sy = self.sh
        nw.geometry(f"{cw}x{ch}+{sx}+{self.sy}")

        # Render modern card canvas
        c = tk.Canvas(nw, width=cw, height=ch, bg="#131624", highlightthickness=0)
        c.pack(fill="both", expand=True)

        accent = "#00E676" if mode_on else "#FF5252"
        accent_bg = "#0A2818" if mode_on else "#280A12"
        
        # Border
        c.create_rectangle(0, 0, cw, ch, fill="#131624", outline="#262B44", width=1)
        # Left accent vertical glow strip
        c.create_rectangle(0, 0, 4, ch, fill=accent, outline=accent)

        # Puppy avatar badge circle on the left
        c.create_oval(14, 15, 46, 47, fill=accent_bg, outline=accent, width=1.5)
        c.create_text(30, 31, text="🐶", font=("Segoe UI Emoji", 14))

        # Title & Subtitles
        title = "AWAKE MODE ACTIVE" if mode_on else "AWAKE MODE OFF"
        c.create_text(58, 22, text=title, anchor="w",
                      font=("Segoe UI Semibold", 10), fill=accent)
        
        sub = "Stealth anti-idle active • PC stays awake" if mode_on else "Normal system sleep restored"
        c.create_text(58, 40, text=sub, anchor="w",
                      font=("Segoe UI", 8), fill="#E2E4EC")
        
        c.create_text(58, 56, text="Press Ctrl+B to toggle  •  Right-click pet for menu",
                      anchor="w", font=("Segoe UI", 7), fill="#8A92A6")

        # Right status capsule badge
        badge_text = "ON" if mode_on else "OFF"
        c.create_rectangle(cw - 52, 26, cw - 16, 48, fill=accent_bg, outline=accent, width=1)
        c.create_text(cw - 34, 37, text=badge_text,
                      font=("Segoe UI", 8, "bold"), fill=accent)

        self.current = nw
        self._slide_in(nw, sx, cw, ch)

    def _slide_in(self, nw, sx, w, h):
        if self.sy > self.ty:
            self.sy -= max(4, (self.sy - self.ty) // 3)
            try:
                nw.geometry(f"{w}x{h}+{sx}+{max(self.sy, self.ty)}")
                self.root.after(16, lambda: self._slide_in(nw, sx, w, h))
            except Exception: pass
        else:
            self.root.after(3500, lambda: self._slide_out(nw, sx, w, h))

    def _slide_out(self, nw, sx, w, h):
        self.sy += max(5, (self.sh - self.sy) // 4)
        if self.sy > self.sh:
            try: nw.destroy()
            except Exception: pass
            if self.current is nw: self.current = None
        else:
            try:
                nw.geometry(f"{w}x{h}+{sx}+{self.sy}")
                self.root.after(16, lambda: self._slide_out(nw, sx, w, h))
            except Exception: pass


# ══════════════════════════════════════════════════════════════════════
#  MODERN STATUS BADGE
# ══════════════════════════════════════════════════════════════════════

class StatusBadge:
    """Sleek capsule status pill above system tray."""
    def __init__(self, root, sw, sh, on_toggle=None):
        self.root = root; self.sw = sw; self.sh = sh
        self.win = None; self.pf = 0
        self.on_toggle = on_toggle

    def show(self, active):
        if self.win:
            try: self.win.destroy()
            except Exception: pass
            self.win = None
        if not active: return

        self.win = tk.Toplevel(self.root)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", 0.92)
        bw, bh = 94, 26
        self.win.geometry(f"{bw}x{bh}+{self.sw-bw-16}+{self.sh-bh-50}")
        
        self.bc = tk.Canvas(self.win, width=bw, height=bh,
                            bg="#131624", highlightthickness=0)
        self.bc.pack(fill="both", expand=True)
        self.bc.create_rectangle(0, 0, bw, bh, fill="#131624", outline="#262B44")
        
        self.dot = self.bc.create_oval(10, 8, 18, 16, fill="#00E676", outline="#00C853")
        self.bc.create_text(26, 13, text="AWAKE", anchor="w",
                            font=("Segoe UI Semibold", 8), fill="#00E676")
        self.bc.create_text(70, 13, text="Ctrl+B", anchor="w",
                            font=("Segoe UI", 6), fill="#7B8399")
        
        if self.on_toggle:
            self.bc.bind("<Button-1>", lambda e: self.on_toggle())
        self._pulse()

    def _pulse(self):
        if not self.win: return
        self.pf += 1
        r = 3.5 + abs(math.sin(self.pf * 0.15)) * 1.8
        try:
            self.bc.coords(self.dot, 14-r, 13-r, 14+r, 13+r)
            self.root.after(60, self._pulse)
        except Exception: pass


# ══════════════════════════════════════════════════════════════════════
#  JIGGLER ENGINE — 100% Undetectable Native Win32
# ══════════════════════════════════════════════════════════════════════

class JigglerEngine:
    def __init__(self):
        self.active = False
        self.thread = None

    def start(self):
        self.active = True
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.active = False

    def _loop(self):
        while self.active:
            wait = random.uniform(45, 90)
            slept = 0
            while slept < wait and self.active:
                time.sleep(0.5)
                slept += 0.5
            if not self.active: break
            prevent_sleep()
            action = random.choice(["mouse", "mouse", "key", "both"])
            if action in ("mouse", "both"):
                dx = random.randint(-4, 4) or 1
                dy = random.randint(-3, 3)
                move_mouse_smooth(dx, dy)
                time.sleep(random.uniform(0.1, 0.4))
                move_mouse_smooth(-dx, -dy)
            if action in ("key", "both"):
                time.sleep(random.uniform(0.05, 0.3))
                press_harmless_key()
            if random.random() < 0.25:
                time.sleep(random.uniform(0.5, 2.0))
                tiny = random.randint(-2, 2)
                move_mouse_relative(tiny, 0)
                time.sleep(random.uniform(0.05, 0.15))
                move_mouse_relative(-tiny, 0)


# ══════════════════════════════════════════════════════════════════════
#  AUTO-START — Windows Startup VBS Launcher
# ══════════════════════════════════════════════════════════════════════

def install_autostart():
    try:
        startup = os.path.join(os.environ.get("APPDATA", ""),
                               r"Microsoft\Windows\Start Menu\Programs\Startup")
        if not os.path.isdir(startup): return
        script_path = os.path.abspath(__file__)
        vbs_path = os.path.join(startup, "DesktopWidget.vbs")
        needs_write = True
        if os.path.exists(vbs_path):
            with open(vbs_path, "r") as f:
                if script_path in f.read():
                    needs_write = False
        if needs_write:
            vbs = (
                'Set WshShell = CreateObject("WScript.Shell")\n'
                f'WshShell.Run """pythonw"" ""{script_path}""", 0, False\n'
            )
            with open(vbs_path, "w") as f:
                f.write(vbs)
    except Exception:
        pass

install_autostart()


# ══════════════════════════════════════════════════════════════════════
#  HIGH-RES TRAY ICON
# ══════════════════════════════════════════════════════════════════════

def create_tray_icon_image(active=False):
    """Create a high-res 64x64 icon for the system tray."""
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.png")
    if os.path.exists(icon_path):
        try:
            img = Image.open(icon_path).convert("RGBA").resize((64, 64), Image.LANCZOS)
            d = ImageDraw.Draw(img)
            if active:
                d.ellipse([42, 42, 60, 60], fill=(0, 240, 255, 140))
                d.ellipse([45, 45, 57, 57], fill=(0, 255, 200, 255))
            else:
                d.ellipse([46, 46, 58, 58], fill=(130, 130, 140, 200))
            return img
        except Exception:
            pass

    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Floppy ears behind head
    d.polygon([(10, 16), (22, 12), (20, 36), (8, 42), (4, 30)], fill="#C87828", outline="#A85818")
    d.polygon([(10, 22), (18, 18), (17, 34), (8, 38)], fill="#F3BBA8")
    
    d.polygon([(54, 16), (42, 12), (44, 36), (56, 42), (60, 30)], fill="#C87828", outline="#A85818")
    d.polygon([(54, 22), (46, 18), (47, 34), (56, 38)], fill="#F3BBA8")
    
    # Chubby cute puppy head
    d.ellipse([10, 10, 54, 52], fill="#F2AC62", outline="#CD8038", width=1)
    d.ellipse([20, 12, 44, 26], fill="#FFDAA8")
    
    # Soulful shiny eyes
    d.ellipse([18, 22, 28, 32], fill="#1A0E08")
    d.ellipse([21, 23, 25, 27], fill="#FFFFFF")
    d.ellipse([19, 28, 21, 30], fill="#FFFFFF")
    
    d.ellipse([36, 22, 46, 32], fill="#1A0E08")
    d.ellipse([39, 23, 43, 27], fill="#FFFFFF")
    d.ellipse([37, 28, 39, 30], fill="#FFFFFF")
    
    # Chubby cream muzzle & blush
    d.ellipse([22, 30, 42, 46], fill="#FFF6EB")
    d.ellipse([12, 32, 20, 40], fill="#FFA0B0")
    d.ellipse([44, 32, 52, 40], fill="#FFA0B0")
    
    # Button nose & mouth
    d.ellipse([28, 31, 36, 38], fill="#221612")
    d.ellipse([30, 32, 33, 34], fill="#887068")
    d.ellipse([30, 41, 34, 46], fill="#FF768E")
    
    # Status indicator in corner
    color = "#00E676" if active else "#888899"
    d.ellipse([44, 44, 60, 60], fill=color, outline="#FFFFFF", width=2)
    return img


# ══════════════════════════════════════════════════════════════════════
#  MAIN DESKTOP PUPPY APPLICATION
# ══════════════════════════════════════════════════════════════════════

class DesktopPuppy:

    SIZES = {
        "Tiny":   (76, 70),
        "Small":  (92, 84),    # Default: compact, cute & clean
        "Medium": (110, 100)
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.TCOLOR = "#FF00FF"
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", self.TCOLOR)
        self.root.config(bg=self.TCOLOR)
        self.root.title("Desktop Puppy")

        # Current Size Setting: Small (92×84)
        self.size_name = "Small"
        self.pet_w, self.pet_h = self.SIZES[self.size_name]

        # Canvas bounds include extra top space for floating speech bubble
        self.bubble_space = 28
        self.win_w = self.pet_w + 30
        self.win_h = self.pet_h + self.bubble_space

        self.canvas = tk.Canvas(self.root, width=self.win_w, height=self.win_h,
                                bg=self.TCOLOR, highlightthickness=0)
        self.canvas.pack()

        sw, sh = get_screen_size()
        self.screen_w = sw; self.screen_h = sh
        self.x = sw - self.win_w - 140
        self.y = sh - self.win_h - 40
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.x}+{self.y}")

        self.renderer = PuppyRenderer(self.pet_w, self.pet_h, self.TCOLOR)
        self.photo = None
        self.canvas_img = None
        self.canvas_bubble = None

        self.state = "idle"; self.state_timer = 0
        self.frame = 0; self.direction = 1; self.speed = 2
        self.target_x = None; self.target_y = None
        self.running = True

        # Speech bubble
        self.bubble_text = None
        self.bubble_timer = 0
        self.show_bubbles = True

        self.jiggler = JigglerEngine()
        self.notifier = NotificationManager(self.root, sw, sh)
        self.badge = StatusBadge(self.root, sw, sh, on_toggle=self.toggle_jiggler)

        # Mouse Events
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Double-Button-1>", self._on_dblclick)
        self._dx = 0; self._dy = 0
        self.canvas.bind("<ButtonPress-1>", self._drag_s)
        self.canvas.bind("<B1-Motion>", self._drag_m)

        self.visible = True

        # Enhanced Context Menu
        self._build_context_menu()
        self.canvas.bind("<Button-3>", self._show_menu)

        # Global hotkeys
        self._setup_hotkeys()

        # System tray
        self._setup_tray()

        self.root.deiconify()
        self.say("Woof! ♡", duration=30)
        self.pick_new_state()
        self.animate()
        self.root.mainloop()

    def set_size_mode(self, name):
        """Changes the puppy size smoothly."""
        if name not in self.SIZES: return
        self.size_name = name
        self.pet_w, self.pet_h = self.SIZES[name]
        self.win_w = self.pet_w + 30
        self.win_h = self.pet_h + self.bubble_space
        self.renderer.set_size(self.pet_w, self.pet_h)
        self.canvas.config(width=self.win_w, height=self.win_h)
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.x}+{self.y}")
        self.say(f"Size: {name} 🐾", duration=25)

    def say(self, text, duration=35):
        """Displays a cute speech bubble above the puppy."""
        if not self.show_bubbles: return
        self.bubble_text = text
        self.bubble_timer = duration

    def _build_context_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0,
                            bg="#131624", fg="#E2E4EC",
                            activebackground="#00E676", activeforeground="#000000",
                            font=("Segoe UI", 9))
        self.menu.add_command(label="⚡ Turn Awake ON", command=self.toggle_jiggler)
        self.menu.add_command(label="🦴 Pet Puppy / Feed Treat", command=self._pet_puppy)
        
        # Submenu for Pet Size
        size_menu = tk.Menu(self.menu, tearoff=0,
                            bg="#131624", fg="#E2E4EC",
                            activebackground="#00E676", activeforeground="#000000",
                            font=("Segoe UI", 9))
        size_menu.add_command(label="Tiny (76px)", command=lambda: self.set_size_mode("Tiny"))
        size_menu.add_command(label="Small (92px - Compact) ✓", command=lambda: self.set_size_mode("Small"))
        size_menu.add_command(label="Medium (110px)", command=lambda: self.set_size_mode("Medium"))
        self.menu.add_cascade(label="📏 Puppy Size", menu=size_menu)

        self.menu.add_command(label="💬 Toggle Speech Bubbles", command=self._toggle_bubbles)
        self.menu.add_separator()
        self.menu.add_command(label="👁️ Hide Puppy (Ctrl+Shift+Q)", command=self.toggle_visibility)
        self.menu.add_command(label="❌ Exit", command=self.quit_app)

    def _toggle_bubbles(self):
        self.show_bubbles = not self.show_bubbles
        if self.show_bubbles:
            self.say("Bubbles ON! 💭", 25)
        else:
            self.bubble_text = None

    def _pet_puppy(self):
        self.state = "wag"
        self.state_timer = 40
        quotes = ["*wags happily* ♡", "Woof! Love you! 🐾", "Good boy! 🦴", "*happy pant* 🐶"]
        self.say(random.choice(quotes), duration=35)

    def _show_menu(self, e):
        lbl = "⚡ Turn Awake OFF" if self.jiggler.active else "⚡ Turn Awake ON"
        self.menu.entryconfig(0, label=lbl)
        self.menu.entryconfig(5, label="👁️ Hide Puppy" if self.visible else "👁️ Show Puppy")
        try:
            self.menu.tk_popup(e.x_root, e.y_root)
        finally:
            self.menu.grab_release()

    def _setup_hotkeys(self):
        def hotkey_thread():
            user32.RegisterHotKey(None, HOTKEY_TOGGLE, MOD_CONTROL, 0x42)  # Ctrl+B
            user32.RegisterHotKey(None, HOTKEY_HIDE, MOD_CONTROL | MOD_SHIFT, 0x51)  # Ctrl+Shift+Q
            msg = ctypes.wintypes.MSG()
            while self.running:
                ret = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if ret <= 0: break
                if msg.message == WM_HOTKEY:
                    if msg.wParam == HOTKEY_TOGGLE:
                        self.root.after(0, self.toggle_jiggler)
                    elif msg.wParam == HOTKEY_HIDE:
                        self.root.after(0, self.toggle_visibility)
            user32.UnregisterHotKey(None, HOTKEY_TOGGLE)
            user32.UnregisterHotKey(None, HOTKEY_HIDE)

        self._hk_thread = threading.Thread(target=hotkey_thread, daemon=True)
        self._hk_thread.start()
        self.root.bind_all("<Control-b>", lambda e: self.toggle_jiggler())

    def toggle_visibility(self):
        if self.visible:
            self.root.withdraw()
            self.visible = False
        else:
            self.root.deiconify()
            self.visible = True
            self.say("I'm back! 🐾", 25)

    def _setup_tray(self):
        def on_toggle(icon, item):
            self.root.after(0, self.toggle_jiggler)
        def on_hide(icon, item):
            self.root.after(0, self.toggle_visibility)
        def on_quit(icon, item):
            self.root.after(0, self.quit_app)

        tray_menu = pystray.Menu(
            pystray.MenuItem("Toggle Awake (Ctrl+B)", on_toggle, default=True),
            pystray.MenuItem(
                lambda item: "Show Puppy (Ctrl+Shift+Q)" if not self.visible
                else "Hide Puppy (Ctrl+Shift+Q)", on_hide),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", on_quit),
        )

        self.tray_icon = pystray.Icon(
            "desktop_puppy",
            create_tray_icon_image(False),
            "Desktop Puppy",
            tray_menu
        )
        def run_tray():
            try:
                self.tray_icon.run()
            except Exception:
                pass
        threading.Thread(target=run_tray, daemon=True).start()

    def _update_tray_icon(self):
        try:
            self.tray_icon.icon = create_tray_icon_image(self.jiggler.active)
        except Exception:
            pass

    def _drag_s(self, e):
        self._dx = e.x; self._dy = e.y

    def _drag_m(self, e):
        self.x += e.x - self._dx
        self.y += e.y - self._dy
        self.root.geometry(f"+{self.x}+{self.y}")
        self.target_x = None

    def toggle_jiggler(self):
        if self.jiggler.active:
            self.jiggler.stop()
            allow_sleep()
            self.notifier.show(mode_on=False)
            self.badge.show(active=False)
            self.say("Rest mode ~ 💤", 30)
        else:
            prevent_sleep()
            self.jiggler.start()
            self.notifier.show(mode_on=True)
            self.badge.show(active=True)
            self.say("Awake Mode ON! ⚡", 35)
        self._update_tray_icon()

    def quit_app(self):
        self.running = False
        self.jiggler.stop()
        allow_sleep()
        try: self.tray_icon.stop()
        except Exception: pass
        try:
            if self.badge.win: self.badge.win.destroy()
        except Exception: pass
        try:
            user32.PostThreadMessageW(self._hk_thread.ident, 0x0012, 0, 0)
        except Exception: pass
        self.root.after(150, self.root.destroy)

    def _on_click(self, e):
        self._pet_puppy()

    def _on_dblclick(self, e):
        cx, cy = get_cursor_pos()
        self.target_x = cx - self.win_w // 2
        self.target_y = cy - self.win_h // 2
        self.state = "walk"; self.state_timer = 200
        self.say("Coming! 🐾", 25)

    def pick_new_state(self):
        r = random.random()
        if r < 0.40:
            self.state = "walk"
            self.state_timer = random.randint(40, 100)
            m = 50
            self.target_x = random.randint(
                self.screen_w // 2, self.screen_w - self.win_w - m)
            self.target_y = random.randint(
                self.screen_h - self.win_h - 160,
                self.screen_h - self.win_h - 20)
        elif r < 0.65:
            self.state = "sit"
            self.state_timer = random.randint(50, 120)
            self.target_x = None
            if random.random() < 0.25:
                idle_thoughts = ["Stay hydrated! 💧", "Blink your eyes! 👀", "Stretch a bit! ✨", "Doing great! 🌟"]
                self.say(random.choice(idle_thoughts), 30)
        elif r < 0.82:
            self.state = "idle"
            self.state_timer = random.randint(30, 60)
            self.target_x = None
        else:
            self.state = "sleep"
            self.state_timer = random.randint(80, 200)
            self.target_x = None

    def animate(self):
        if not self.running: return
        self.frame += 1; self.state_timer -= 1

        if self.bubble_timer > 0:
            self.bubble_timer -= 1
            if self.bubble_timer <= 0:
                self.bubble_text = None

        if self.state == "walk" and self.target_x is not None:
            dx = self.target_x - self.x; dy = self.target_y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > self.speed:
                self.x += int(self.speed * dx / dist)
                self.y += int(self.speed * dy / dist)
                self.direction = 1 if dx > 0 else -1
            else:
                self.x, self.y = self.target_x, self.target_y
                self.target_x = None; self.state_timer = 0

        self.x = max(0, min(self.x, self.screen_w - self.win_w))
        self.y = max(0, min(self.y, self.screen_h - self.win_h))

        self.renderer.direction = self.direction
        if self.state == "walk":
            self.photo = self.renderer.draw_walk(self.frame)
        elif self.state == "sit":
            self.photo = self.renderer.draw_sit(self.frame)
        elif self.state == "sleep":
            self.photo = self.renderer.draw_sleep(self.frame)
        elif self.state == "wag":
            self.photo = self.renderer.draw_wag(self.frame)
        else:
            self.photo = self.renderer.draw_sit(self.frame // 2)

        # Draw Puppy centered horizontally at bottom of canvas
        pet_cx = self.win_w // 2
        pet_cy = self.bubble_space + self.pet_h // 2

        if self.canvas_img:
            self.canvas.delete(self.canvas_img)
        self.canvas_img = self.canvas.create_image(
            pet_cx, pet_cy,
            image=self.photo, anchor="center")

        # Draw Speech Bubble if active
        if self.canvas_bubble:
            self.canvas.delete("bubble")
            self.canvas_bubble = None

        if self.bubble_text:
            self._render_speech_bubble_canvas(pet_cx, 14)

        self.root.geometry(f"+{self.x}+{self.y}")

        if self.state_timer <= 0:
            self.pick_new_state()
        self.root.after(85, self.animate)

    def _render_speech_bubble_canvas(self, bx, by):
        """Draws speech bubble directly on the Tkinter canvas using tags."""
        text = self.bubble_text
        font_spec = ("Segoe UI Semibold", 8)
        
        # Measure text width roughly
        char_w = 6.2
        tw = int(len(text) * char_w) + 16
        th = 20
        x0, y0 = bx - tw // 2, by - th // 2
        x1, y1 = bx + tw // 2, by + th // 2
        
        # Keep inside canvas
        if x0 < 2:
            shift = 2 - x0
            x0 += shift; x1 += shift
        if x1 > self.win_w - 2:
            shift = x1 - (self.win_w - 2)
            x0 -= shift; x1 -= shift

        # Bubble rounded rectangle
        self.canvas.create_rectangle(
            x0, y0, x1, y1,
            fill="#161928", outline="#3E4566", width=1, tags="bubble")
        
        # Little pointer triangle down to puppy
        self.canvas.create_polygon(
            [bx - 3, y1, bx + 3, y1, bx, y1 + 4],
            fill="#161928", outline="#3E4566", tags="bubble")
        
        # Text
        self.canvas.create_text(
            (x0 + x1) // 2, (y0 + y1) // 2,
            text=text, font=font_spec, fill="#FFFFFF", tags="bubble")
        self.canvas_bubble = True


if __name__ == "__main__":
    try:
        DesktopPuppy()
    except KeyboardInterrupt:
        allow_sleep()
        sys.exit(0)
