import tkinter as tk
import time

class Win11Menu:
    """
    Windows 10 / 11 Fluent Dark Style Context Menu for Tkinter.
    Features:
    - Acrylic / Mica dark background (#1E1E24 / #181820)
    - 1px subtle highlight border (#38384A)
    - Rounded pill hover effect (#2C2C3A)
    - Icon, label, hotkey badges, checkmarks (✓), and submenus (›)
    - Automatic dismiss on click-outside or Escape
    """
    BG_COLOR = "#1C1B24"
    BORDER_COLOR = "#343346"
    HOVER_BG = "#2C2B3C"
    HOVER_BORDER = "#403E58"
    TEXT_COLOR = "#F2F2F7"
    TEXT_MUTED = "#8E8DA0"
    ACCENT_COLOR = "#00F0FF"
    SEPARATOR_COLOR = "#2B2A3A"
    FONT_ITEM = ("Segoe UI", 9)
    FONT_ICON = ("Segoe UI Emoji", 10)
    FONT_BADGE = ("Segoe UI", 8)

    def __init__(self, master, items, is_submenu=False, parent_menu=None):
        self.master = master
        self.items = items
        self.is_submenu = is_submenu
        self.parent_menu = parent_menu
        self.active_submenu = None
        self.hover_timer = None
        
        self.win = tk.Toplevel(master)
        self.win.withdraw()
        self.win.wm_overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=self.BORDER_COLOR)

        # Inner container for 1px border
        self.container = tk.Frame(self.win, bg=self.BG_COLOR, padx=4, pady=5)
        self.container.pack(fill="both", expand=True, padx=1, pady=1)

        self.row_widgets = []
        self._build_items()

        if not is_submenu:
            # Bind global dismiss events
            self.win.bind("<Escape>", lambda e: self.dismiss_all())
            self.master.bind("<Button-1>", self._on_master_click, add="+")
            self.win.bind("<FocusOut>", self._on_focus_out)

    def _build_items(self):
        for idx, item in enumerate(self.items):
            if item.get("type") == "separator":
                sep = tk.Frame(self.container, bg=self.SEPARATOR_COLOR, height=1)
                sep.pack(fill="x", padx=6, pady=4)
                continue

            if item.get("type") == "header":
                hdr = tk.Label(self.container, text=item.get("text", ""),
                               bg=self.BG_COLOR, fg=self.TEXT_MUTED,
                               font=("Segoe UI", 7, "bold"), anchor="w", padx=8, pady=2)
                hdr.pack(fill="x")
                continue

            # Menu item row
            row = tk.Frame(self.container, bg=self.BG_COLOR, padx=6, pady=4, cursor="arrow")
            row.pack(fill="x", pady=1)

            # Left Icon
            icon_lbl = tk.Label(row, text=item.get("icon", " "), bg=self.BG_COLOR,
                                fg=self.TEXT_COLOR, font=self.FONT_ICON, width=2, anchor="center")
            icon_lbl.pack(side="left", padx=(0, 6))

            # Label text
            txt_lbl = tk.Label(row, text=item.get("label", ""), bg=self.BG_COLOR,
                               fg=self.TEXT_COLOR, font=self.FONT_ITEM, anchor="w")
            txt_lbl.pack(side="left", fill="x", expand=True)

            # Right badge: Submenu arrow / checkmark / shortcut
            right_text = ""
            right_color = self.TEXT_MUTED
            if item.get("submenu"):
                right_text = "›"
                right_color = self.TEXT_MUTED
            elif item.get("checked"):
                right_text = "✓"
                right_color = self.ACCENT_COLOR
            elif item.get("shortcut"):
                right_text = item.get("shortcut")
                right_color = self.TEXT_MUTED

            right_lbl = tk.Label(row, text=right_text, bg=self.BG_COLOR,
                                 fg=right_color, font=self.FONT_BADGE, anchor="e")
            right_lbl.pack(side="right", padx=(8, 2))

            widgets = [row, icon_lbl, txt_lbl, right_lbl]
            for w in widgets:
                w.bind("<Enter>", lambda e, r=row, it=item, ws=widgets: self._on_item_enter(r, it, ws))
                w.bind("<Leave>", lambda e, r=row, it=item, ws=widgets: self._on_item_leave(r, it, ws))
                w.bind("<Button-1>", lambda e, it=item: self._on_item_click(it))

            self.row_widgets.append((row, item, widgets))

    def _on_item_enter(self, row, item, widgets):
        # Apply hover pill background
        for w in widgets:
            w.configure(bg=self.HOVER_BG)
        
        # Handle submenu
        if item.get("submenu"):
            if self.active_submenu:
                self.active_submenu.destroy()
                self.active_submenu = None
            self._open_submenu(row, item["submenu"])
        else:
            if self.active_submenu:
                self.active_submenu.destroy()
                self.active_submenu = None

    def _on_item_leave(self, row, item, widgets):
        # Revert background only if submenu isn't actively open for this row
        if not (self.active_submenu and self.active_submenu_item == item):
            for w in widgets:
                w.configure(bg=self.BG_COLOR)

    def _open_submenu(self, row, sub_items):
        self.active_submenu_item = sub_items
        sub = Win11Menu(self.master, sub_items, is_submenu=True, parent_menu=self)
        self.active_submenu = sub
        
        # Position submenu to the right
        self.win.update_idletasks()
        rx = self.win.winfo_x() + self.win.winfo_width() - 4
        ry = self.win.winfo_y() + row.winfo_y()
        sub.show(rx, ry)

    def _on_item_click(self, item):
        cmd = item.get("command")
        if cmd:
            self.dismiss_all()
            cmd()

    def show(self, x, y):
        self.win.update_idletasks()
        w = self.win.winfo_reqwidth()
        h = self.win.winfo_reqheight()

        # Screen boundary check
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        if x + w > sw - 10:
            x = sw - w - 10 if not self.is_submenu else self.win.winfo_x() - w + 4
        if y + h > sh - 40:
            y = sh - h - 40

        self.win.geometry(f"+{max(10, x)}+{max(10, y)}")
        self.win.deiconify()
        self.win.focus_set()

    def _on_master_click(self, e):
        # If click outside our menu window, dismiss
        if self.win.winfo_ismapped():
            x, y = self.win.winfo_pointerxy()
            wx = self.win.winfo_x()
            wy = self.win.winfo_y()
            ww = self.win.winfo_width()
            wh = self.win.winfo_height()
            if not (wx <= x <= wx + ww and wy <= y <= wy + wh):
                self.dismiss_all()

    def _on_focus_out(self, e):
        # Dismiss if focus lost and no submenu open
        if not self.active_submenu:
            self.win.after(100, self._check_focus)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Win11 Menu Test")
    root.geometry("400x300")
    
    def on_select(name):
        print(f"Selected: {name}")

    menu_items = [
        {"type": "header", "text": "👑 DESKTOP COMPANION"},
        {"icon": "⚡", "label": "Activate Shadow Domain", "shortcut": "Ctrl+B", "command": lambda: on_select("Awake")},
        {"icon": "👑", "label": "Praise Companion", "command": lambda: on_select("Praise")},
        {"type": "separator"},
        {"icon": "👤", "label": "Switch Companion", "submenu": [
            {"icon": "🐜", "label": "Shadow Marshal Beru", "checked": True, "command": lambda: on_select("Beru")},
            {"icon": "🗡️", "label": "Commander Igris", "checked": False, "command": lambda: on_select("Igris")},
            {"icon": "🐶", "label": "Cute Golden Puppy", "checked": False, "command": lambda: on_select("Puppy")},
        ]},
        {"icon": "📏", "label": "Companion Size", "submenu": [
            {"icon": "▫️", "label": "Tiny (76px)", "checked": False, "command": lambda: on_select("Tiny")},
            {"icon": "▪️", "label": "Small (96px)", "checked": True, "command": lambda: on_select("Small")},
            {"icon": "◽", "label": "Medium (120px)", "checked": False, "command": lambda: on_select("Medium")},
        ]},
        {"icon": "💬", "label": "Speech Bubbles", "checked": True, "command": lambda: on_select("Bubbles")},
        {"type": "separator"},
        {"icon": "👁️", "label": "Hide Companion", "shortcut": "Ctrl+Shift+Q", "command": lambda: on_select("Hide")},
        {"icon": "❌", "label": "Dismiss Companion", "command": root.quit},
    ]

    def show_popup(e):
        m = Win11Menu(root, menu_items)
        m.show(e.x_root, e.y_root)

    root.bind("<Button-3>", show_popup)
    label = tk.Label(root, text="Right-click anywhere to test the Windows 11 Fluent Menu!", pady=40)
    label.pack()
    root.after(500, lambda: print("Win11 Menu Test initialized successfully."))
    root.after(1000, root.quit)
    root.mainloop()
