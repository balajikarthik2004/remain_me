"""
👑🐾 Solo Leveling & Desktop Companion Suite — Windows 10 Professional Edition
Unified Flagship Desktop Companion featuring:
- 🐜 Shadow Marshal Beru (Dynamic flight, cyan soulfire, tears of devotion, royal praise)
- 🗡️ Blood-Red Commander Igris (Marching stride, crimson soulfire, knightly fealty)
- 🐱 Cute Calico Cat (Pointy ears, twitching whiskers, emerald eyes, purring, bat paws)
- 🕷️ The Amazing Spider-Man (Web throwing thwip!, web swinging, wall crawling on screen edges)
- 🐶 Cute Golden Puppy (4x AA procedural renderer, wagging tail, floppy ears, sweet woofs)
- 🪟 Windows 10 Light Mode Context Menu (Snug submenu alignment, 1px border, hover highlight, checkmarks)
- ⏰ Configurable Reminder System (15m, 30m, 45m, 60m intervals for Water, Posture, Eye Relief, Walk, Coffee)
- 💬 Full-Display Speech Bubbles (Dynamic bounding box, multi-line auto-wrap, zero word clipping)
- 👤 Professional System Tray Menu (Grouped Character submenu, Reminders submenu, live status)
- 🛡️ Enterprise-Grade Stealth Anti-Idle Engine (SendInput, hardware scancodes, Bezier curves)
- ⌨️ Global Hotkeys: Ctrl+B (Awake Mode / Shadow Domain), Ctrl+Shift+Q (Hide / Show)
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
import json
import hashlib
import argparse

# ══════════════════════════════════════════════════════════════════════
#  SINGLE INSTANCE MUTEX
# ══════════════════════════════════════════════════════════════════════

MUTEX_NAME = "Global\\WinSvcHelper_DesktopCompanionMaster_" + hashlib.md5(
    os.path.abspath(__file__).encode()).hexdigest()[:12]

def ensure_single_instance():
    k32 = ctypes.windll.kernel32
    mutex = k32.CreateMutexW(None, True, MUTEX_NAME)
    if k32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        try:
            import subprocess
            subprocess.Popen('taskkill /F /IM pythonw.exe 2>nul',
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1.2)
            k32.CloseHandle(mutex)
            mutex = k32.CreateMutexW(None, True, MUTEX_NAME)
        except Exception:
            pass
    return mutex

INSTANCE_MUTEX = ensure_single_instance()

# ══════════════════════════════════════════════════════════════════════
#  DEPENDENCY RESOLUTION
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

try:
    from desktop_puppy import PuppyRenderer
except Exception:
    PuppyRenderer = None

# ══════════════════════════════════════════════════════════════════════
#  NATIVE WIN32 HARDWARE INPUT & STEALTH ANTI-IDLE
# ══════════════════════════════════════════════════════════════════════

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

ES_CONTINUOUS       = 0x80000000
ES_SYSTEM_REQUIRED  = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def prevent_sleep():
    kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)

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
    _fields_ = [("type", ctypes.c_ulong), ("u", INPUT_UNION)]

def send_hardware_key(scancode=0x8E):  # VK_F15 extended dummy key
    inp_down = INPUT()
    inp_down.type = INPUT_KEYBOARD
    inp_down.u.ki.wScan = scancode
    inp_down.u.ki.dwFlags = KEYEVENTF_SCANCODE

    inp_up = INPUT()
    inp_up.type = INPUT_KEYBOARD
    inp_up.u.ki.wScan = scancode
    inp_up.u.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP

    arr = (INPUT * 2)(inp_down, inp_up)
    user32.SendInput(2, arr, ctypes.sizeof(INPUT))

def send_relative_mouse(dx, dy):
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.u.mi.dx = int(dx)
    inp.u.mi.dy = int(dy)
    inp.u.mi.dwFlags = MOUSEEVENTF_MOVE
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

def human_bezier_motion(total_dx, total_dy, steps=18):
    if steps < 4:
        send_relative_mouse(total_dx, total_dy)
        return
    p0 = (0.0, 0.0)
    p3 = (float(total_dx), float(total_dy))
    jitter_scale = max(6.0, (total_dx**2 + total_dy**2)**0.25 * 1.5)
    p1 = (p3[0] * 0.35 + random.uniform(-jitter_scale, jitter_scale),
          p3[1] * 0.20 + random.uniform(-jitter_scale, jitter_scale))
    p2 = (p3[0] * 0.65 + random.uniform(-jitter_scale, jitter_scale),
          p3[1] * 0.80 + random.uniform(-jitter_scale, jitter_scale))

    last_x, last_y = 0.0, 0.0
    for i in range(1, steps + 1):
        t = i / steps
        u = 1.0 - t
        tt = t * t
        uu = u * u
        cur_x = uu * u * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + tt * t * p3[0]
        cur_y = uu * u * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + tt * t * p3[1]
        cur_x += random.uniform(-0.6, 0.6)
        cur_y += random.uniform(-0.6, 0.6)
        dx = int(round(cur_x - last_x))
        dy = int(round(cur_y - last_y))
        if dx != 0 or dy != 0:
            send_relative_mouse(dx, dy)
        last_x += dx
        last_y += dy
        time.sleep(random.uniform(0.007, 0.016))

# ══════════════════════════════════════════════════════════════════════
#  WINDOWS 10 LIGHT MODE CONTEXT MENU (SNUG SUBMENU POSITIONING)
# ══════════════════════════════════════════════════════════════════════

class Win10LightContextMenu:
    """
    Authentic Windows 10 Light Mode Context Menu.
    - Crisp surface (#FCFCFC / #F3F3F3) with 1px border (#C8C8C8)
    - Classic Windows 10 hover selection highlight (#E5E5E5)
    - High-contrast typography (Segoe UI, #111111)
    - Windows Blue accent (#0078D7) for checkmarks and headers
    - Pixel-perfect submenu positioning immediately adjacent to hovered row (no jumping!)
    - Auto-dismiss on click-outside or Escape
    """
    BG_COLOR        = "#FCFCFC"
    BORDER_COLOR    = "#C8C8C8"
    HOVER_BG        = "#E5E5E5"
    TEXT_COLOR      = "#111111"
    TEXT_MUTED      = "#555555"
    ACCENT_BLUE     = "#0078D7"
    SEPARATOR_COLOR = "#E2E2E2"

    def __init__(self, master, items, is_submenu=False, parent_menu=None):
        self.master = master
        self.items = items
        self.is_submenu = is_submenu
        self.parent_menu = parent_menu
        self.active_submenu = None
        self.active_submenu_item = None

        self.win = tk.Toplevel(master)
        self.win.withdraw()
        self.win.wm_overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=self.BORDER_COLOR)

        self.container = tk.Frame(self.win, bg=self.BG_COLOR, padx=2, pady=3)
        self.container.pack(fill="both", expand=True, padx=1, pady=1)

        self._build_items()

        if not is_submenu:
            self.win.bind("<Escape>", lambda e: self.dismiss_all())
            self.master.bind("<Button-1>", self._on_master_click, add="+")
            self.win.bind("<FocusOut>", self._on_focus_out)

    def _build_items(self):
        for item in self.items:
            itype = item.get("type")
            if itype == "separator":
                sep = tk.Frame(self.container, bg=self.SEPARATOR_COLOR, height=1)
                sep.pack(fill="x", padx=6, pady=3)
                continue

            if itype == "header":
                hdr_frame = tk.Frame(self.container, bg="#F0F0F0", padx=6, pady=4)
                hdr_frame.pack(fill="x", pady=(0, 2))
                
                # App icon thumbnail if provided
                icon_img = item.get("icon_img")
                if icon_img:
                    icon_lbl = tk.Label(hdr_frame, image=icon_img, bg="#F0F0F0")
                    icon_lbl.image = icon_img
                    icon_lbl.pack(side="left", padx=(0, 6))

                txt_frame = tk.Frame(hdr_frame, bg="#F0F0F0")
                txt_frame.pack(side="left", fill="both", expand=True)

                lbl_top = tk.Label(txt_frame, text=item.get("title", ""), bg="#F0F0F0",
                                   fg=self.ACCENT_BLUE, font=("Segoe UI", 8, "bold"), anchor="w")
                lbl_top.pack(fill="x")
                if "subtitle" in item:
                    lbl_sub = tk.Label(txt_frame, text=item.get("subtitle", ""), bg="#F0F0F0",
                                       fg=self.TEXT_MUTED, font=("Segoe UI", 7), anchor="w")
                    lbl_sub.pack(fill="x")
                continue

            row = tk.Frame(self.container, bg=self.BG_COLOR, padx=6, pady=3, cursor="arrow")
            row.pack(fill="x", pady=1)

            # Left icon (fixed width column)
            icon_lbl = tk.Label(row, text=item.get("icon", " "), bg=self.BG_COLOR,
                                fg=self.TEXT_COLOR, font=("Segoe UI Emoji", 10), width=2, anchor="center")
            icon_lbl.pack(side="left", padx=(2, 6))

            # Center text
            txt_lbl = tk.Label(row, text=item.get("label", ""), bg=self.BG_COLOR,
                               fg=self.TEXT_COLOR, font=("Segoe UI", 9), anchor="w")
            txt_lbl.pack(side="left", fill="x", expand=True)

            # Right badge / checkmark / chevron
            right_text = ""
            right_color = self.TEXT_MUTED
            if item.get("submenu"):
                right_text = "›"
            elif item.get("checked"):
                right_text = "✓"
                right_color = self.ACCENT_BLUE
            elif item.get("shortcut"):
                right_text = item.get("shortcut")

            right_lbl = tk.Label(row, text=right_text, bg=self.BG_COLOR,
                                 fg=right_color, font=("Segoe UI", 8, "bold" if item.get("checked") else "normal"), anchor="e")
            right_lbl.pack(side="right", padx=(10, 4))

            widgets = [row, icon_lbl, txt_lbl, right_lbl]
            for w in widgets:
                w.bind("<Enter>", lambda e, r=row, it=item, ws=widgets: self._on_enter(r, it, ws))
                w.bind("<Leave>", lambda e, r=row, it=item, ws=widgets: self._on_leave(r, it, ws))
                w.bind("<Button-1>", lambda e, it=item: self._on_click(it))

    def _on_enter(self, row, item, widgets):
        for w in widgets:
            w.configure(bg=self.HOVER_BG)
        if item.get("submenu"):
            if self.active_submenu and self.active_submenu_item != item["submenu"]:
                self.active_submenu.destroy()
                self.active_submenu = None
            if not self.active_submenu:
                self._open_submenu(row, item["submenu"])
        else:
            if self.active_submenu:
                self.active_submenu.destroy()
                self.active_submenu = None

    def _on_leave(self, row, item, widgets):
        if not (self.active_submenu and self.active_submenu_item == item.get("submenu")):
            for w in widgets:
                w.configure(bg=self.BG_COLOR)

    def _open_submenu(self, row, sub_items):
        self.active_submenu_item = sub_items
        sub = Win10LightContextMenu(self.master, sub_items, is_submenu=True, parent_menu=self)
        self.active_submenu = sub

        self.win.update_idletasks()
        sub.win.update_idletasks()

        parent_rx = self.win.winfo_rootx()
        parent_rw = self.win.winfo_width()
        row_ry = row.winfo_rooty()

        sub_w = sub.win.winfo_reqwidth()
        sub_h = sub.win.winfo_reqheight()
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()

        # Place immediately adjacent to right edge
        if parent_rx + parent_rw + sub_w <= sw - 8:
            sub_x = parent_rx + parent_rw - 2
        else:
            sub_x = parent_rx - sub_w + 2

        sub_y = row_ry - 2
        if sub_y + sub_h > sh - 35:
            sub_y = max(4, sh - sub_h - 35)

        sub.show(max(4, sub_x), max(4, sub_y))

    def _on_click(self, item):
        cmd = item.get("command")
        if cmd:
            self.dismiss_all()
            cmd()

    def show(self, x, y):
        self.win.update_idletasks()
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        w = self.win.winfo_reqwidth()
        h = self.win.winfo_reqheight()

        if not self.is_submenu:
            if x + w > sw - 10:
                x = sw - w - 10
            if y + h > sh - 40:
                y = sh - h - 40

        self.win.geometry(f"+{max(4, x)}+{max(4, y)}")
        self.win.deiconify()
        self.win.lift()
        self.win.focus_set()

    def _on_master_click(self, e):
        if self.win.winfo_ismapped():
            x, y = self.win.winfo_pointerxy()
            wx, wy = self.win.winfo_x(), self.win.winfo_y()
            ww, wh = self.win.winfo_width(), self.win.winfo_height()
            if not (wx <= x <= wx + ww and wy <= y <= wy + wh):
                self.dismiss_all()

    def _on_focus_out(self, e):
        if not self.active_submenu:
            self.win.after(120, self._check_focus)

    def _check_focus(self):
        try:
            if not self.win.focus_get() and not self.active_submenu:
                self.dismiss_all()
        except Exception:
            pass

    def dismiss_all(self):
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None
        if self.parent_menu:
            self.parent_menu.dismiss_all()
        else:
            self.destroy()

    def destroy(self):
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None
        try:
            self.win.destroy()
        except Exception:
            pass

# ══════════════════════════════════════════════════════════════════════
#  PROCEDURAL CUTE CAT RENDERER (Pure Vector Anatomy & Animations)
# ══════════════════════════════════════════════════════════════════════

class CuteCatRenderer:
    """
    Pure procedural 4x supersampled Cute Cat companion.
    No image files needed! Rendered with high precision vectors,
    calico fur patterns, expressive emerald anime eyes, twitching ears,
    chubby whisker pads, swinging tail, and soft pink paw pads.
    """
    AA = 4

    # Palette
    FUR_CREAM     = (255, 242, 230, 255)   # Base creamy soft kitten fur
    FUR_GINGER    = (238, 142, 65, 255)    # Calico ginger patches
    FUR_GINGER_DK = (195, 105, 40, 255)    # Ginger patch shadow
    FUR_SHADOW    = (225, 205, 190, 255)   # Body depth shadow
    FUR_WHITE     = (255, 255, 255, 255)   # Pure white chest & paws
    
    EAR_OUTER     = (238, 142, 65, 255)    # Pointy kitty ear
    EAR_INNER     = (255, 185, 195, 255)   # Soft pink inner ear fluff
    EAR_SHADOW    = (190, 100, 45, 255)

    EYE_EMERALD   = (38, 196, 130, 255)    # Brilliant emerald iris
    EYE_EMERALD_LT= (105, 240, 180, 255)   # Lower iris glow
    EYE_PUPIL     = (20, 22, 28, 255)      # Feline pupil
    EYE_WHITE     = (255, 255, 255, 255)   # High specular sparkle

    NOSE_PINK     = (255, 145, 165, 255)   # Dainty heart nose
    NOSE_SHADOW   = (215, 105, 125, 255)
    
    CHEEK_BLUSH   = (255, 155, 175, 130)   # Rosy cheeks
    PAW_PAD       = (255, 160, 175, 255)   # Cute pink toe beans
    
    COLLAR_RED    = (235, 45, 65, 255)     # Cute red bell collar
    BELL_GOLD     = (255, 218, 55, 255)    # Shiny golden bell
    BELL_SHINE    = (255, 248, 185, 255)
    
    WHISKER_COL   = (255, 255, 255, 220)   # White whiskers
    WHISKER_DK    = (120, 100, 95, 160)    # Shadow whisker

    def __init__(self, w=110, h=105, tcolor="#FF00FF"):
        self.w, self.h = w, h
        self.tcolor = tcolor
        self.aw, self.ah = w * self.AA, h * self.AA
        self.direction = 1
        # Design space: 160 x 150
        self.sx = self.w / 160.0
        self.sy = self.h / 150.0

    def set_size(self, w, h):
        self.w, self.h = w, h
        self.aw, self.ah = w * self.AA, h * self.AA
        self.sx = self.w / 160.0
        self.sy = self.h / 150.0

    def _new(self):
        return Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))

    def _s(self, v):
        return int(v * self.AA)

    def _mx(self, x):
        xm = x * self.sx
        if self.direction == -1:
            xm = self.w - xm
        return self._s(xm)

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

    def _line(self, d, pts, fill, width=1.5):
        mapped = [(self._mx(x), self._my(y)) for x, y in pts]
        d.line(mapped, fill=fill, width=max(1, self._s(width * min(self.sx, self.sy))))

    def _arc(self, d, cx, cy, rx, ry, start, end, fill, width=1.5):
        mcx, mcy = self._mx(cx), self._my(cy)
        mrx, mry = self._s(rx * self.sx), self._s(ry * self.sy)
        box = [mcx - mrx, mcy - mry, mcx + mrx, mcy + mry]
        s, e = start, end
        if self.direction == -1:
            s, e = 180 - end, 180 - start
        d.arc(box, s, e, fill=fill, width=max(1, self._s(width * min(self.sx, self.sy))))

    def _render(self, img):
        resized = img.resize((self.w, self.h), Image.LANCZOS)
        tc = self.tcolor.lstrip('#')
        rt, gt, bt = tuple(int(tc[i:i+2], 16) for i in (0, 2, 4))
        bg = Image.new("RGBA", (self.w, self.h), (rt, gt, bt, 255))
        alpha = resized.split()[-1]
        clean_mask = alpha.point(lambda p: 255 if p >= 70 else 0)
        final = Image.composite(resized.convert("RGB"), bg.convert("RGB"), clean_mask)
        return ImageTk.PhotoImage(final)

    def _ground_shadow(self, d, cx=80, cy=136, rx=42, ry=9):
        self._ell(d, cx, cy, rx, ry, (25, 20, 35, 45))
        self._ell(d, cx, cy, rx * 0.72, ry * 0.65, (20, 15, 30, 75))

    def _draw_pointy_ear(self, d, cx, cy, side=-1, twitch=0.0):
        """Cute triangular feline ear with soft pink inner fluff and tufts."""
        s = side
        ex = cx + s * 22
        ey = cy - 20 + twitch
        
        # Outer ear polygon
        ear_pts = [
            (ex - s * 14, ey + 10),
            (ex - s * 3, ey - 22 + twitch),
            (ex + s * 16, ey + 6),
        ]
        self._pol(d, ear_pts, self.EAR_OUTER, outline=self.EAR_SHADOW, width=1.2)

        # Calico patch on one ear
        if s == 1:
            patch_pts = [
                (ex - s * 2, ey - 21 + twitch),
                (ex + s * 15, ey + 5),
                (ex + s * 5, ey - 4)
            ]
            self._pol(d, patch_pts, (75, 45, 35, 255))

        # Inner ear fluff
        inner_pts = [
            (ex - s * 9, ey + 6),
            (ex - s * 2, ey - 14 + twitch),
            (ex + s * 10, ey + 3),
        ]
        self._pol(d, inner_pts, self.EAR_INNER)
        
        # Ear tuft hairs
        self._line(d, [(ex - s * 10, ey + 4), (ex - s * 3, ey - 4)], (255, 255, 255, 220), width=1.5)
        self._line(d, [(ex - s * 6, ey + 7), (ex, ey - 1)], (255, 255, 255, 200), width=1.2)

    def _draw_cat_eye(self, d, ex, ey, r=8.0, blink=0.0, happy=False):
        """Expressive emerald feline eye with crystal glints."""
        if happy or blink > 0.75:
            # Happy smiling arc
            self._arc(d, ex, ey + 1, r * 1.1, r * 0.7, 195, 345, (30, 20, 25, 255), width=2.4)
            self._arc(d, ex + (1 if self.direction == 1 else -1) * 3, ey + 2, r * 0.6, r * 0.4, 210, 330, (30, 20, 25, 255), width=1.8)
            return

        ry = max(1.5, r * (1.0 - blink))
        # Eye socket & dark liner
        self._ell(d, ex, ey, r + 0.8, ry + 0.8, (25, 18, 22, 255))
        # Emerald iris
        self._ell(d, ex, ey, r, ry, self.EYE_EMERALD)
        self._ell(d, ex, ey + 2, r * 0.75, max(1.0, ry * 0.5), self.EYE_EMERALD_LT)
        
        # Feline pupil (almond oval)
        pw = max(1.2, r * 0.45)
        ph = max(1.0, ry * 0.85)
        self._ell(d, ex, ey, pw, ph, self.EYE_PUPIL)
        
        # High-gloss sparkles
        if blink < 0.3:
            self._cir(d, ex - 2.8, ey - 2.5, 2.5, self.EYE_WHITE)
            self._cir(d, ex + 2.5, ey + 2.5, 1.4, (255, 255, 255, 210))
            self._cir(d, ex - 0.5, ey + 3.0, 0.9, (255, 255, 255, 170))

    def _draw_cat_muzzle(self, d, cx, cy):
        """Chubby white whisker pads, heart nose, and delicate whiskers."""
        # Whisker pads
        self._ell(d, cx - 7.5, cy + 4, 9.5, 7.5, self.FUR_WHITE, outline=(230, 215, 205, 255), width=1)
        self._ell(d, cx + 7.5, cy + 4, 9.5, 7.5, self.FUR_WHITE, outline=(230, 215, 205, 255), width=1)
        self._ell(d, cx, cy + 6.5, 5.5, 4.0, (255, 200, 210, 255))

        # Cheek blush
        self._cir(d, cx - 21, cy + 3, 6.0, self.CHEEK_BLUSH)
        self._cir(d, cx + 21, cy + 3, 6.0, self.CHEEK_BLUSH)

        # Sweet smile
        self._arc(d, cx - 5.0, cy + 5.5, 4.5, 3.8, 20, 160, (50, 30, 35, 255), width=1.6)
        self._arc(d, cx + 5.0, cy + 5.5, 4.5, 3.8, 20, 160, (50, 30, 35, 255), width=1.6)

        # Pink nose
        self._pol(d, [(cx - 4.5, cy - 1.0), (cx + 4.5, cy - 1.0), (cx, cy + 3.2)], self.NOSE_PINK, outline=self.NOSE_SHADOW, width=1.0)
        self._cir(d, cx - 1.2, cy - 0.2, 1.2, (255, 255, 255, 220))

        # Real Feline Whiskers (3 on each side)
        for side in (-1, 1):
            wx = cx + side * 14
            self._line(d, [(wx, cy + 2), (wx + side * 22, cy - 3)], self.WHISKER_COL, width=1.2)
            self._line(d, [(wx, cy + 5), (wx + side * 24, cy + 4)], self.WHISKER_COL, width=1.2)
            self._line(d, [(wx, cy + 7), (wx + side * 20, cy + 10)], self.WHISKER_COL, width=1.2)

    def _draw_cat_tail(self, d, bx, by, curl=0.0):
        """Graceful curved feline tail with dynamic waving."""
        rad = math.radians(curl)
        tip_x = bx + 28 + math.sin(rad) * 16
        tip_y = by - 24 - math.cos(rad) * 14
        mid_x = bx + 16 + math.sin(rad) * 6
        mid_y = by - 8

        tail_pts = [
            (bx - 3, by + 4),
            (mid_x - 5, mid_y),
            (tip_x - 3, tip_y - 2),
            (tip_x + 4, tip_y),
            (tip_x + 3, tip_y + 6),
            (mid_x + 5, mid_y + 4),
            (bx + 4, by - 2)
        ]
        self._pol(d, tail_pts, self.FUR_GINGER, outline=self.FUR_GINGER_DK, width=1.1)
        # White tip
        self._cir(d, tip_x, tip_y, 4.8, self.FUR_WHITE)

    def _draw_bell_collar(self, d, cx, cy, wag=0.0):
        """Ruby collar with shiny golden bell."""
        self._ell(d, cx, cy, 21, 6.0, self.COLLAR_RED, outline=(180, 20, 35, 255), width=1.1)
        # Bell
        bx = cx + wag * 0.3
        by = cy + 6.0
        self._cir(d, bx, by, 4.5, self.BELL_GOLD, outline=(180, 140, 20, 255), width=1.0)
        self._cir(d, bx - 1.2, by - 1.2, 1.4, self.BELL_SHINE)
        self._line(d, [(bx - 2.5, by + 1.2), (bx + 2.5, by + 1.2)], (140, 95, 15, 255), width=1.0)

    # ── POSE: SIT ───────────────────────────────────────────
    def draw_sit(self, frame, landing_squash=0.0):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        breath = math.sin(frame * 0.22) * 1.5
        tail_wave = math.sin(frame * 0.35) * 14.0
        ear_twitch = math.sin(frame * 0.4) * 1.2 if (frame % 30 < 10) else 0.0

        sq_x = 1.0 + landing_squash * 0.35
        sq_y = 1.0 - landing_squash * 0.25

        self._ground_shadow(d, cx, 136, 44 * sq_x, 9 * sq_y)
        self._draw_cat_tail(d, cx + 22, 106 + breath, curl=tail_wave)

        # Hind legs / loaf base
        self._ell(d, cx - 26, 114, 14 * sq_x, 18 * sq_y, self.FUR_SHADOW)
        self._ell(d, cx + 26, 114, 14 * sq_x, 18 * sq_y, self.FUR_GINGER)

        # Main body
        by = 96 + breath + int(landing_squash * 5)
        self._ell(d, cx, by, 32 * sq_x, 26 * sq_y, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        # Calico ginger side patch
        self._ell(d, cx + 14, by - 4, 18, 20, self.FUR_GINGER)
        # White fluffy bib/chest
        self._ell(d, cx, by + 4, 18, 20, self.FUR_WHITE)

        # Front paws
        for lx in (cx - 10, cx + 10):
            self._ell(d, lx, 126, 7.5, 6.0, self.FUR_WHITE, outline=(225, 210, 200, 255), width=1)
            self._cir(d, lx - 2.5, 126.5, 1.2, (255, 175, 190, 255))
            self._cir(d, lx + 2.5, 126.5, 1.2, (255, 175, 190, 255))

        self._draw_bell_collar(d, cx, by - 14, wag=tail_wave * 0.2)

        # Head
        hy = 56 + breath * 0.6 + int(landing_squash * 3)
        self._draw_pointy_ear(d, cx, hy, side=-1, twitch=ear_twitch)
        self._draw_pointy_ear(d, cx, hy, side=1, twitch=-ear_twitch)

        self._ell(d, cx, hy, 29 * sq_x, 25 * sq_y, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        # Calico forehead patch
        self._ell(d, cx + 10, hy - 10, 16, 14, self.FUR_GINGER)
        self._ell(d, cx - 12, hy - 12, 11, 9, (80, 50, 40, 255)) # Dark calico spot

        # Eyes & blink
        blink_cycle = (frame % 42)
        blink = 1.0 if 38 <= blink_cycle <= 40 else 0.0
        self._draw_cat_eye(d, cx - 11, hy - 1, r=7.5, blink=blink)
        self._draw_cat_eye(d, cx + 11, hy - 1, r=7.5, blink=blink)

        self._draw_cat_muzzle(d, cx, hy + 9)

        return self._render(img)

    # ── POSE: WALK ──────────────────────────────────────────
    def draw_walk(self, frame, walk_cycle=0.0):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        cycle = walk_cycle if walk_cycle != 0.0 else (frame * 0.45)
        step_bob = abs(math.sin(cycle)) * 4.2
        stride = math.sin(cycle) * 14.0
        tail_wave = math.sin(cycle) * 20.0

        self._ground_shadow(d, cx, 136, 45, 9)
        self._draw_cat_tail(d, cx + 22, 102 - step_bob, curl=tail_wave)

        # Back legs walking stride
        self._ell(d, cx - 22 + stride * 0.5, 116, 12, 16, self.FUR_SHADOW)
        self._ell(d, cx + 22 - stride * 0.5, 116, 12, 16, self.FUR_GINGER)

        # Body
        by = 92 - int(step_bob)
        self._ell(d, cx, by, 33, 25, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        self._ell(d, cx + 14, by - 4, 18, 20, self.FUR_GINGER)
        self._ell(d, cx, by + 4, 18, 20, self.FUR_WHITE)

        # Front stepping paws
        paw_l_y = 126 + int(stride * 0.4)
        paw_r_y = 126 - int(stride * 0.4)
        self._ell(d, cx - 12 - stride * 0.6, paw_l_y, 7.5, 6.0, self.FUR_WHITE, outline=(225, 210, 200, 255), width=1)
        self._ell(d, cx + 12 + stride * 0.6, paw_r_y, 7.5, 6.0, self.FUR_WHITE, outline=(225, 210, 200, 255), width=1)

        self._draw_bell_collar(d, cx, by - 14, wag=stride * 0.3)

        # Head alert
        hy = 52 - int(step_bob * 0.7)
        self._draw_pointy_ear(d, cx, hy, side=-1, twitch=stride * 0.1)
        self._draw_pointy_ear(d, cx, hy, side=1, twitch=-stride * 0.1)

        self._ell(d, cx, hy, 29, 25, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        self._ell(d, cx + 10, hy - 10, 16, 14, self.FUR_GINGER)
        self._ell(d, cx - 12, hy - 12, 11, 9, (80, 50, 40, 255))

        self._draw_cat_eye(d, cx - 11, hy - 1, r=7.5, blink=0.0)
        self._draw_cat_eye(d, cx + 11, hy - 1, r=7.5, blink=0.0)
        self._draw_cat_muzzle(d, cx, hy + 9)

        return self._render(img)

    # ── POSE: PURR ──────────────────────────────────────────
    def draw_purr(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        purr_rumble = math.sin(frame * 0.9) * 1.5
        tail_wave = math.sin(frame * 0.5) * 18.0

        self._ground_shadow(d, cx, 136, 44, 9)
        self._draw_cat_tail(d, cx + 22, 106 + purr_rumble, curl=tail_wave)

        by = 96 + purr_rumble
        self._ell(d, cx, by, 32, 26, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        self._ell(d, cx + 14, by - 4, 18, 20, self.FUR_GINGER)
        self._ell(d, cx, by + 4, 18, 20, self.FUR_WHITE)

        for lx in (cx - 10, cx + 10):
            self._ell(d, lx, 126, 7.5, 6.0, self.FUR_WHITE, outline=(225, 210, 200, 255), width=1)

        self._draw_bell_collar(d, cx, by - 14, wag=tail_wave * 0.3)

        hy = 56 + purr_rumble * 0.7
        self._draw_pointy_ear(d, cx, hy, side=-1, twitch=1.5)
        self._draw_pointy_ear(d, cx, hy, side=1, twitch=-1.5)

        self._ell(d, cx, hy, 29, 25, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        self._ell(d, cx + 10, hy - 10, 16, 14, self.FUR_GINGER)
        self._ell(d, cx - 12, hy - 12, 11, 9, (80, 50, 40, 255))

        # Blissful closed eyes
        self._draw_cat_eye(d, cx - 11, hy - 1, r=7.5, happy=True)
        self._draw_cat_eye(d, cx + 11, hy - 1, r=7.5, happy=True)
        self._draw_cat_muzzle(d, cx, hy + 9)

        # Floating heart particles
        for i, off in enumerate([-20, 20]):
            hy_p = (frame * 3 + i * 16) % 40
            alpha = int(max(0, 255 - hy_p * 6.0))
            hx = cx + off + int(math.sin((frame + i * 5) * 0.3) * 6)
            d.text((self._mx(hx), self._my(hy - 26 - hy_p)), "♡", fill=(255, 90, 150, alpha))

        return self._render(img)

    # ── POSE: SLEEP ─────────────────────────────────────────
    def draw_sleep(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        breath = math.sin(frame * 0.18) * 1.5
        self._ground_shadow(d, cx, 136, 42, 8)
        by = 100 + breath
        self._ell(d, cx, by, 32, 22, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        self._ell(d, cx + 12, by - 2, 16, 16, self.FUR_GINGER)
        self._arc(d, cx, by + 4, 30, 16, 10, 190, self.FUR_GINGER, width=4.5)
        self._cir(d, cx - 22, by + 10, 4.5, self.FUR_WHITE)
        hy = 82 + breath * 0.6
        self._draw_pointy_ear(d, cx - 12, hy, side=-1, twitch=0.0)
        self._draw_pointy_ear(d, cx + 12, hy, side=1, twitch=0.0)
        self._ell(d, cx, hy, 22, 18, self.FUR_CREAM, outline=self.FUR_SHADOW, width=1.1)
        self._arc(d, cx - 8, hy + 2, 5, 3, 20, 160, (50, 40, 45, 255), width=1.6)
        self._arc(d, cx + 8, hy + 2, 5, 3, 20, 160, (50, 40, 45, 255), width=1.6)
        self._draw_cat_muzzle(d, cx, hy + 7)
        for i, off in enumerate([-12, 12]):
            zy = (frame * 2 + i * 14) % 36
            alpha = int(max(0, 240 - zy * 6.5))
            zx = cx + off + int(math.sin((frame + i * 4) * 0.3) * 5)
            d.text((self._mx(zx), self._my(hy - 16 - zy)), "z", fill=(140, 180, 255, alpha))
        return self._render(img)


# ══════════════════════════════════════════════════════════════════════
#  PROCEDURAL SPIDER-MAN RENDERER (Pure Vector Marvel Hero Engine)
# ══════════════════════════════════════════════════════════════════════

class SpidermanRenderer:
    """
    Pure procedural 4x supersampled Spider-Man companion.
    No image files needed! Rendered with high precision vectors:
    classic Marvel red & blue suit, full web grid patterns, black chest spider,
    expressive comic eye lenses, Spider-Sense tingling aura, web-swinging,
    wall crawling, and Thwip web blasts.
    """
    AA = 4

    # Palette
    SUIT_RED      = (225, 30, 45, 255)     # Classic Spider-Man red
    SUIT_RED_LT   = (255, 65, 80, 255)     # Highlight red
    SUIT_RED_DK   = (175, 18, 30, 255)     # Shadow red
    
    SUIT_BLUE     = (25, 75, 195, 255)     # Comic royal blue
    SUIT_BLUE_LT  = (50, 115, 240, 255)    # Blue highlight
    SUIT_BLUE_DK  = (14, 42, 115, 255)     # Blue shadow

    LENS_WHITE    = (255, 255, 255, 255)   # Mask lens
    LENS_RIM      = (18, 18, 24, 255)      # Bold black lens frame
    LENS_GLINT    = (210, 245, 255, 210)   # Glass specular glint

    WEB_LINE      = (22, 22, 28, 235)      # Black web grid on suit
    SPIDER_BLACK  = (18, 18, 22, 255)      # Chest spider emblem
    WEB_SILK      = (255, 255, 255, 245)   # Shooting web silk
    WEB_AURA      = (180, 235, 255, 160)   # Web glow aura

    SHADOW_COL    = (20, 20, 35, 70)

    def __init__(self, w=110, h=105, tcolor="#FF00FF"):
        self.w, self.h = w, h
        self.tcolor = tcolor
        self.aw, self.ah = w * self.AA, h * self.AA
        self.direction = 1
        # Design space: 160 x 150
        self.sx = self.w / 160.0
        self.sy = self.h / 150.0

    def set_size(self, w, h):
        self.w, self.h = w, h
        self.aw, self.ah = w * self.AA, h * self.AA
        self.sx = self.w / 160.0
        self.sy = self.h / 150.0

    def _new(self):
        return Image.new("RGBA", (self.aw, self.ah), (0, 0, 0, 0))

    def _s(self, v):
        return int(v * self.AA)

    def _mx(self, x):
        xm = x * self.sx
        if self.direction == -1:
            xm = self.w - xm
        return self._s(xm)

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

    def _line(self, d, pts, fill, width=1.5):
        mapped = [(self._mx(x), self._my(y)) for x, y in pts]
        d.line(mapped, fill=fill, width=max(1, self._s(width * min(self.sx, self.sy))))

    def _arc(self, d, cx, cy, rx, ry, start, end, fill, width=1.5):
        mcx, mcy = self._mx(cx), self._my(cy)
        mrx, mry = self._s(rx * self.sx), self._s(ry * self.sy)
        box = [mcx - mrx, mcy - mry, mcx + mrx, mcy + mry]
        s, e = start, end
        if self.direction == -1:
            s, e = 180 - end, 180 - start
        d.arc(box, s, e, fill=fill, width=max(1, self._s(width * min(self.sx, self.sy))))

    def _render(self, img):
        resized = img.resize((self.w, self.h), Image.LANCZOS)
        tc = self.tcolor.lstrip('#')
        rt, gt, bt = tuple(int(tc[i:i+2], 16) for i in (0, 2, 4))
        bg = Image.new("RGBA", (self.w, self.h), (rt, gt, bt, 255))
        alpha = resized.split()[-1]
        clean_mask = alpha.point(lambda p: 255 if p >= 70 else 0)
        final = Image.composite(resized.convert("RGB"), bg.convert("RGB"), clean_mask)
        return ImageTk.PhotoImage(final)

    def _ground_shadow(self, d, cx=80, cy=136, rx=38, ry=8):
        self._ell(d, cx, cy, rx, ry, (20, 20, 35, 50))
        self._ell(d, cx, cy, rx * 0.7, ry * 0.6, (15, 15, 30, 80))

    def _draw_spider_emblem(self, d, cx, cy, scale=1.0):
        """Classic iconic black arachnid emblem on chest."""
        s = scale
        # Central spider body
        self._ell(d, cx, cy, 3.2 * s, 5.0 * s, self.SPIDER_BLACK)
        self._cir(d, cx, cy - 4.5 * s, 2.2 * s, self.SPIDER_BLACK)
        # 8 spider legs
        for side in (-1, 1):
            # Top legs reaching up
            self._line(d, [(cx + side * 1.5, cy - 2.5), (cx + side * 8 * s, cy - 9 * s), (cx + side * 11 * s, cy - 13 * s)], self.SPIDER_BLACK, width=1.4)
            self._line(d, [(cx + side * 2.0, cy - 1.0), (cx + side * 9 * s, cy - 5 * s), (cx + side * 13 * s, cy - 7 * s)], self.SPIDER_BLACK, width=1.4)
            # Bottom legs reaching down
            self._line(d, [(cx + side * 2.0, cy + 1.0), (cx + side * 9 * s, cy + 5 * s), (cx + side * 12 * s, cy + 10 * s)], self.SPIDER_BLACK, width=1.4)
            self._line(d, [(cx + side * 1.5, cy + 2.5), (cx + side * 7 * s, cy + 8 * s), (cx + side * 9 * s, cy + 14 * s)], self.SPIDER_BLACK, width=1.4)

    def _draw_mask_lens(self, d, ex, ey, side=-1, squint=0.0):
        """Iconic comic-book Spider-Man white eye lens with bold black border."""
        s = side
        sq = squint * 3.0
        # Lens outer polygon
        pts_rim = [
            (ex - s * 14, ey - 7 + sq),
            (ex + s * 11, ey - 4 + sq * 0.5),
            (ex + s * 3, ey + 11 - sq),
            (ex - s * 12, ey + 4),
        ]
        self._pol(d, pts_rim, self.LENS_RIM)

        # White reflective interior
        pts_in = [
            (ex - s * 11, ey - 5 + sq),
            (ex + s * 9, ey - 3 + sq * 0.5),
            (ex + s * 2, ey + 8 - sq),
            (ex - s * 9, ey + 3),
        ]
        self._pol(d, pts_in, self.LENS_WHITE)

        # Lens glint specular highlight
        self._line(d, [(ex - s * 8, ey - 2 + sq), (ex + s * 5, ey - 1 + sq * 0.5)], self.LENS_GLINT, width=1.6)

    def _draw_web_grid(self, d, cx, cy, rx, ry):
        """Web grid lines radiating from nose bridge across red mask."""
        # Radiating web lines
        for ang in [-50, -25, 0, 25, 50]:
            rad = math.radians(ang)
            wx = cx + math.sin(rad) * rx * 0.95
            wy = cy - math.cos(rad) * ry * 0.95
            self._line(d, [(cx, cy + 3), (wx, wy)], self.WEB_LINE, width=1.1)
        # Concentric curved web arcs
        for r_scale in [0.35, 0.65, 0.90]:
            self._arc(d, cx, cy + 2, rx * r_scale, ry * r_scale, 200, 340, self.WEB_LINE, width=1.1)

    def _draw_spidey_sense(self, d, cx, cy, frame):
        """Electric comic-book Spider-Sense tingling arcs around head."""
        arc_phase = frame % 30
        if arc_phase < 18:
            alpha = int(255 - (arc_phase / 18.0) * 120)
            col_gold = (255, 225, 30, alpha)
            col_red = (255, 50, 40, alpha)
            for side in (-1, 1):
                ax = cx + side * 22
                ay = cy - 24
                # Zig-zag electric tingling lines
                self._line(d, [(ax, ay), (ax + side * 7, ay - 9)], col_gold, width=2.0)
                self._line(d, [(ax + side * 7, ay - 9), (ax + side * 14, ay - 5)], col_red, width=2.0)
                self._line(d, [(ax + side * 14, ay - 5), (ax + side * 21, ay - 14)], col_gold, width=2.0)

    # ── POSE: IDLE ──────────────────────────────────────────
    def draw_idle(self, frame, landing_squash=0.0):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        breath = math.sin(frame * 0.25) * 1.5
        sq_x = 1.0 + landing_squash * 0.35
        sq_y = 1.0 - landing_squash * 0.25

        self._ground_shadow(d, cx, 136, 40 * sq_x, 9 * sq_y)

        # Legs in athletic ready stance
        # Left leg (blue thigh, red boot)
        self._ell(d, cx - 18 * sq_x, 108, 7, 18, self.SUIT_BLUE, outline=self.SUIT_BLUE_DK, width=1)
        self._ell(d, cx - 19 * sq_x, 126, 8, 10, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1)
        # Right leg
        self._ell(d, cx + 18 * sq_x, 108, 7, 18, self.SUIT_BLUE, outline=self.SUIT_BLUE_DK, width=1)
        self._ell(d, cx + 19 * sq_x, 126, 8, 10, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1)

        # Torso
        by = 82 + breath + int(landing_squash * 5)
        # Blue waist & ribs
        self._ell(d, cx, by + 6, 22 * sq_x, 18 * sq_y, self.SUIT_BLUE, outline=self.SUIT_BLUE_DK, width=1)
        # Red chest shield
        self._pol(d, [
            (cx - 16 * sq_x, by - 12),
            (cx + 16 * sq_x, by - 12),
            (cx + 12 * sq_x, by + 12),
            (cx - 12 * sq_x, by + 12)
        ], self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.1)

        # Web grid on chest
        for ang in [-30, 0, 30]:
            rad = math.radians(ang)
            self._line(d, [(cx, by - 12), (cx + math.sin(rad) * 14, by + 10)], self.WEB_LINE, width=1.0)
        self._arc(d, cx, by - 2, 12, 8, 20, 160, self.WEB_LINE, width=1.0)

        # Chest spider emblem
        self._draw_spider_emblem(d, cx, by, scale=1.0)

        # Arms (heroic fists)
        # Left arm
        self._ell(d, cx - 24 * sq_x, by - 2, 6, 12, self.SUIT_BLUE)
        self._ell(d, cx - 25 * sq_x, by + 12, 7, 8, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1)
        # Right arm
        self._ell(d, cx + 24 * sq_x, by - 2, 6, 12, self.SUIT_BLUE)
        self._ell(d, cx + 25 * sq_x, by + 12, 7, 8, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1)

        # Mask / Head
        hy = 48 + breath * 0.7 + int(landing_squash * 3)
        self._ell(d, cx, hy, 23 * sq_x, 26 * sq_y, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.2)
        self._draw_web_grid(d, cx, hy, 23 * sq_x, 26 * sq_y)

        # Expressive eye lenses (squint when breathing or thinking)
        squint_val = math.sin(frame * 0.15) * 0.25 if frame % 40 < 20 else 0.0
        self._draw_mask_lens(d, cx - 10, hy, side=-1, squint=squint_val)
        self._draw_mask_lens(d, cx + 10, hy, side=1, squint=squint_val)

        # Spider-Sense tingling aura
        self._draw_spidey_sense(d, cx, hy, frame)

        return self._render(img)

    # ── POSE: ATHLETIC DASH ─────────────────────────────────
    def draw_dash(self, frame, walk_cycle=0.0):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        cycle = walk_cycle if walk_cycle != 0.0 else (frame * 0.5)
        step_bob = abs(math.sin(cycle)) * 4.0
        stride = math.sin(cycle) * 16.0

        # Motion speed streak trails trailing behind Spider-Man
        trail_dir = -self.direction
        for i in range(5):
            st_x = cx + trail_dir * (22 + i * 12)
            st_y = 65 + i * 12 + int(math.sin(frame * 0.4 + i) * 3)
            st_len = random.randint(18, 30)
            col = (255, 45, 60, max(30, 160 - i * 30)) if i % 2 == 0 else (45, 120, 255, max(30, 160 - i * 30))
            self._line(d, [(st_x, st_y), (st_x + trail_dir * st_len, st_y)], col, width=2.0)

        # Stretched shadow
        self._ground_shadow(d, cx, 136, 46, 8)

        # Low crouch forward athletic lean
        lean_x = 8.0

        # Running legs
        # Front leg lunging
        self._ell(d, cx + stride * 0.7 + lean_x, 112, 7, 16, self.SUIT_BLUE)
        self._ell(d, cx + stride * 0.7 + lean_x + 4, 128, 8, 9, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1)
        # Back leg trailing
        self._ell(d, cx - stride * 0.7 + lean_x, 114, 7, 16, self.SUIT_BLUE)
        self._ell(d, cx - stride * 0.7 + lean_x - 6, 128, 8, 9, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1)

        # Torso angled forward
        by = 80 - int(step_bob)
        self._ell(d, cx + lean_x, by + 4, 21, 16, self.SUIT_BLUE)
        self._pol(d, [
            (cx - 14 + lean_x, by - 12),
            (cx + 18 + lean_x, by - 10),
            (cx + 14 + lean_x, by + 12),
            (cx - 10 + lean_x, by + 12)
        ], self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.1)

        self._draw_spider_emblem(d, cx + lean_x, by, scale=0.95)

        # Pumping arms
        # Back arm reaching back
        self._ell(d, cx - 22 - stride * 0.4 + lean_x, by + 2, 6, 14, self.SUIT_BLUE)
        self._ell(d, cx - 26 - stride * 0.4 + lean_x, by + 14, 7, 8, self.SUIT_RED)
        # Front arm reaching forward
        self._ell(d, cx + 24 + stride * 0.4 + lean_x, by - 2, 6, 14, self.SUIT_BLUE)
        self._ell(d, cx + 28 + stride * 0.4 + lean_x, by + 8, 7, 8, self.SUIT_RED)

        # Head angled low
        hy = 46 - int(step_bob * 0.7)
        self._ell(d, cx + lean_x + 4, hy, 23, 24, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.2)
        self._draw_web_grid(d, cx + lean_x + 4, hy, 23, 24)

        # Focused squinting lenses
        self._draw_mask_lens(d, cx + lean_x - 6, hy, side=-1, squint=0.35)
        self._draw_mask_lens(d, cx + lean_x + 14, hy, side=1, squint=0.35)

        return self._render(img)

    # ── POSE: WEB SWING ─────────────────────────────────────
    def draw_web_swing(self, frame, flight_tilt=0.0):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        swing_angle = math.sin(frame * 0.35) * 22.0 + flight_tilt * 0.8

        # Web anchor at screen ceiling (y = 0)
        hand_x = cx + 18
        hand_y = 36
        anchor_x = cx - int(swing_angle * 1.6)

        # Braided glowing web line
        self._line(d, [(anchor_x, 0), (hand_x, hand_y)], self.WEB_AURA, width=3.5)
        self._line(d, [(anchor_x, 0), (hand_x, hand_y)], self.WEB_SILK, width=1.6)
        # Ceiling spark
        self._cir(d, anchor_x, 2, 4.0, (255, 255, 255, 240))

        # Dynamic tucked swinging legs
        by = 82
        self._ell(d, cx - 12, by + 22, 8, 16, self.SUIT_BLUE)
        self._ell(d, cx - 8, by + 34, 8, 10, self.SUIT_RED)
        self._ell(d, cx + 14, by + 18, 8, 18, self.SUIT_BLUE)
        self._ell(d, cx + 18, by + 30, 8, 10, self.SUIT_RED)

        # Torso in mid-air arch
        self._ell(d, cx, by, 22, 18, self.SUIT_BLUE)
        self._pol(d, [
            (cx - 15, by - 12),
            (cx + 15, by - 12),
            (cx + 12, by + 12),
            (cx - 12, by + 12)
        ], self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.1)
        self._draw_spider_emblem(d, cx, by, scale=1.0)

        # Web clutch arm reaching straight up to hand_x, hand_y
        self._line(d, [(cx + 10, by - 10), (hand_x, hand_y)], self.SUIT_RED, width=4.5)
        self._cir(d, hand_x, hand_y, 4.8, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1)

        # Free arm extended forward
        self._line(d, [(cx - 12, by - 8), (cx - 28, by - 2)], self.SUIT_RED, width=4.0)
        self._cir(d, cx - 28, by - 2, 4.2, self.SUIT_RED)

        # Head tilted into the wind
        hy = 48
        self._ell(d, cx, hy, 23, 25, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.2)
        self._draw_web_grid(d, cx, hy, 23, 25)

        self._draw_mask_lens(d, cx - 10, hy, side=-1, squint=0.2)
        self._draw_mask_lens(d, cx + 10, hy, side=1, squint=0.2)

        return self._render(img)

    # ── POSE: WALL CRAWL ────────────────────────────────────
    def draw_wall_crawl(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 80
        crawl_bob = math.sin(frame * 0.45) * 3.5

        # Wall edge line
        wall_x = 14 if self.direction == -1 else 146
        self._line(d, [(wall_x, 10), (wall_x, 140)], (255, 255, 255, 180), width=2.0)

        # Wall suction sticky points
        for wy in [35, 65, 95, 125]:
            self._cir(d, wall_x, wy, 3.8, (255, 255, 255, 220))

        # Splayed limbs clinging to wall
        by = 78 + crawl_bob
        self._ell(d, cx, by, 22, 20, self.SUIT_BLUE)
        self._pol(d, [(cx - 14, by - 12), (cx + 14, by - 12), (cx + 10, by + 12), (cx - 10, by + 12)], self.SUIT_RED)
        self._draw_spider_emblem(d, cx, by, scale=0.95)

        # Splayed arms reaching for wall
        reach_x = wall_x
        self._line(d, [(cx, by - 8), (reach_x, by - 26)], self.SUIT_RED, width=3.8)
        self._line(d, [(cx, by + 6), (reach_x, by + 26)], self.SUIT_RED, width=3.8)

        # Mask rotated against wall
        hy = 46 + crawl_bob
        self._ell(d, cx, hy, 23, 24, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.2)
        self._draw_web_grid(d, cx, hy, 23, 24)
        self._draw_mask_lens(d, cx - 9, hy, side=-1, squint=0.3)
        self._draw_mask_lens(d, cx + 9, hy, side=1, squint=0.3)

        return self._render(img)

    # ── POSE: THWIP WEB BLAST ───────────────────────────────
    def draw_thwip(self, frame):
        img = self._new(); d = ImageDraw.Draw(img); cx = 72
        by = 82
        self._ground_shadow(d, cx, 136, 40, 8)

        # Lower body
        self._ell(d, cx - 18, 110, 7, 18, self.SUIT_BLUE)
        self._ell(d, cx - 19, 126, 8, 10, self.SUIT_RED)
        self._ell(d, cx + 18, 110, 7, 18, self.SUIT_BLUE)
        self._ell(d, cx + 19, 126, 8, 10, self.SUIT_RED)

        # Torso
        self._ell(d, cx, by + 4, 22, 18, self.SUIT_BLUE)
        self._pol(d, [(cx - 16, by - 12), (cx + 16, by - 12), (cx + 12, by + 12), (cx - 12, by + 12)], self.SUIT_RED)
        self._draw_spider_emblem(d, cx, by, scale=1.0)

        # Head
        hy = 48
        self._ell(d, cx, hy, 23, 26, self.SUIT_RED, outline=self.SUIT_RED_DK, width=1.2)
        self._draw_web_grid(d, cx, hy, 23, 26)
        self._draw_mask_lens(d, cx - 10, hy, side=-1, squint=0.45)
        self._draw_mask_lens(d, cx + 10, hy, side=1, squint=0.45)

        # Extended firing arm
        wrist_x = cx + 32
        wrist_y = by - 2
        self._line(d, [(cx + 12, by - 4), (wrist_x, wrist_y)], self.SUIT_RED, width=4.5)
        # Web shooter wrist gauntlet
        self._cir(d, wrist_x, wrist_y, 4.2, (190, 195, 205, 255))

        # Thwip Web projectile lines shooting out
        tip_x = wrist_x + 48
        tip_y = wrist_y - 6
        self._line(d, [(wrist_x, wrist_y), (tip_x, tip_y)], self.WEB_SILK, width=2.4)
        self._line(d, [(wrist_x, wrist_y), (tip_x, tip_y + 14)], self.WEB_SILK, width=1.6)
        self._line(d, [(wrist_x, wrist_y), (tip_x - 10, tip_y - 14)], self.WEB_SILK, width=1.6)

        # Expanding web net rings
        self._arc(d, tip_x, tip_y, 16, 16, 0, 360, self.WEB_SILK, width=2.0)
        self._arc(d, tip_x, tip_y, 24, 24, 0, 360, self.WEB_AURA, width=1.4)

        # Comic THWIP! text burst
        d.text((self._mx(tip_x - 14), self._my(tip_y - 24)), "THWIP!", fill=(255, 235, 50, 255))

        return self._render(img)

# ══════════════════════════════════════════════════════════════════════
#  SHADOW SOLDIER RENDERER (Beru & Igris + Real Particle Engine)
# ══════════════════════════════════════════════════════════════════════

class UniversalCompanionRenderer:
    """
    Renders all five companions with their respective art styles & physics:
    - Beru: Ant Carapace, Translucent Fluttering Wings, Cyan Soulfire, Shadow Smoke
    - Igris: Crimson Plate Armor, Flowing Red Plume, Crimson Soulfire, Greatsword
    - Cat: Pointy Ears, Whiskers, Emerald Eyes, Purring Hearts
    - Spiderman: Red & Blue suit, Web Swinging, Screen Wall Crawl, Thwip!
    - Puppy: 4x Supersampled cute golden pup from desktop_puppy.pyw
    """
    def __init__(self, char_name="Beru", w=110, h=105, tcolor="#FF00FF"):
        self.char_name = char_name
        self.w, self.h = w, h
        self.tcolor = tcolor
        self.direction = 1
        self.base_dir = os.path.join(os.path.dirname(__file__), "assets", "shadow_soldiers")
        self.puppy_renderer = PuppyRenderer(w, h, tcolor) if PuppyRenderer else None
        self.cat_renderer = CuteCatRenderer(w, h, tcolor)
        self.spidey_renderer = SpidermanRenderer(w, h, tcolor)
        self.bg_particles = []
        self.fg_embers = []
        self._load_sprites()

    def _load_sprites(self):
        self.sprites = {}
        for cname, fname in [("Beru", "beru_hq.png"), ("Igris", "igris_hq.png")]:
            p = os.path.join(self.base_dir, fname)
            if os.path.exists(p):
                try: self.sprites[cname] = Image.open(p).convert("RGBA")
                except Exception: pass

    def set_character(self, char_name):
        self.char_name = char_name
        self.bg_particles.clear()
        self.fg_embers.clear()
        if self.puppy_renderer: self.puppy_renderer.direction = self.direction
        self.cat_renderer.direction = self.direction
        self.spidey_renderer.direction = self.direction

    def set_size(self, w, h):
        self.w, self.h = w, h
        if self.puppy_renderer: self.puppy_renderer.set_size(w, h)
        self.cat_renderer.set_size(w, h)
        self.spidey_renderer.set_size(w, h)

    def render(self, frame=0, emotion="idle", flight_tilt=0.0, is_active=False, is_moving=False, is_wall_crawling=False, walk_cycle=0.0, is_grounded=True, landing_squash=0.0):
        # 1. Puppy
        if self.char_name == "Puppy" and self.puppy_renderer:
            self.puppy_renderer.direction = self.direction
            if emotion in ("happy", "praise"):
                return self.puppy_renderer.draw_wag(frame)
            elif is_moving:
                return self.puppy_renderer.draw_walk(frame)
            elif emotion == "sleeping":
                return self.puppy_renderer.draw_sleep(frame)
            else:
                return self.puppy_renderer.draw_sit(frame)

        # 2. Cute Cat
        if self.char_name == "Cat":
            self.cat_renderer.direction = self.direction
            if emotion in ("happy", "praise"):
                return self.cat_renderer.draw_purr(frame)
            elif is_moving:
                return self.cat_renderer.draw_walk(frame, walk_cycle=walk_cycle)
            else:
                return self.cat_renderer.draw_sit(frame, landing_squash=landing_squash)

        # 3. Spider-Man
        if self.char_name == "Spiderman":
            self.spidey_renderer.direction = self.direction
            if emotion in ("happy", "praise", "thwip"):
                return self.spidey_renderer.draw_thwip(frame)
            elif is_wall_crawling:
                return self.spidey_renderer.draw_wall_crawl(frame)
            elif is_moving:
                if is_grounded:
                    return self.spidey_renderer.draw_dash(frame, walk_cycle=walk_cycle)
                else:
                    return self.spidey_renderer.draw_web_swing(frame, flight_tilt)
            else:
                return self.spidey_renderer.draw_idle(frame, landing_squash=landing_squash)

        # 4. Beru & Igris (Solo Leveling Shadow Soldiers with Particle Smoke)
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        cx = self.w // 2
        cy = self.h // 2 + 4

        if self.char_name == "Beru":
            hover_y = (math.sin(frame * 0.28) * 3.5 + math.sin(frame * 0.52) * 1.5) if emotion in ("idle", "fly") else 0.0
        else:
            hover_y = math.sin(frame * 0.38) * 2.0 if emotion in ("idle", "fly") else 0.0

        # Background Shadow Smoke Wisps
        spawn_rate = 2 if is_active else 1
        for _ in range(spawn_rate):
            if len(self.bg_particles) < 24:
                self.bg_particles.append({
                    'x': cx + random.uniform(-22, 22),
                    'y': cy + 24 + random.uniform(-4, 8),
                    'vx': random.uniform(-0.5, 0.5),
                    'vy': random.uniform(-2.2, -1.0) * (1.3 if is_active else 1.0),
                    'size': random.uniform(4.5, 8.0),
                    'life': 1.0,
                    'decay': random.uniform(0.04, 0.07)
                })

        for p in self.bg_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['size'] += 0.35
            p['life'] -= p['decay']
            if p['life'] <= 0:
                self.bg_particles.remove(p)
                continue
            alpha = int(p['life'] * (140 if is_active else 85))
            r = int(p['size'])
            smoke_color = (18, 8, 30, alpha) if self.char_name == "Beru" else (30, 8, 16, alpha)
            d.ellipse([p['x'] - r, p['y'] - r, p['x'] + r, p['y'] + r], fill=smoke_color)

        # Base Sprite
        base = self.sprites.get(self.char_name)
        if base:
            sq_x = 1.0 + landing_squash * 0.30
            sq_y = 1.0 - landing_squash * 0.22
            target_w = int(self.w * 0.84 * sq_x)
            target_h = int(self.h * 0.88 * sq_y)
            sprite_scaled = base.resize((target_w, target_h), Image.LANCZOS)
            if self.direction == -1:
                sprite_scaled = sprite_scaled.transpose(Image.FLIP_LEFT_RIGHT)
            if abs(flight_tilt) > 0.01:
                sprite_scaled = sprite_scaled.rotate(flight_tilt, resample=Image.BICUBIC, expand=False)
            sx = (self.w - target_w) // 2
            sy = int((self.h - target_h) // 2 + hover_y + int(landing_squash * 4))
            canvas.alpha_composite(sprite_scaled, (sx, sy))

        # Foreground Soulfire Embers
        if len(self.fg_embers) < 18:
            self.fg_embers.append({
                'x': cx + random.uniform(-20, 20),
                'y': cy + 18 + random.uniform(-5, 5),
                'vx': random.uniform(-0.4, 0.4),
                'vy': random.uniform(-2.8, -1.2) * (1.4 if is_active else 1.0),
                'size': random.uniform(1.6, 3.2),
                'life': 1.0,
                'decay': random.uniform(0.04, 0.08)
            })

        for em in self.fg_embers[:]:
            em['x'] += em['vx']
            em['y'] += em['vy']
            em['life'] -= em['decay']
            if em['life'] <= 0:
                self.fg_embers.remove(em)
                continue
            alpha = int(em['life'] * (240 if is_active else 170))
            er = em['size']
            ec = (0, 240, 255, alpha) if self.char_name == "Beru" else (255, 45, 75, alpha)
            d.ellipse([em['x'] - er, em['y'] - er, em['x'] + er, em['y'] + er], fill=ec)

        # Emotional Overlays
        if emotion == "crying":  # Tears of Devotion
            tear_y = (frame * 3) % 20
            d.line([cx - 10, cy - 6 + tear_y, cx - 10, cy + 4 + tear_y], fill=(0, 240, 255, 230), width=2)
            d.line([cx + 10, cy - 6 + tear_y, cx + 10, cy + 4 + tear_y], fill=(0, 240, 255, 230), width=2)
            d.text((cx - 16, cy - 32), "♡", fill=(255, 105, 180, 255), font=None)
        elif emotion == "bow":  # Royal Fealty Crown
            d.polygon([(cx - 12, cy - 32), (cx - 16, cy - 42), (cx - 6, cy - 36),
                       (cx, cy - 44), (cx + 6, cy - 36), (cx + 16, cy - 42),
                       (cx + 12, cy - 32)], fill=(255, 215, 0, 240))

        return self._composite_chroma(canvas)

    def _composite_chroma(self, img_rgba):
        tc = self.tcolor.lstrip('#')
        rt, gt, bt = tuple(int(tc[i:i+2], 16) for i in (0, 2, 4))
        bg = Image.new("RGBA", (self.w, self.h), (rt, gt, bt, 255))
        alpha = img_rgba.split()[-1]
        clean_mask = alpha.point(lambda p: 255 if p >= 50 else 0)
        final = Image.composite(img_rgba.convert("RGB"), bg.convert("RGB"), clean_mask)
        return ImageTk.PhotoImage(final)

# ══════════════════════════════════════════════════════════════════════
#  JIGGLER AUTOMATION ENGINE
# ══════════════════════════════════════════════════════════════════════

class JigglerEngine:
    """Background stealth automation thread."""
    def __init__(self, callback_active=None):
        self.active = False
        self.running = True
        self.thread = None
        self.stop_event = threading.Event()
        self.callback_active = callback_active

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def toggle(self):
        self.active = not self.active
        if self.active:
            prevent_sleep()
        else:
            allow_sleep()
        if self.callback_active:
            self.callback_active(self.active)
        return self.active

    def _run(self):
        while self.running:
            if self.active:
                try:
                    mode = random.choice(["bezier", "key", "micro"])
                    if mode == "bezier":
                        dx = random.randint(-18, 18)
                        dy = random.randint(-18, 18)
                        human_bezier_motion(dx, dy, steps=random.randint(14, 22))
                    elif mode == "key":
                        send_hardware_key(0x8E)
                    elif mode == "micro":
                        send_relative_mouse(1, 1)
                        time.sleep(0.02)
                        send_relative_mouse(-1, -1)
                except Exception:
                    pass
                sleep_time = random.uniform(15.0, 32.0)
            else:
                sleep_time = 1.0

            slept = 0.0
            while slept < sleep_time and self.running:
                time.sleep(0.2)
                slept += 0.2

    def stop(self):
        self.running = False
        self.active = False
        allow_sleep()

# ══════════════════════════════════════════════════════════════════════
#  MAIN DESKTOP COMPANION APPLICATION
# ══════════════════════════════════════════════════════════════════════

HOTKEY_TOGGLE  = 101
HOTKEY_HIDE    = 102
HOTKEY_GRAVITY = 103
HOTKEY_SIT     = 104
MOD_CONTROL    = 0x0002
MOD_SHIFT      = 0x0004

class DesktopCompanionApp:
    SIZES = {
        "Tiny":   (80, 74),
        "Small":  (96, 90),
        "Medium": (118, 110),
        "Large":  (142, 132),
    }

    QUOTES = {
        "Beru": [
            "My king! 👑",
            "You are the best! ✨",
            "Nothing can stop you, My King! ⚡",
            "You will conquer today, Sovereign! ⚔️",
            "Your code is magnificent, My King! 💎",
            "Shall I eliminate this bug, My King?! 🩸"
        ],
        "Igris": [
            "For the Sovereign! 🗡️",
            "My blade is yours, My King! 👑",
            "A Knight's honor for the Monarch! 🛡️",
            "Victory awaits you, Sovereign! ⚡",
            "Stay strong, My King! ⚔️",
            "I shall stand guard, My King! 🛡️"
        ],
        "Cat": [
            "Meow! Love you, human! 🐾♡",
            "Purrrrr... you're doing awesome! 🧶✨",
            "*rubs against your screen* ♡🐱",
            "*bats paw at your cursor* 🐾",
            "You are purr-fect! 🐾⭐"
        ],
        "Spiderman": [
            "Your friendly neighborhood Spider-Man! 🕷️✨",
            "With great power comes great responsibility! 🕸️",
            "Thwip! Webbed up your bugs, boss! 🕸️💻",
            "Hang in there, champion! You've got this! 🕷️💪",
            "Just swinging by to see greatness in action! 🕸️⚡"
        ],
        "Puppy": [
            "*wags happily* ♡🐾",
            "Woof! Love you! 🐶✨",
            "You're the best human! 💖",
            "Good boy loves you! 🦴",
            "You're doing awesome! 🌟"
        ]
    }

    REMINDERS = {
        "water": {
            "Beru": "Drink water, My King! Your mortal vessel must be replenished! 💧👑",
            "Igris": "Replenish your mana, Sovereign! A Knight must stay hydrated! 💧🛡️",
            "Cat": "Meow! Time for fresh water, human! Stay hydrated! 💧🐾",
            "Spiderman": "Hydrate that super-hero vessel, web-head! Drink water! 💧🕷️",
            "Puppy": "*brings a water bowl* Woof! Drink some water, human! 💧🐾"
        },
        "posture": {
            "Beru": "Straighten your back, My King! A Monarch bows to no one! 🧘👑",
            "Igris": "Upright posture, Sovereign! Maintain the battle stance! ⚔️🛡️",
            "Cat": "Arch your back and stretch like a kitty, meow! 🧘🐱",
            "Spiderman": "Straighten that spine! Even Spidey needs good posture! 🧘🕸️",
            "Puppy": "*does a cute play-bow* Woof! Time to stretch our paws! 🧘🐕"
        },
        "eye": {
            "Beru": "Rest your supreme eyes, Sovereign! Look into the distance! 👀⚡",
            "Igris": "Shield your vision, My King! Rest your eyes for 20 seconds! 🛡️👀",
            "Cat": "Slow blink at the distance! Rest your eyes, meow! 👀✨",
            "Spiderman": "Rest those peepers for 20 seconds! Spider-Sense tingling! 👀✨",
            "Puppy": "*blinks gently* Look far away and rest your eyes! 👀✨"
        },
        "walk": {
            "Beru": "Take a short walk, My King! Survey your domain! 🚶👑",
            "Igris": "Patrol the perimeter, Sovereign! Stretch your legs! 🚶🛡️",
            "Cat": "Let's take a graceful prowl around the room, meow! 🐾🐱",
            "Spiderman": "Stretch those legs! Even Spidey takes a roof stroll! 🚶🕷️",
            "Puppy": "*spins in happy circles* Let's take a quick walk! 🐾🐕"
        },
        "coffee": {
            "Beru": "Allow yourself a moment of rest, My King! ☕👑",
            "Igris": "A tactical breather for the Sovereign! ☕🛡️",
            "Cat": "Curled up break time! Purrrrr... ☕🧶",
            "Spiderman": "Take five, champ! Grab a snack or coffee! ☕🍕",
            "Puppy": "*nuzzles your hand gently* Time for a quick break! ☕🐾"
        }
    }

    def __init__(self, default_char=None):
        self.state_file = os.path.join(os.path.dirname(__file__), "deskpet_state.json")
        self.saved_state = self._load_state()

        self.current_char = default_char or self.saved_state.get("character", "Beru")
        self.size_name = self.saved_state.get("size_name", "Small")
        self.pet_w, self.pet_h = self.SIZES.get(self.size_name, self.SIZES["Small"])
        self.show_bubbles = self.saved_state.get("show_bubbles", True)
        self.reminders_enabled = self.saved_state.get("reminders_enabled", True)
        self.reminder_interval_mins = self.saved_state.get("reminder_interval_mins", 30)

        # Floor Gravity & Sit Silently Modes
        self.gravity_enabled = self.saved_state.get("gravity_enabled", True)
        self.sit_silently = self.saved_state.get("sit_silently", False)

        # Tkinter Setup
        self.root = tk.Tk()
        self.root.title("Desktop Companion")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.tcolor = "#FF00FF"
        self.root.attributes("-transparentcolor", self.tcolor)
        self.root.configure(bg=self.tcolor)

        self.bubble_space = 56
        self.win_w = max(280, self.pet_w + 140)
        self.win_h = self.pet_h + self.bubble_space

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        default_ground_y = max(40, sh - self.win_h - 45)
        self.x = self.saved_state.get("x", sw - self.win_w - 70)
        self.y = self.saved_state.get("y", default_ground_y if self.gravity_enabled else (sh - self.win_h - 110))
        self.pos_x = float(self.x)
        self.pos_y = float(self.y)
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.x}+{self.y}")

        self.canvas = tk.Canvas(self.root, width=self.win_w, height=self.win_h,
                                bg=self.tcolor, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Physics & Animation State
        self.frame = 0
        self.emotion = "idle"
        self.state_timer = 0
        self.target_x = float(self.x)
        self.target_y = float(self.y)
        self.vx = 0.0
        self.vy = 0.0
        self.walk_cycle = 0.0
        self.landing_squash = 0.0
        self.is_grounded = False
        self.flight_tilt = 0.0
        self.bubble_text = None
        self.bubble_timer = 0
        self.visible = True
        self.is_wall_crawling = False
        self.dust_particles = []

        self.reminder_counter = 0

        # Mouse Dragging
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_release)
        self.canvas.bind("<Double-Button-1>", self._on_double_click)
        self.canvas.bind("<Button-3>", self._on_right_click)

        # Renderer & Jiggler
        self.renderer = UniversalCompanionRenderer(self.current_char, self.pet_w, self.pet_h, self.tcolor)
        self.jiggler = JigglerEngine(callback_active=self._on_jiggler_toggle)
        self.jiggler.start()

        self.context_menu = None

        # Load Application Icons (PNG & ICO)
        self.icon_path_ico = os.path.join(os.path.dirname(__file__), "assets", "app_icon.ico")
        self.icon_path_png = os.path.join(os.path.dirname(__file__), "assets", "app_icon.png")
        self.menu_header_icon = None
        if os.path.exists(self.icon_path_ico):
            try:
                self.root.iconbitmap(self.icon_path_ico)
            except Exception:
                pass
        if os.path.exists(self.icon_path_png):
            try:
                self._app_icon_photo = ImageTk.PhotoImage(Image.open(self.icon_path_png).resize((64, 64), Image.LANCZOS))
                self.root.iconphoto(True, self._app_icon_photo)
                self.menu_header_icon = ImageTk.PhotoImage(Image.open(self.icon_path_png).resize((22, 22), Image.LANCZOS))
            except Exception:
                pass

        self._setup_hotkeys()
        self._setup_tray()
        
        intro_msg = f"{self.current_char} is ready, My King! 👑" if self.current_char in ("Beru", "Igris") else \
                    ("Meow! I'm here! 🐾" if self.current_char == "Cat" else \
                    ("Your friendly neighborhood Spider-Man is here! 🕷️" if self.current_char == "Spiderman" else "Woof! I'm here! 🐾"))
        self.say(intro_msg, 45)

        self.root.after(40, self._tick)

    def _load_state(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_state(self):
        self.saved_state.update({
            "character": self.current_char,
            "size_name": self.size_name,
            "show_bubbles": self.show_bubbles,
            "reminders_enabled": self.reminders_enabled,
            "reminder_interval_mins": self.reminder_interval_mins,
            "gravity_enabled": self.gravity_enabled,
            "sit_silently": self.sit_silently,
            "x": self.x,
            "y": self.y
        })
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.saved_state, f, indent=2)
        except Exception:
            pass

    def switch_character(self, char_name):
        if char_name == self.current_char:
            return
        self.current_char = char_name
        self.renderer.set_character(char_name)
        self._save_state()
        self._update_tray()

        if char_name == "Beru":
            self.say("I am at your command, My King! 🐜👑", 45)
        elif char_name == "Igris":
            self.say("My blade is sworn to you, Sovereign! 🗡️👑", 45)
        elif char_name == "Cat":
            self.say("Meow! Ready to purr by your side! 🐾🐱", 45)
        elif char_name == "Spiderman":
            self.say("Thwip! Spider-Man swinging into action! 🕷️🕸️", 45)
        elif char_name == "Puppy":
            self.say("Woof! Happy to see you! 🐶🐾", 45)

    def set_size_mode(self, size_name):
        if size_name not in self.SIZES:
            return
        self.size_name = size_name
        self.pet_w, self.pet_h = self.SIZES[size_name]
        self.win_w = max(280, self.pet_w + 140)
        self.win_h = self.pet_h + self.bubble_space
        self.renderer.set_size(self.pet_w, self.pet_h)
        self.canvas.config(width=self.win_w, height=self.win_h)
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.x}+{self.y}")
        self._save_state()
        self.say(f"Size: {size_name} 📏", 30)

    def set_reminder_interval(self, mins):
        self.reminder_interval_mins = mins
        self.reminder_counter = 0
        self._save_state()
        self.say(f"Reminders: Every {mins}m ⏱️", 35)

    def toggle_gravity(self):
        self.gravity_enabled = not self.gravity_enabled
        self._save_state()
        self._update_tray()
        if self.gravity_enabled:
            self.say("Floor Gravity ON! 🌍 Roaming bottom", 40)
        else:
            self.say("Floor Gravity OFF! 🕊️ Free Roam", 40)

    def toggle_sit_silently(self):
        self.sit_silently = not self.sit_silently
        if self.sit_silently:
            self.target_x = self.pos_x
            self.target_y = self.pos_y
            self.vx = 0.0
            self.vy = 0.0
            self.say("Sitting silently! 🪑 Staying right here", 45)
        else:
            self.say("Roaming active! 🐾", 35)
        self._save_state()
        self._update_tray()

    def toggle_jiggler(self):
        state = self.jiggler.toggle()
        msg = ("Domain Active! ⚡" if self.current_char in ("Beru", "Igris") else \
               ("Spidey Vigilance Active! 🕷️" if self.current_char == "Spiderman" else "Awake Mode ON! ⚡")) if state else "Resting ~ 💤"
        self.say(msg, 35)

    def _on_jiggler_toggle(self, active):
        self._update_tray()

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.root.deiconify()
        else:
            self.root.withdraw()
        self._update_tray()

    def say(self, text, duration=45):
        if not self.show_bubbles:
            return
        self.bubble_text = text
        self.bubble_timer = duration

    def trigger_reminder(self, key):
        rem_dict = self.REMINDERS.get(key, {})
        msg = rem_dict.get(self.current_char, "Take care of yourself! ✨")
        if self.current_char == "Beru":
            self.emotion = "fly"
        elif self.current_char == "Igris":
            self.emotion = "bow"
        elif self.current_char == "Cat":
            self.emotion = "happy"
        elif self.current_char == "Spiderman":
            self.emotion = "thwip"
        else:
            self.emotion = "happy"
        self.state_timer = 55
        self.say(msg, duration=60)

    def toggle_reminders(self):
        self.reminders_enabled = not self.reminders_enabled
        self._save_state()
        status_msg = "Reminders ON! ⏰" if self.reminders_enabled else "Reminders Muted 🔕"
        self.say(status_msg, 35)

    def _praise(self):
        if self.current_char == "Beru":
            self.emotion = "crying"
            quotes = [
                "MY KING HAS TOUCHED ME!! 😭👑",
                "TEARS OF DEVOTION, SOVEREIGN! 😭✨",
                "MY LIFE IS YOURS, MY KING! 🐜👑",
                "THE GREATEST MONARCH OF ALL! 👑💎"
            ]
        elif self.current_char == "Igris":
            self.emotion = "bow"
            quotes = [
                "My blade is sworn to you, My King! 🗡️👑",
                "A Knight's honor for the Sovereign! 🛡️✨",
                "I shall conquer your enemies, My King! ⚡",
                "Always by your side, Sovereign! 👑"
            ]
        elif self.current_char == "Cat":
            self.emotion = "happy"
            quotes = [
                "Purrrrrr... *happy cat cheek rubs* 🐾♡",
                "Meow! You are my favorite human! 🐱✨",
                "*slow blinks with love* Purrr... 🧶💖",
                "*bats paw affectionately* Meow! 🐾"
            ]
        elif self.current_char == "Spiderman":
            self.emotion = "thwip"
            quotes = [
                "Thwip! Thanks, buddy! Spidey's got your back! 🕷️✨",
                "Hey, with great power comes great teamwork! 🕸️👊",
                "Thwip! Web high-five! 🕸️✋",
                "Your friendly neighborhood superhero! 🕷️🌟"
            ]
        else:
            self.emotion = "happy"
            quotes = [
                "*wags tail happily* ♡🐾",
                "Woof! Love you so much! 🐶✨",
                "You're the best human ever! 🦴💖",
                "*happy puppy barks* 🐶🎵"
            ]
        self.state_timer = 50
        self.say(random.choice(quotes), duration=50)

    def _on_left_click(self, e):
        self.drag_start_x = e.x_root - self.x
        self.drag_start_y = e.y_root - self.y
        self.is_dragging = False
        self._praise()

    def _on_drag(self, e):
        self.is_dragging = True
        self.x = e.x_root - self.drag_start_x
        self.y = e.y_root - self.drag_start_y
        self.pos_x = float(self.x)
        self.pos_y = float(self.y)
        self.target_x = float(self.x)
        self.target_y = float(self.y)
        self.vx = 0.0
        self.vy = 0.0
        self.root.geometry(f"+{self.x}+{self.y}")

    def _on_drag_release(self, e):
        if self.is_dragging:
            self._save_state()
            if self.sit_silently:
                self.say("Sitting here! 🪑", 30)

    def _on_double_click(self, e):
        self.target_x = float(e.x_root - self.win_w // 2)
        self.target_y = float(e.y_root - self.win_h // 2)
        call_msg = "Coming, My King! ⚡" if self.current_char in ("Beru", "Igris") else \
                   ("Thwip! Swinging over! 🕸️" if self.current_char == "Spiderman" else \
                   ("Prowling over, meow! 🐾" if self.current_char == "Cat" else "Coming! 🐾"))
        self.say(call_msg, 35)

    # ══════════════════════════════════════════════════════════════════
    #  WINDOWS 10 LIGHT CONTEXT MENU BUILDER
    # ══════════════════════════════════════════════════════════════════

    def _on_right_click(self, e):
        if self.context_menu:
            self.context_menu.dismiss_all()
            self.context_menu = None

        is_awake = self.jiggler.active
        awake_lbl = "Deactivate Domain" if (is_awake and self.current_char in ("Beru", "Igris")) else \
                    "Activate Domain" if self.current_char in ("Beru", "Igris") else \
                    "Turn Off Vigilance" if (is_awake and self.current_char == "Spiderman") else \
                    "Activate Vigilance" if self.current_char == "Spiderman" else \
                    "Turn Off Awake" if is_awake else "Turn On Awake"

        menu_items = [
            {
                "type": "header",
                "title": "👑 DESKTOP COMPANION",
                "subtitle": f"{self.current_char} • {'● AWAKE' if is_awake else '○ SLEEP'}",
                "icon_img": self.menu_header_icon
            },
            {
                "icon": "⚡",
                "label": awake_lbl,
                "shortcut": "Ctrl+B",
                "command": self.toggle_jiggler
            },
            {
                "icon": "👑" if self.current_char in ("Beru", "Igris") else ("🕷️" if self.current_char == "Spiderman" else "🐾"),
                "label": "Praise Companion" if self.current_char in ("Beru", "Igris") else ("High-Five Spidey" if self.current_char == "Spiderman" else "Pet Companion"),
                "command": self._praise
            },
            {"type": "separator"},
            {
                "icon": "🌍",
                "label": "Floor Gravity (Bottom Roam)",
                "shortcut": "Ctrl+G",
                "checked": self.gravity_enabled,
                "command": self.toggle_gravity
            },
            {
                "icon": "🪑",
                "label": "Sit Silently (Stay in Place)",
                "shortcut": "Ctrl+S",
                "checked": self.sit_silently,
                "command": self.toggle_sit_silently
            },
            {"type": "separator"},
            {
                "icon": "⏰",
                "label": "Remind Me / Care",
                "submenu": [
                    {
                        "icon": "⏱️",
                        "label": "Reminder Timing",
                        "submenu": [
                            {
                                "icon": "⚡",
                                "label": "Every 15 Minutes",
                                "checked": (self.reminder_interval_mins == 15),
                                "command": lambda: self.set_reminder_interval(15)
                            },
                            {
                                "icon": "⏱️",
                                "label": "Every 30 Minutes (Default)",
                                "checked": (self.reminder_interval_mins == 30),
                                "command": lambda: self.set_reminder_interval(30)
                            },
                            {
                                "icon": "⏳",
                                "label": "Every 45 Minutes",
                                "checked": (self.reminder_interval_mins == 45),
                                "command": lambda: self.set_reminder_interval(45)
                            },
                            {
                                "icon": "🕐",
                                "label": "Every 60 Minutes",
                                "checked": (self.reminder_interval_mins == 60),
                                "command": lambda: self.set_reminder_interval(60)
                            }
                        ]
                    },
                    {"type": "separator"},
                    {
                        "icon": "💧",
                        "label": "Drink Water Break",
                        "command": lambda: self.trigger_reminder("water")
                    },
                    {
                        "icon": "🧘",
                        "label": "Posture & Stretch Check",
                        "command": lambda: self.trigger_reminder("posture")
                    },
                    {
                        "icon": "👀",
                        "label": "20-20-20 Eye Relief",
                        "command": lambda: self.trigger_reminder("eye")
                    },
                    {
                        "icon": "🚶",
                        "label": "Stand Up & Walk",
                        "command": lambda: self.trigger_reminder("walk")
                    },
                    {
                        "icon": "☕",
                        "label": "Quick Rest / Coffee Break",
                        "command": lambda: self.trigger_reminder("coffee")
                    },
                    {"type": "separator"},
                    {
                        "icon": "🔔",
                        "label": "Auto-Reminders Active",
                        "checked": self.reminders_enabled,
                        "command": self.toggle_reminders
                    }
                ]
            },
            {
                "icon": "👤",
                "label": "Switch Companion",
                "submenu": [
                    {
                        "icon": "🐜",
                        "label": "Shadow Marshal Beru",
                        "checked": (self.current_char == "Beru"),
                        "command": lambda: self.switch_character("Beru")
                    },
                    {
                        "icon": "🗡️",
                        "label": "Blood-Red Commander Igris",
                        "checked": (self.current_char == "Igris"),
                        "command": lambda: self.switch_character("Igris")
                    },
                    {
                        "icon": "🐱",
                        "label": "Cute Calico Cat",
                        "checked": (self.current_char == "Cat"),
                        "command": lambda: self.switch_character("Cat")
                    },
                    {
                        "icon": "🕷️",
                        "label": "The Amazing Spider-Man",
                        "checked": (self.current_char == "Spiderman"),
                        "command": lambda: self.switch_character("Spiderman")
                    },
                    {
                        "icon": "🐶",
                        "label": "Cute Golden Puppy",
                        "checked": (self.current_char == "Puppy"),
                        "command": lambda: self.switch_character("Puppy")
                    },
                ]
            },
            {
                "icon": "📏",
                "label": "Companion Size",
                "submenu": [
                    {
                        "icon": "▫️",
                        "label": "Tiny",
                        "checked": (self.size_name == "Tiny"),
                        "command": lambda: self.set_size_mode("Tiny")
                    },
                    {
                        "icon": "▪️",
                        "label": "Small (Default)",
                        "checked": (self.size_name == "Small"),
                        "command": lambda: self.set_size_mode("Small")
                    },
                    {
                        "icon": "◽",
                        "label": "Medium",
                        "checked": (self.size_name == "Medium"),
                        "command": lambda: self.set_size_mode("Medium")
                    },
                    {
                        "icon": "◻️",
                        "label": "Large",
                        "checked": (self.size_name == "Large"),
                        "command": lambda: self.set_size_mode("Large")
                    },
                ]
            },
            {
                "icon": "💬",
                "label": "Speech Bubbles",
                "checked": self.show_bubbles,
                "command": self._toggle_bubbles
            },
            {"type": "separator"},
            {
                "icon": "👁️",
                "label": "Hide Companion",
                "shortcut": "Ctrl+Shift+Q",
                "command": self.toggle_visibility
            },
            {
                "icon": "❌",
                "label": "Dismiss Application",
                "command": self.quit_app
            }
        ]

        self.context_menu = Win10LightContextMenu(self.root, menu_items)
        self.context_menu.show(e.x_root, e.y_root)

    def _toggle_bubbles(self):
        self.show_bubbles = not self.show_bubbles
        self._save_state()
        if self.show_bubbles:
            self.say("Comments ON! 💬", 30)
        else:
            self.bubble_text = None

    # ══════════════════════════════════════════════════════════════════
    #  PHYSICS & MAIN LOOP (Real Object Motion, Gravity & Sit Silently)
    # ══════════════════════════════════════════════════════════════════

    def _tick(self):
        self.frame += 1

        if self.state_timer > 0:
            self.state_timer -= 1
            if self.state_timer == 0:
                self.emotion = "idle"

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        taskbar_h = 45
        ground_y = max(40, sh - self.win_h - taskbar_h)

        # Update dust puff particles
        for p in self.dust_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['size'] += 0.18
            p['life'] -= p['decay']
            if p['life'] <= 0:
                self.dust_particles.remove(p)

        # -------------------------------------------------------------
        # 1. Sit Silently Mode (Stationary in place, zero wandering)
        # -------------------------------------------------------------
        if self.sit_silently:
            self.vx *= 0.3
            self.vy *= 0.3
            if abs(self.vx) < 0.05: self.vx = 0.0
            if abs(self.vy) < 0.05: self.vy = 0.0
            self.flight_tilt *= 0.8
            self.target_x = self.pos_x
            self.target_y = self.pos_y

        # -------------------------------------------------------------
        # 2. Floor Gravity & Real Movement Physics
        # -------------------------------------------------------------
        else:
            # Spider-Man Edge Crawl Physics Check (if gravity is off and near edge)
            self.is_wall_crawling = False
            if self.current_char == "Spiderman" and not self.gravity_enabled:
                if self.pos_x <= 35:
                    self.is_wall_crawling = True
                    self.target_x = 22
                    if random.random() < 0.015 and self.state_timer == 0:
                        self.target_y = random.randint(50, sh - self.win_h - 80)
                elif self.pos_x >= sw - self.win_w - 35:
                    self.is_wall_crawling = True
                    self.target_x = sw - self.win_w - 22
                    if random.random() < 0.015 and self.state_timer == 0:
                        self.target_y = random.randint(50, sh - self.win_h - 80)

            # Gravity pull down towards ground floor
            if self.gravity_enabled:
                if self.pos_y < ground_y - 2:
                    self.vy += 1.4  # Gravitational acceleration
                    self.vy = min(18.0, self.vy)  # Terminal falling velocity
                    self.is_grounded = False
                else:
                    # Ground contact!
                    if not self.is_grounded and self.vy > 2.5:
                        # Impact landing squash and dust burst
                        self.landing_squash = min(0.35, self.vy * 0.035)
                        for _ in range(6):
                            self.dust_particles.append({
                                'x': (self.win_w // 2) + random.uniform(-16, 16),
                                'y': self.win_h - 10 + random.uniform(-2, 2),
                                'vx': random.uniform(-1.8, 1.8),
                                'vy': random.uniform(-1.2, -0.2),
                                'size': random.uniform(3.0, 5.0),
                                'life': 1.0,
                                'decay': random.uniform(0.08, 0.14)
                            })
                    self.pos_y = float(ground_y)
                    self.target_y = float(ground_y)
                    self.vy = 0.0
                    self.is_grounded = True

                # Autonomous wander strictly on bottom floor horizontally
                if random.random() < 0.008 and self.state_timer == 0:
                    wander_range = 280
                    new_tx = self.pos_x + random.randint(-wander_range, wander_range)
                    self.target_x = max(20.0, min(float(sw - self.win_w - 20), new_tx))
                    self.target_y = float(ground_y)

            else:
                # Gravity OFF (Free Roam)
                self.is_grounded = False
                if random.random() < 0.007 and self.state_timer == 0:
                    self.target_x = max(20.0, min(float(sw - self.win_w - 20), self.pos_x + random.randint(-220, 220)))
                    self.target_y = max(40.0, min(float(sh - self.win_h - 60), self.pos_y + random.randint(-140, 140)))

            # Realistic Inertia & Velocity Easing
            # Horizontal motion
            dx = self.target_x - self.pos_x
            if abs(dx) > 3.0:
                max_spd_x = 6.8 if self.current_char in ("Beru", "Spiderman") else 4.2
                desired_vx = max(-max_spd_x, min(max_spd_x, dx * 0.14))
                self.vx += (desired_vx - self.vx) * 0.22
            else:
                self.vx *= 0.65
                if abs(self.vx) < 0.08:
                    self.vx = 0.0

            # Vertical motion (if not grounded in gravity mode)
            if not (self.gravity_enabled and self.is_grounded):
                dy = self.target_y - self.pos_y
                if abs(dy) > 3.0:
                    max_spd_y = 6.0 if self.current_char in ("Beru", "Spiderman") else 3.8
                    desired_vy = max(-max_spd_y, min(max_spd_y, dy * 0.14))
                    self.vy += (desired_vy - self.vy) * 0.20
                else:
                    self.vy *= 0.65
                    if abs(self.vy) < 0.08:
                        self.vy = 0.0

            # Integrate position
            self.pos_x += self.vx
            self.pos_y += self.vy

            # Clamp boundaries
            self.pos_x = max(10.0, min(float(sw - self.win_w - 10), self.pos_x))
            if self.gravity_enabled:
                if self.pos_y >= ground_y:
                    self.pos_y = float(ground_y)
                    self.vy = 0.0
                    self.is_grounded = True
            else:
                self.pos_y = max(30.0, min(float(sh - self.win_h - 40), self.pos_y))

            self.x = int(self.pos_x)
            self.y = int(self.pos_y)
            self.root.geometry(f"+{self.x}+{self.y}")

            # Direction & Flight Tilt
            if abs(self.vx) > 0.35:
                self.renderer.direction = 1 if self.vx > 0 else -1
            if self.current_char in ("Beru", "Spiderman"):
                self.flight_tilt = max(-18.0, min(18.0, self.vx * -2.4))
            else:
                self.flight_tilt *= 0.8

            # Stride accumulation for realistic walk cycle
            speed = math.hypot(self.vx, self.vy)
            if speed > 0.3:
                self.walk_cycle += speed * 0.15
                # Spawn running dust puffs on floor
                if self.is_grounded and abs(self.vx) > 1.2 and random.random() < 0.35:
                    paw_dir = -1 if self.vx > 0 else 1
                    self.dust_particles.append({
                        'x': (self.win_w // 2) + paw_dir * 14 + random.uniform(-4, 4),
                        'y': self.win_h - 10 + random.uniform(-2, 2),
                        'vx': paw_dir * random.uniform(0.6, 1.4),
                        'vy': random.uniform(-0.8, -0.2),
                        'size': random.uniform(2.5, 4.2),
                        'life': 1.0,
                        'decay': random.uniform(0.09, 0.15)
                    })

        # Elastic recovery from landing squash
        self.landing_squash *= 0.82

        # -------------------------------------------------------------
        # 3. Scheduled Reminders & Comments (Always Active!)
        # -------------------------------------------------------------
        if self.reminders_enabled and self.bubble_timer == 0:
            self.reminder_counter += 1
            target_ticks = self.reminder_interval_mins * 1714
            if self.reminder_counter >= target_ticks:
                self.reminder_counter = 0
                chosen_key = random.choice(["water", "posture", "eye", "walk", "coffee"])
                self.trigger_reminder(chosen_key)

        elif random.random() < 0.003 and self.bubble_timer == 0 and self.show_bubbles:
            char_quotes = self.QUOTES.get(self.current_char, self.QUOTES["Beru"])
            self.say(random.choice(char_quotes), duration=50)

        if self.bubble_timer > 0:
            self.bubble_timer -= 1
            if self.bubble_timer == 0:
                self.bubble_text = None

        self._draw_scene()
        self.root.after(35, self._tick)

    def _draw_scene(self):
        self.canvas.delete("all")

        # Ground dust puff particles
        for p in self.dust_particles:
            r = p['size']
            alpha_ratio = p['life']
            dust_col = "#D4CDBC" if alpha_ratio > 0.5 else "#E2DDD2"
            self.canvas.create_oval(p['x'] - r, p['y'] - r, p['x'] + r, p['y'] + r,
                                    fill=dust_col, outline="")

        # Full Display Speech Bubble
        if self.bubble_text and self.show_bubbles:
            bx = self.win_w // 2
            by = 22
            max_txt_w = 230

            tmp_id = self.canvas.create_text(bx, by, text=self.bubble_text,
                                             fill="#FFFFFF", font=("Segoe UI", 8, "bold"),
                                             width=max_txt_w, justify="center")
            bbox = self.canvas.bbox(tmp_id)
            self.canvas.delete(tmp_id)

            if bbox:
                tx1, ty1, tx2, ty2 = bbox
                pad_x = 12
                pad_y = 6
                x1, y1, x2, y2 = tx1 - pad_x, ty1 - pad_y, tx2 + pad_x, ty2 + pad_y

                bubble_fill = "#141124" if self.current_char in ("Beru", "Igris") else \
                              ("#1A0C14" if self.current_char == "Spiderman" else "#211A14")
                border_accent = "#00F0FF" if self.current_char == "Beru" else \
                                ("#FF2A4D" if self.current_char == "Igris" else \
                                ("#FF2233" if self.current_char == "Spiderman" else \
                                ("#40C070" if self.current_char == "Cat" else "#FFAA33")))

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bubble_fill, outline=border_accent, width=1.5)
                self.canvas.create_polygon([bx - 5, y2, bx + 5, y2, bx, y2 + 6], fill=bubble_fill, outline=border_accent)

                self.canvas.create_text(bx, (y1 + y2) // 2, text=self.bubble_text,
                                        fill="#FFFFFF", font=("Segoe UI", 8, "bold"),
                                        width=max_txt_w, justify="center")

        # Render Character Sprite with dynamic physical attributes
        is_moving_now = (abs(self.vx) > 0.4 or abs(self.vy) > 0.4) and not self.sit_silently
        photo = self.renderer.render(
            frame=self.frame,
            emotion=self.emotion,
            flight_tilt=self.flight_tilt,
            is_active=self.jiggler.active,
            is_moving=is_moving_now,
            is_wall_crawling=self.is_wall_crawling,
            walk_cycle=self.walk_cycle,
            is_grounded=self.is_grounded,
            landing_squash=self.landing_squash
        )
        self._current_photo = photo
        px = (self.win_w - self.pet_w) // 2
        py = self.bubble_space + (self.win_h - self.bubble_space - self.pet_h) // 2
        self.canvas.create_image(px, py, anchor="nw", image=photo)

    # ══════════════════════════════════════════════════════════════════
    #  HOTKEYS & SYSTEM TRAY
    # ══════════════════════════════════════════════════════════════════

    def _setup_hotkeys(self):
        def hotkey_loop():
            user32.RegisterHotKey(None, HOTKEY_TOGGLE, MOD_CONTROL, 0x42)  # Ctrl+B
            user32.RegisterHotKey(None, HOTKEY_HIDE, MOD_CONTROL | MOD_SHIFT, 0x51)  # Ctrl+Shift+Q
            user32.RegisterHotKey(None, HOTKEY_GRAVITY, MOD_CONTROL, 0x47)  # Ctrl+G
            user32.RegisterHotKey(None, HOTKEY_SIT, MOD_CONTROL, 0x53)  # Ctrl+S
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == 0x0312:
                    if msg.wParam == HOTKEY_TOGGLE:
                        self.root.after(0, self.toggle_jiggler)
                    elif msg.wParam == HOTKEY_HIDE:
                        self.root.after(0, self.toggle_visibility)
                    elif msg.wParam == HOTKEY_GRAVITY:
                        self.root.after(0, self.toggle_gravity)
                    elif msg.wParam == HOTKEY_SIT:
                        self.root.after(0, self.toggle_sit_silently)
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        threading.Thread(target=hotkey_loop, daemon=True).start()

    def _setup_tray(self):
        def on_toggle(icon, item): self.root.after(0, self.toggle_jiggler)
        def on_hide(icon, item): self.root.after(0, self.toggle_visibility)
        def on_gravity(icon=None, item=None): self.root.after(0, self.toggle_gravity)
        def on_sit(icon=None, item=None): self.root.after(0, self.toggle_sit_silently)
        def on_switch(char): self.root.after(0, lambda: self.switch_character(char))
        def on_remind(key): self.root.after(0, lambda: self.trigger_reminder(key))
        def on_interval(mins): self.root.after(0, lambda: self.set_reminder_interval(mins))
        def on_quit(icon, item): self.root.after(0, self.quit_app)

        def create_char_item(char_name, label):
            return pystray.MenuItem(
                label,
                lambda: on_switch(char_name),
                checked=lambda item: self.current_char == char_name
            )

        char_menu = pystray.Menu(
            create_char_item("Beru", "🐜 Shadow Marshal Beru"),
            create_char_item("Igris", "🗡️ Blood-Red Commander Igris"),
            create_char_item("Cat", "🐱 Cute Calico Cat"),
            create_char_item("Spiderman", "🕷️ The Amazing Spider-Man"),
            create_char_item("Puppy", "🐶 Cute Golden Puppy"),
        )

        timing_menu = pystray.Menu(
            pystray.MenuItem("Every 15 Minutes", lambda: on_interval(15), checked=lambda item: self.reminder_interval_mins == 15),
            pystray.MenuItem("Every 30 Minutes", lambda: on_interval(30), checked=lambda item: self.reminder_interval_mins == 30),
            pystray.MenuItem("Every 45 Minutes", lambda: on_interval(45), checked=lambda item: self.reminder_interval_mins == 45),
            pystray.MenuItem("Every 60 Minutes", lambda: on_interval(60), checked=lambda item: self.reminder_interval_mins == 60),
        )

        remind_menu = pystray.Menu(
            pystray.MenuItem("💧 Drink Water", lambda: on_remind("water")),
            pystray.MenuItem("🧘 Posture & Stretch", lambda: on_remind("posture")),
            pystray.MenuItem("👀 20-20-20 Eye Break", lambda: on_remind("eye")),
            pystray.MenuItem("🚶 Stand & Walk", lambda: on_remind("walk")),
            pystray.MenuItem("☕ Coffee / Tea", lambda: on_remind("coffee")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("⏱️ Interval", timing_menu),
            pystray.MenuItem("Auto-Reminders Active", lambda: self.toggle_reminders(), checked=lambda item: self.reminders_enabled)
        )

        tray_menu = pystray.Menu(
            pystray.MenuItem("Toggle Awake / Domain (Ctrl+B)", on_toggle, default=True),
            pystray.MenuItem("🌍 Floor Gravity (Bottom Roam)", lambda item: on_gravity(), checked=lambda item: self.gravity_enabled),
            pystray.MenuItem("🪑 Sit Silently (Stay)", lambda item: on_sit(), checked=lambda item: self.sit_silently),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("👤 Character", char_menu),
            pystray.MenuItem("⏰ Reminders", remind_menu),
            pystray.MenuItem(lambda item: "Show Companion" if not self.visible else "Hide Companion (Ctrl+Shift+Q)", on_hide),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", on_quit)
        )

        self.tray_icon = pystray.Icon(
            "desktop_companion",
            self._create_tray_image(),
            f"Desktop Companion ({self.current_char})",
            tray_menu
        )

        def run_tray_safely():
            try:
                self.tray_icon.run()
            except Exception:
                pass
        threading.Thread(target=run_tray_safely, daemon=True).start()

    def _create_tray_image(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.png")
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path).convert("RGBA").resize((64, 64), Image.LANCZOS)
                d = ImageDraw.Draw(img)
                if self.jiggler.active:
                    # Glowing cyan/neon dot on bottom right for awake status
                    d.ellipse([42, 42, 60, 60], fill=(0, 240, 255, 140))
                    d.ellipse([45, 45, 57, 57], fill=(0, 255, 200, 255))
                return img
            except Exception:
                pass

        # Fallback procedural icon
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        bg_col = (18, 12, 32, 255) if self.current_char == "Beru" else \
                 ((32, 10, 18, 255) if self.current_char == "Igris" else \
                 ((220, 20, 45, 255) if self.current_char == "Spiderman" else \
                 ((255, 220, 190, 255) if self.current_char == "Cat" else (242, 172, 98, 255))))
        d.ellipse([4, 4, 60, 60], fill=bg_col)
        dot_col = (0, 240, 255, 255) if self.jiggler.active else (140, 140, 150, 255)
        d.ellipse([44, 44, 58, 58], fill=dot_col)
        return img

    def _update_tray(self):
        try:
            if hasattr(self, "tray_icon") and self.tray_icon:
                self.tray_icon.icon = self._create_tray_image()
                self.tray_icon.title = f"Desktop Companion ({self.current_char}) - {'AWAKE' if self.jiggler.active else 'SLEEP'}"
        except Exception:
            pass

    def quit_app(self):
        if self.context_menu:
            self.context_menu.dismiss_all()
        self.jiggler.stop()
        self._save_state()
        try:
            if hasattr(self, "tray_icon") and self.tray_icon:
                self.tray_icon.stop()
        except Exception:
            pass
        self.root.destroy()
        sys.exit(0)

# ══════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Solo Leveling & Desktop Companion Suite")
    parser.add_argument("--char", choices=["Beru", "Igris", "Cat", "Spiderman", "Puppy"], default=None,
                        help="Initial character to launch with")
    args, _ = parser.parse_known_args()

    app = DesktopCompanionApp(default_char=args.char)
    app.root.mainloop()

if __name__ == "__main__":
    main()
