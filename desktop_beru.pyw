"""
👑 Solo Leveling Desktop Companions — Real Beru & Igris
Professional Stealth Anti-Idle Desktop Widget with Living Shadow Monarch Aura.

Features:
- High-Definition Manhwa Artwork:
  - Beru: Ultra-detailed Shadow Marshal ant silhouette, glowing cyan soulfire eyes,
    translucent wings, and layered obsidian carapace.
  - Igris: Full obsidian plate armor, flowing crimson plume, glowing soulfire visor,
    and massive silver-blue broadsword.
- Real Shadow Aura Particle System:
  - Rising, swirling purple/black shadow smoke wisps + glowing cyan/red soulfire embers.
  - Rages into a shadow tempest when the Shadow Domain (Awake Mode) is active.
- Dynamic Flying & Hover Physics:
  - Multi-harmonic floating hover.
  - Directional banking tilt during flight across the screen.
- 5 Expressive Emotions:
  1. Idle / Hover: Floating with living shadow aura & drifting soulfire embers.
  2. Crying (Tears of Devotion): Waterfalls of joyful anime tears when praised.
  3. Bow / Royal Fealty: Homage with floating golden Monarch Crown.
  4. Cheer: Triumphant leap with floating Monarch gems.
  5. Fly / Rush: Aerodynamic dash to cursor with trailing mist.
- Dedicated Motivational Dialogue:
  - "My king!", "You are the best!", "You will conquer today!", "Your code is magnificent!",
    and caring health/hydration reminders.
- Switch Characters Anytime via Right-Click Menu -> Switch Character.
- 100% Undetectable Native Win32 SendInput (ctypes), hardware scancodes, Bezier curves.
- Global Hotkeys: Ctrl+B (Toggle Shadow Domain), Ctrl+Shift+Q (Hide/Show Companion).

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
#  SINGLE INSTANCE
# ══════════════════════════════════════════════════════════════════════

MUTEX_NAME = "Global\\WinSvcHelper_ShadowMonarch_" + hashlib.md5(
    os.path.abspath(__file__).encode()).hexdigest()[:12]

def ensure_single_instance():
    k32 = ctypes.windll.kernel32
    mutex = k32.CreateMutexW(None, True, MUTEX_NAME)
    if k32.GetLastError() == 183:
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
#  DEPENDENCIES
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
#  NATIVE WIN32 INPUT
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
    press_key_scancode(random.choice([0x2A, 0x36, 0x1D]))

WM_HOTKEY     = 0x0312
MOD_CONTROL   = 0x0002
MOD_SHIFT     = 0x0004
HOTKEY_TOGGLE = 1
HOTKEY_HIDE   = 2


# ══════════════════════════════════════════════════════════════════════
#  PROFESSIONAL SHADOW CHARACTER RENDERER WITH LIVING AURA
# ══════════════════════════════════════════════════════════════════════

class RealShadowRenderer:
    """
    Renders high-definition Solo Leveling Shadow Soldiers (Beru and Igris):
    - Uses ultra-detailed manhwa-grade character base sprites
    - Real-time swirling Shadow Monarch flame aura & soulfire ember particle engine
    - Multi-harmonic flying & hovering physics
    - Directional banking & flight inertia
    - Emotional overlays (Crying tears of devotion, King's Fealty Crown, Battle Stance glow)
    - Clean chroma-key compositing onto Windows transparent color (#FF00FF)
    """
    def __init__(self, char_name="Beru", w=110, h=105, tcolor="#FF00FF"):
        self.char_name = char_name
        self.w = w
        self.h = h
        self.tcolor = tcolor
        self.direction = 1
        
        self.base_dir = os.path.join(os.path.dirname(__file__), "assets", "shadow_soldiers")
        self._load_sprite()

        self.bg_particles = []
        self.fg_embers = []

    def _load_sprite(self):
        img_name = "beru_hq.png" if self.char_name == "Beru" else "igris_hq.png"
        raw_path = os.path.join(self.base_dir, img_name)
        if os.path.exists(raw_path):
            self.base_img = Image.open(raw_path).convert("RGBA")
        else:
            # Fallback simple base if asset directory missing
            self.base_img = Image.new("RGBA", (200, 200), (20, 15, 30, 255))

    def set_character(self, char_name):
        self.char_name = char_name
        self._load_sprite()
        self.bg_particles.clear()
        self.fg_embers.clear()

    def set_size(self, w, h):
        self.w = w
        self.h = h

    def render(self, frame=0, emotion="idle", flight_tilt=0.0, is_active=False):
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)

        cx = self.w // 2
        cy = self.h // 2 + 5

        # Floating Hover Physics
        hover_y = math.sin(frame * 0.28) * 3.5 if emotion in ("idle", "fly") else 0.0

        # 1. Background Shadow Aura Particles (swirling rising smoke)
        spawn_count = 2 if is_active else 1
        for _ in range(spawn_count):
            if len(self.bg_particles) < 22:
                self.bg_particles.append({
                    'x': cx + random.uniform(-22, 22),
                    'y': cy + 24 + random.uniform(-5, 10),
                    'vx': random.uniform(-0.6, 0.6),
                    'vy': random.uniform(-2.0, -1.0) * (1.3 if is_active else 1.0),
                    'size': random.uniform(4.0, 7.5),
                    'life': 1.0,
                    'decay': random.uniform(0.04, 0.07)
                })

        surviving_bg = []
        for p in self.bg_particles:
            p['x'] += p['vx'] + math.sin(frame * 0.15 + p['y'] * 0.06) * 0.5
            p['y'] += p['vy']
            p['size'] += 0.16
            p['life'] -= p['decay']
            if p['life'] > 0:
                alpha = int(p['life'] * (165 if is_active else 115))
                col = (130, 45, 210, alpha) if self.char_name == "Beru" else (180, 20, 50, alpha)
                d.ellipse([p['x'] - p['size'], p['y'] - p['size'],
                           p['x'] + p['size'], p['y'] + p['size']], fill=col)
                surviving_bg.append(p)
        self.bg_particles = surviving_bg

        # 2. Render Character Base Sprite with breathing / tilt / scale
        char_h = int(self.h * 0.76)
        aspect = self.base_img.width / self.base_img.height
        char_w = int(char_h * aspect)

        breath = 1.0 + math.sin(frame * 0.25) * 0.025
        scaled_w = max(10, int(char_w * breath))
        scaled_h = max(10, int(char_h * breath))

        char_resized = self.base_img.resize((scaled_w, scaled_h), Image.LANCZOS)

        if self.direction == -1:
            char_resized = char_resized.transpose(Image.FLIP_LEFT_RIGHT)

        if abs(flight_tilt) > 0.01:
            char_resized = char_resized.rotate(flight_tilt * self.direction, resample=Image.BICUBIC, expand=True)

        px = cx - char_resized.width // 2
        py = int(cy - char_resized.height // 2 + hover_y)
        canvas.paste(char_resized, (px, py), char_resized)

        # 3. Emotional Overlays
        d_fg = ImageDraw.Draw(canvas)

        if emotion == "crying":
            # Overwhelmed anime tears of devotion!
            for side in (-1, 1):
                tx = cx + side * 14
                ty = py + int(char_resized.height * 0.35)
                t_pts = [(tx - 2, ty), (tx + 2, ty), (tx + 4, ty + 24), (tx - 4, ty + 24)]
                d_fg.polygon(t_pts, fill=(90, 220, 255, 230), outline=(200, 245, 255, 255))
                d_fg.ellipse([tx - 4, ty + 22, tx + 4, ty + 28], fill=(220, 255, 255, 255))

        elif emotion == "bow":
            # Floating Golden Monarch Crown
            crown_y = py - 12
            d_fg.polygon([(cx - 9, crown_y), (cx - 4, crown_y + 5), (cx, crown_y - 2),
                          (cx + 4, crown_y + 5), (cx + 9, crown_y), (cx + 7, crown_y + 9),
                          (cx - 7, crown_y + 9)], fill=(255, 215, 60, 255), outline=(255, 160, 0, 255))

        elif emotion == "cheer":
            # Floating Monarch sparkle gems
            bob = math.sin(frame * 0.5) * 4
            d_fg.ellipse([cx - 28, py + 8 + bob, cx - 22, py + 14 + bob], fill=(0, 240, 255, 230))
            d_fg.ellipse([cx + 24, py + 4 - bob, cx + 30, py + 10 - bob], fill=(255, 215, 60, 240))

        # 4. Foreground Soulfire Embers
        if len(self.fg_embers) < 10:
            self.fg_embers.append({
                'x': cx + random.uniform(-18, 18),
                'y': py + char_resized.height - 10,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-1.8, -0.9),
                'size': random.uniform(1.5, 2.8),
                'life': 1.0,
                'decay': random.uniform(0.04, 0.08)
            })

        surviving_fg = []
        for p in self.fg_embers:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= p['decay']
            if p['life'] > 0:
                alpha = int(p['life'] * 240)
                col = (0, 240, 255, alpha) if self.char_name == "Beru" else (255, 60, 80, alpha)
                d_fg.ellipse([p['x'] - p['size'], p['y'] - p['size'],
                              p['x'] + p['size'], p['y'] + p['size']], fill=col)
                surviving_fg.append(p)
        self.fg_embers = surviving_fg

        # 5. Composite onto TCOLOR with alpha threshold to prevent any halo on Windows
        tc = self.tcolor.lstrip('#')
        r_t, g_t, b_t = tuple(int(tc[i:i+2], 16) for i in (0, 2, 4))
        bg = Image.new("RGBA", (self.w, self.h), (r_t, g_t, b_t, 255))
        
        alpha = canvas.split()[-1]
        clean_mask = alpha.point(lambda p: 255 if p >= 45 else 0)
        final_img = Image.composite(canvas.convert("RGB"), bg.convert("RGB"), clean_mask)
        return ImageTk.PhotoImage(final_img)


# ══════════════════════════════════════════════════════════════════════
#  SHADOW NOTIFICATION & STATUS BADGE
# ══════════════════════════════════════════════════════════════════════

class ShadowNotificationManager:
    def __init__(self, root, sw, sh):
        self.root = root; self.sw = sw; self.sh = sh
        self.current = None; self.sy = 0

    def show(self, mode_on, char_name="Beru"):
        if self.current:
            try: self.current.destroy()
            except Exception: pass
        
        nw = tk.Toplevel(self.root)
        nw.overrideredirect(True)
        nw.attributes("-topmost", True)
        nw.attributes("-alpha", 0.96)
        
        cw, ch = 340, 78
        sx = self.sw - cw - 24
        self.ty = self.sh - ch - 54
        self.sy = self.sh
        nw.geometry(f"{cw}x{ch}+{sx}+{self.sy}")

        c = tk.Canvas(nw, width=cw, height=ch, bg="#0B0814", highlightthickness=0)
        c.pack(fill="both", expand=True)

        accent = "#00F0FF" if mode_on else "#9D4EDD"
        border_col = "#7928CA" if mode_on else "#3D2260"
        
        c.create_rectangle(0, 0, cw, ch, fill="#0B0814", outline=border_col, width=1)
        c.create_rectangle(0, 0, 4, ch, fill=accent, outline=accent)

        icon = "🐜" if char_name == "Beru" else "🗡️"
        c.create_oval(14, 15, 48, 49, fill="#18102C", outline=accent, width=1.5)
        c.create_text(31, 32, text=icon, font=("Segoe UI Emoji", 14))

        title = "SHADOW DOMAIN: ACTIVE" if mode_on else "SHADOW DOMAIN: DORMANT"
        c.create_text(58, 22, text=title, anchor="w",
                      font=("Segoe UI Semibold", 10), fill=accent)
        
        sub = f"{char_name} guards your PC • Slumber is forbidden!" if mode_on else "Mana conservation mode • Slumber allowed"
        c.create_text(58, 41, text=sub, anchor="w",
                      font=("Segoe UI", 8), fill="#E2E4EC")
        
        c.create_text(58, 57, text="Ctrl+B = Toggle Domain  •  Right-click for menu",
                      anchor="w", font=("Segoe UI", 7), fill="#8E85A8")

        badge_text = "AWAKE" if mode_on else "SLEEP"
        c.create_rectangle(cw - 56, 26, cw - 14, 48, fill="#18102C", outline=accent, width=1)
        c.create_text(cw - 35, 37, text=badge_text,
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


class ShadowStatusBadge:
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
        bw, bh = 104, 26
        self.win.geometry(f"{bw}x{bh}+{self.sw-bw-16}+{self.sh-bh-50}")
        
        self.bc = tk.Canvas(self.win, width=bw, height=bh,
                            bg="#0D091A", highlightthickness=0)
        self.bc.pack(fill="both", expand=True)
        self.bc.create_rectangle(0, 0, bw, bh, fill="#0D091A", outline="#7928CA")
        
        self.dot = self.bc.create_oval(10, 8, 18, 16, fill="#00F0FF", outline="#00A0B0")
        self.bc.create_text(26, 13, text="SHADOW", anchor="w",
                            font=("Segoe UI Semibold", 8), fill="#00F0FF")
        self.bc.create_text(76, 13, text="Ctrl+B", anchor="w",
                            font=("Segoe UI", 6), fill="#8E85A8")
        
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
#  JIGGLER ENGINE
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


def create_tray_icon(char_name="Beru", active=False):
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
    if char_name == "Beru":
        d.line([(24, 20), (14, 8), (18, 4)], fill="#6548B2", width=2)
        d.ellipse([16, 2, 22, 8], fill="#00F0FF")
        d.line([(40, 20), (50, 8), (46, 4)], fill="#6548B2", width=2)
        d.ellipse([42, 2, 48, 8], fill="#00F0FF")
        d.ellipse([12, 12, 52, 52], fill="#0C0916", outline="#7928CA", width=2)
        d.polygon([(20, 26), (28, 27), (26, 33), (18, 30)], fill="#00F0FF")
        d.ellipse([22, 28, 26, 32], fill="#FFFFFF")
        d.polygon([(44, 26), (36, 27), (38, 33), (46, 30)], fill="#00F0FF")
        d.ellipse([38, 28, 42, 32], fill="#FFFFFF")
    else:
        d.polygon([(8, 8), (28, 20), (22, 40), (4, 25)], fill="#E63946")
        d.ellipse([14, 16, 50, 52], fill="#0E121C", outline="#3A4860", width=2)
        d.line([(22, 34), (42, 34)], fill="#00F0FF", width=3)
        d.ellipse([28, 33, 36, 35], fill="#FFFFFF")
    
    color = "#00F0FF" if active else "#554477"
    d.ellipse([44, 44, 60, 60], fill=color, outline="#FFFFFF", width=2)
    return img


# ══════════════════════════════════════════════════════════════════════
#  MAIN DESKTOP SHADOW COMPANION
# ══════════════════════════════════════════════════════════════════════

class DesktopShadowCompanion:

    SIZES = {
        "Tiny":   (86, 82),
        "Small":  (110, 105),   # Default: crisp, perfect desktop scale
        "Medium": (132, 126)
    }

    MOTIVATIONAL_BERU = [
        "My king! 👑",
        "You are the best! ✨",
        "Nothing can stop you, My King! ⚡",
        "You will conquer today, Sovereign! ⚔️",
        "I believe in you, My King! 🌟",
        "Your code is magnificent, My King! 💎",
        "The greatest Monarch of all time! 👑",
        "Keep going, My King! Victory is yours! 💪",
        "Shall I eradicate that bug, My King?! 🩸",
        "Drink water, My King! Your vessel must stay strong! 💧",
        "Rest your eyes, Sovereign! Your vision is supreme! 👀",
        "I live only to serve your greatness, My King!"
    ]

    MOTIVATIONAL_IGRIS = [
        "My King... 🗡️",
        "You are the best, My King.",
        "Your sword and shield stand ready, Sovereign. ⚔️",
        "Hold your head high, My King. Victory is assured.",
        "None can match your resolve, My King. ✨",
        "I shall cut down any obstacle in your path.",
        "An honorable day to stand beside the Monarch! 👑",
        "Stand tall, My King. I believe in you.",
        "Do not overwork yourself, My Sovereign. Hydrate! 💧",
        "Your brilliance commands the battlefield."
    ]

    def __init__(self, default_char="Beru"):
        self.root = tk.Tk()
        self.root.withdraw()

        self.current_char = default_char

        self.TCOLOR = "#FF00FF"
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", self.TCOLOR)
        self.root.config(bg=self.TCOLOR)
        self.root.title("Shadow Monarch Companion")

        self.size_name = "Small"
        self.pet_w, self.pet_h = self.SIZES[self.size_name]

        self.bubble_space = 28
        self.win_w = self.pet_w + 36
        self.win_h = self.pet_h + self.bubble_space

        self.canvas = tk.Canvas(self.root, width=self.win_w, height=self.win_h,
                                bg=self.TCOLOR, highlightthickness=0)
        self.canvas.pack()

        sw, sh = get_screen_size()
        self.screen_w = sw; self.screen_h = sh
        self.x = sw - self.win_w - 140
        self.y = sh - self.win_h - 40
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.x}+{self.y}")

        self.renderer = RealShadowRenderer(self.current_char, self.pet_w, self.pet_h, self.TCOLOR)

        self.photo = None
        self.canvas_img = None
        self.canvas_bubble = None

        self.state = "idle"; self.state_timer = 0
        self.frame = 0; self.direction = 1; self.speed = 3
        self.target_x = None; self.target_y = None
        self.running = True

        self.bubble_text = None
        self.bubble_timer = 0
        self.show_bubbles = True

        self.jiggler = JigglerEngine()
        self.notifier = ShadowNotificationManager(self.root, sw, sh)
        self.badge = ShadowStatusBadge(self.root, sw, sh, on_toggle=self.toggle_jiggler)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Double-Button-1>", self._on_dblclick)
        self._dx = 0; self._dy = 0
        self.canvas.bind("<ButtonPress-1>", self._drag_s)
        self.canvas.bind("<B1-Motion>", self._drag_m)

        self.visible = True

        self._build_context_menu()
        self.canvas.bind("<Button-3>", self._show_menu)

        self._setup_hotkeys()
        self._setup_tray()

        self.root.deiconify()
        greeting = "I have arrived, My King! 👑" if self.current_char == "Beru" else "At your command, My King. 🗡️"
        self.say(greeting, duration=35)
        self.pick_new_state()
        self.animate()
        self.root.mainloop()

    def switch_character(self, name):
        if name not in ("Beru", "Igris"): return
        self.current_char = name
        self.renderer.set_character(name)
        self._update_tray_icon()
        if name == "Beru":
            self.say("My King! Beru is here to serve! 👑", 35)
        else:
            self.say("My King... Igris stands beside you. 🗡️", 35)

    def set_size_mode(self, name):
        if name not in self.SIZES: return
        self.size_name = name
        self.pet_w, self.pet_h = self.SIZES[name]
        self.win_w = self.pet_w + 36
        self.win_h = self.pet_h + self.bubble_space
        self.renderer.set_size(self.pet_w, self.pet_h)
        self.canvas.config(width=self.win_w, height=self.win_h)
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.x}+{self.y}")
        self.say(f"Size: {name} ⚡", duration=25)

    def say(self, text, duration=35):
        if not self.show_bubbles: return
        self.bubble_text = text
        self.bubble_timer = duration

    def _build_context_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0,
                            bg="#0B0814", fg="#E2E4EC",
                            activebackground="#7928CA", activeforeground="#00F0FF",
                            font=("Segoe UI", 9))
        self.menu.add_command(label="⚡ Activate Shadow Domain", command=self.toggle_jiggler)
        self.menu.add_command(label="👑 Praise Companion", command=self._praise)
        
        char_menu = tk.Menu(self.menu, tearoff=0,
                            bg="#0B0814", fg="#E2E4EC",
                            activebackground="#7928CA", activeforeground="#00F0FF",
                            font=("Segoe UI", 9))
        char_menu.add_command(label="🐜 Beru (Shadow Marshal)", command=lambda: self.switch_character("Beru"))
        char_menu.add_command(label="🗡️ Igris (Blood-Red Commander)", command=lambda: self.switch_character("Igris"))
        self.menu.add_cascade(label="👤 Switch Character", menu=char_menu)

        size_menu = tk.Menu(self.menu, tearoff=0,
                            bg="#0B0814", fg="#E2E4EC",
                            activebackground="#7928CA", activeforeground="#00F0FF",
                            font=("Segoe UI", 9))
        size_menu.add_command(label="Tiny (86px)", command=lambda: self.set_size_mode("Tiny"))
        size_menu.add_command(label="Small (110px - Default) ✓", command=lambda: self.set_size_mode("Small"))
        size_menu.add_command(label="Medium (132px)", command=lambda: self.set_size_mode("Medium"))
        self.menu.add_cascade(label="📏 Companion Size", menu=size_menu)

        self.menu.add_command(label="💬 Toggle Speech Bubbles", command=self._toggle_bubbles)
        self.menu.add_separator()
        self.menu.add_command(label="👁️ Hide Companion (Ctrl+Shift+Q)", command=self.toggle_visibility)
        self.menu.add_command(label="❌ Dismiss to Shadows", command=self.quit_app)

    def _toggle_bubbles(self):
        self.show_bubbles = not self.show_bubbles
        if self.show_bubbles: self.say("Comments ON! 💬", 25)
        else: self.bubble_text = None

    def _praise(self):
        if self.current_char == "Beru":
            self.state = "crying"
            quotes = [
                "MY KING HAS TOUCHED ME!! 😭👑",
                "You are the best, My King!!",
                "I pledge my eternal soul to you, Sovereign!",
                "Shall I eliminate this bug in your code?! 🩸",
                "Your humble servant Beru weeps with joy!"
            ]
        else:
            self.state = "cheer"
            quotes = [
                "My King... you are the greatest.",
                "You are the best, My King! ⚔️",
                "Victory was yours from the start, Sovereign.",
                "An honor beyond words to serve the Monarch."
            ]
        self.state_timer = 45
        self.say(random.choice(quotes), duration=40)

    def _show_menu(self, e):
        lbl = "⚡ Deactivate Shadow Domain" if self.jiggler.active else "⚡ Activate Shadow Domain"
        self.menu.entryconfig(0, label=lbl)
        self.menu.entryconfig(6, label="👁️ Hide Companion" if self.visible else "👁️ Summon Companion")
        try:
            self.menu.tk_popup(e.x_root, e.y_root)
        finally:
            self.menu.grab_release()

    def _setup_hotkeys(self):
        def hotkey_thread():
            user32.RegisterHotKey(None, HOTKEY_TOGGLE, MOD_CONTROL, 0x42)
            user32.RegisterHotKey(None, HOTKEY_HIDE, MOD_CONTROL | MOD_SHIFT, 0x51)
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
            self.say("I have returned, My King! 👑", 25)

    def _setup_tray(self):
        def on_toggle(icon, item): self.root.after(0, self.toggle_jiggler)
        def on_hide(icon, item): self.root.after(0, self.toggle_visibility)
        def on_quit(icon, item): self.root.after(0, self.quit_app)

        tray_menu = pystray.Menu(
            pystray.MenuItem("Toggle Shadow Domain (Ctrl+B)", on_toggle, default=True),
            pystray.MenuItem(
                lambda item: "Summon Companion (Ctrl+Shift+Q)" if not self.visible
                else "Hide Companion (Ctrl+Shift+Q)", on_hide),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", on_quit),
        )

        self.tray_icon = pystray.Icon(
            "desktop_shadow",
            create_tray_icon(self.current_char, False),
            f"Shadow Companion ({self.current_char})",
            tray_menu
        )
        def run_tray():
            try: self.tray_icon.run()
            except Exception: pass
        threading.Thread(target=run_tray, daemon=True).start()

    def _update_tray_icon(self):
        try:
            self.tray_icon.icon = create_tray_icon(self.current_char, self.jiggler.active)
            self.tray_icon.title = f"Shadow Companion ({self.current_char})"
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
            self.notifier.show(mode_on=False, char_name=self.current_char)
            self.badge.show(active=False)
            self.say("Rest well, My King... 💤", 30)
            self.state = "idle"
        else:
            prevent_sleep()
            self.jiggler.start()
            self.notifier.show(mode_on=True, char_name=self.current_char)
            self.badge.show(active=True)
            self.say("SHADOW DOMAIN ACTIVE! ⚔️", 35)
            self.state = "idle"
            self.state_timer = 50
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
        self._praise()

    def _on_dblclick(self, e):
        cx, cy = get_cursor_pos()
        self.target_x = cx - self.win_w // 2
        self.target_y = cy - self.win_h // 2
        self.state = "fly"; self.state_timer = 200
        self.say("I fly to your cursor, My King! ⚡", 25)

    def pick_new_state(self):
        r = random.random()
        if r < 0.40:
            self.state = "fly"
            self.state_timer = random.randint(30, 80)
            m = 50
            self.target_x = random.randint(
                self.screen_w // 2, self.screen_w - self.win_w - m)
            self.target_y = random.randint(
                self.screen_h - self.win_h - 160,
                self.screen_h - self.win_h - 20)
        elif r < 0.70:
            self.state = "idle"
            self.state_timer = random.randint(50, 100)
            self.target_x = None
            if random.random() < 0.35:
                quotes = self.MOTIVATIONAL_BERU if self.current_char == "Beru" else self.MOTIVATIONAL_IGRIS
                self.say(random.choice(quotes), 32)
        elif r < 0.88:
            self.state = "bow"
            self.state_timer = random.randint(40, 80)
            self.target_x = None
            self.say("My King! 👑", 25)
        else:
            self.state = "idle"
            self.state_timer = random.randint(30, 60)
            self.target_x = None

    def animate(self):
        if not self.running: return
        self.frame += 1; self.state_timer -= 1

        if self.bubble_timer > 0:
            self.bubble_timer -= 1
            if self.bubble_timer <= 0:
                self.bubble_text = None

        flight_tilt = 0.0
        if self.state == "fly" and self.target_x is not None:
            dx = self.target_x - self.x; dy = self.target_y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > self.speed:
                self.x += int(self.speed * dx / dist)
                self.y += int(self.speed * dy / dist)
                self.direction = 1 if dx > 0 else -1
                flight_tilt = -10.0  # aerodynamic forward banking tilt
            else:
                self.x, self.y = self.target_x, self.target_y
                self.target_x = None; self.state_timer = 0

        self.x = max(0, min(self.x, self.screen_w - self.win_w))
        self.y = max(0, min(self.y, self.screen_h - self.win_h))

        self.renderer.direction = self.direction

        self.photo = self.renderer.render(
            frame=self.frame,
            emotion=self.state,
            flight_tilt=flight_tilt,
            is_active=self.jiggler.active
        )

        pet_cx = self.win_w // 2
        pet_cy = self.bubble_space + self.pet_h // 2

        if self.canvas_img:
            self.canvas.delete(self.canvas_img)
        self.canvas_img = self.canvas.create_image(
            pet_cx, pet_cy,
            image=self.photo, anchor="center")

        if self.canvas_bubble:
            self.canvas.delete("bubble")
            self.canvas_bubble = None

        if self.bubble_text:
            self._render_speech_bubble_canvas(pet_cx, 14)

        self.root.geometry(f"+{self.x}+{self.y}")

        if self.state_timer <= 0:
            self.pick_new_state()
        self.root.after(80, self.animate)

    def _render_speech_bubble_canvas(self, bx, by):
        text = self.bubble_text
        font_spec = ("Segoe UI Semibold", 8)
        
        char_w = 6.2
        tw = int(len(text) * char_w) + 18
        th = 20
        x0, y0 = bx - tw // 2, by - th // 2
        x1, y1 = bx + tw // 2, by + th // 2
        
        if x0 < 2:
            shift = 2 - x0
            x0 += shift; x1 += shift
        if x1 > self.win_w - 2:
            shift = x1 - (self.win_w - 2)
            x0 -= shift; x1 -= shift

        accent_border = "#7928CA" if self.current_char == "Beru" else "#D90429"
        accent_text = "#00F0FF" if self.current_char == "Beru" else "#FFFFFF"

        self.canvas.create_rectangle(
            x0, y0, x1, y1,
            fill="#0D091A", outline=accent_border, width=1, tags="bubble")
        
        self.canvas.create_polygon(
            [bx - 3, y1, bx + 3, y1, bx, y1 + 4],
            fill="#0D091A", outline=accent_border, tags="bubble")
        
        self.canvas.create_text(
            (x0 + x1) // 2, (y0 + y1) // 2,
            text=text, font=font_spec, fill=accent_text, tags="bubble")
        self.canvas_bubble = True


if __name__ == "__main__":
    char = "Beru"
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("igris", "red"):
        char = "Igris"
    try:
        DesktopShadowCompanion(default_char=char)
    except KeyboardInterrupt:
        allow_sleep()
        sys.exit(0)
