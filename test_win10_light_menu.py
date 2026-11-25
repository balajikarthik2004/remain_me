import tkinter as tk

class Win10LightContextMenu:
    """
    Authentic Windows 10 Light Mode Context Menu for Tkinter.
    Features:
    - Pure Windows 10 Light surface: Clean (#FCFCFC / #F3F3F3) with 1px border (#C8C8C8)
    - Classic Windows 10 light selection highlight (#E5E5E5)
    - High-contrast typography (Segoe UI, #111111)
    - Windows Blue accent (#0078D7) for checkmarks and active headers
    - Pixel-perfect submenu positioning immediately adjacent to hovered row (no screen jumping!)
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
                hdr_frame = tk.Frame(self.container, bg="#F0F0F0", padx=8, pady=4)
                hdr_frame.pack(fill="x", pady=(0, 2))
                lbl_top = tk.Label(hdr_frame, text=item.get("title", ""), bg="#F0F0F0",
                                   fg=self.ACCENT_BLUE, font=("Segoe UI", 8, "bold"), anchor="w")
                lbl_top.pack(fill="x")
                if "subtitle" in item:
                    lbl_sub = tk.Label(hdr_frame, text=item.get("subtitle", ""), bg="#F0F0F0",
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

        # If fits to right of parent menu, place immediately on the right edge
        if parent_rx + parent_rw + sub_w <= sw - 8:
            sub_x = parent_rx + parent_rw - 2
        else:
            # Otherwise flip to the left edge of parent menu
            sub_x = parent_rx - sub_w + 2

        # Align vertically with hovered row
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Win10 Light Submenu Geometry Test")
    root.geometry("400x300")
    
    items = [
        {"type": "header", "title": "👑 DESKTOP COMPANION", "subtitle": "Windows 10 Light Format"},
        {"icon": "👤", "label": "Switch Companion", "submenu": [
            {"icon": "🐜", "label": "Shadow Marshal Beru", "checked": True},
            {"icon": "🗡️", "label": "Blood-Red Commander Igris", "checked": False},
            {"icon": "🐶", "label": "Cute Golden Puppy", "checked": False},
        ]},
        {"icon": "⏰", "label": "Remind Me / Care", "submenu": [
            {"icon": "⏱️", "label": "Reminder Timing", "submenu": [
                {"icon": "⚡", "label": "Every 15 Minutes", "checked": False},
                {"icon": "⏱️", "label": "Every 30 Minutes", "checked": True},
                {"icon": "⏳", "label": "Every 45 Minutes", "checked": False},
                {"icon": "🕐", "label": "Every 60 Minutes", "checked": False},
            ]},
            {"type": "separator"},
            {"icon": "💧", "label": "Drink Water Break"},
            {"icon": "🧘", "label": "Posture & Stretch Check"},
            {"icon": "👀", "label": "20-20-20 Eye Relief"},
        ]},
        {"type": "separator"},
        {"icon": "❌", "label": "Exit Application", "command": root.quit}
    ]

    def popup(e):
        m = Win10LightContextMenu(root, items)
        m.show(e.x_root, e.y_root)

    root.bind("<Button-3>", popup)
    root.after(400, lambda: print("Win10 Light Submenu Geometry Test started."))
    root.after(800, root.quit)
    root.mainloop()
