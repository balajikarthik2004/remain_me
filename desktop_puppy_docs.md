# 🐾 Desktop Puppy — Technical Documentation

## Overview

**Desktop Puppy** is a delightful Windows desktop companion that combines:

1. **Visual Charm**: A real cute, animated golden puppy pet that roams near your system tray, reacts to petting, sleeps adorably, trots happily, and shares cute speech bubbles.
2. **Stealth Anti-Idle**: Keeps your PC active using low-level Win32 hardware simulation (`SendInput`), preventing idle timers and screen lockouts with 100% stealth.

---

## What's New: Cute Puppy & UI Enhancement

### 1. Real Cute Puppy Design (`PuppyRenderer`)
- **Soulful Puppy-Dog Eyes**: Deep espresso pupil, warm amber iris rim, and triple specular sparkle highlights that give the puppy real expressive life. Blinks naturally when idle.
- **Floppy Bouncy Ears**: Golden-amber folded ears with soft rosy-peach inner fur that flop and bounce with trot momentum.
- **Chubby Muzzle & Button Nose**: Plush cream muzzle pads, soft blush cheeks, sweet 'ω' smile, panting pink tongue, and a shiny wet button nose with specular highlights and nostrils.
- **Fluffy Tail & Paws**: Curved fluffy tail that wags with smooth physics; chubby paws with cute pink paw pads.
- **Sky-Blue Collar**: Adorned with a sparkling golden bell tag.
- **4× Supersampling (Anti-Aliasing)**: Rendered at 4× resolution, downscaled via Lanczos, and composited cleanly onto `#FF00FF` with a strict alpha threshold to ensure **zero color fringe or magenta halos** on any desktop wallpaper.

### 2. Compact, Small Size
- **Default Size**: **92×84 pixels** (~25% smaller than the original 120×110), making it unobtrusive, adorable, and clean.
- **Customizable Sizes** via the right-click menu:
  - **Small (Default)**: 92×84 px
  - **Tiny (Mini)**: 76×70 px
  - **Medium**: 110×100 px

### 3. Interactive Kawaii Speech Bubble
- Renders a floating dark glassmorphic thought/speech bubble above the puppy's head:
  - On Click / Pet: `*wags happily* ♡`, `Woof! Love you! 🐾`, `Good boy! 🦴`
  - On Awake Mode Toggle: `Awake Mode ON! ⚡`, `Rest mode ~ 💤`
  - Occasional friendly idle thoughts: `Stay hydrated! 💧`, `Blink your eyes! 👀`, `Doing great! 🌟`
  - Can be toggled on/off in the right-click menu.

### 4. Modern Windows 11 Glassmorphic UI
- **Notification Slider (`NotificationManager`)**:
  - Windows 11 style rounded card with frosted dark styling (`#131624`), emerald/coral accent glow bar, circular puppy avatar, and hotkey hints.
  - Smooth cubic slide-in physics from the taskbar.
- **Capsule Status Badge (`StatusBadge`)**:
  - Compact rounded pill (`94×26`) above the system tray clock with a live pulsing emerald dot (`● AWAKE`).
  - Clickable to quickly toggle awake mode.
- **High-Resolution Tray Icon**:
  - High-res 64×64 cute puppy icon in the system tray with live green/gray status dot.

---

## File Structure

```
C:\Users\BalajiKrishnan\Documents\bot\
├── desktop_puppy.pyw      # Main application (~1,250 lines)
├── run_puppy.bat          # Launcher (checks dependencies & starts puppy)
├── run_puppy_debug.bat    # Debug launcher
├── test_puppy.py          # Quick syntax & environment validator
└── desktop_puppy_docs.md  # Technical documentation
```

---

## Controls & Hotkeys

| Action | Shortcut / Trigger | Behavior |
|--------|-------------------|----------|
| **Toggle Awake** | `Ctrl + B` (or right-click menu) | Toggles active anti-idle mode with notification & tray update |
| **Hide / Show Puppy** | `Ctrl + Shift + Q` | Hides puppy window (stays running in tray) or restores it |
| **Pet Puppy** | Left-Click | Plays excited wag animation, hearts & cute woof bubble |
| **Call to Cursor** | Double-Click | Puppy trots directly to cursor position |
| **Move Puppy** | Click & Drag | Drag puppy to any location on your screen |
| **Context Menu** | Right-Click | Access awake toggle, pet size selector, bubble toggle, exit |
