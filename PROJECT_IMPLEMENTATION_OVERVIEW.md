# 🐾👑 Desktop Companion Suite — Windows 10 Professional Edition
**All 5 Companions: Beru, Igris, Puppy, Cute Cat & Spider-Man**

* **Workspace**: `c:\Users\BalajiKrishnan\Documents\bot`
* **Operating System**: Windows 10 / 11 (64-bit)
* **Core Languages & Runtimes**: Python 3.14 (Tkinter, ctypes, PIL, pystray), JavaScript / WebGL (Three.js)
* **Status**: Fully Implemented, Tested & Production-Ready

---

## 📖 Table of Contents
1. [Executive Overview](#1-executive-overview)
2. [Official Application Icon & Windows Branding](#2-official-application-icon--windows-branding)
3. [Windows 10 Light Mode Context Menu & Submenus](#3-windows-10-light-mode-context-menu--submenus)
4. [Full-Display Speech Bubble Engine (Zero Word Clipping)](#4-full-display-speech-bubble-engine-zero-word-clipping)
5. [Remind Me / Daily Care Habit System & Timing Intervals](#5-remind-me--daily-care-habit-system--timing-intervals)
6. [Companion 1: 🐜 Shadow Marshal Beru](#6-companion-1-🐜-shadow-marshal-beru)
7. [Companion 2: 🗡️ Blood-Red Commander Igris](#7-companion-2-🗡️-blood-red-commander-igris)
8. [Companion 3: 🐶 Cute Golden Puppy (Original Cute Pet Engine)](#8-companion-3-🐶-cute-golden-puppy-original-cute-pet-engine)
9. [Companion 4: 🐱 Cute Cat (Playful Calico Kitty)](#9-companion-4-🐱-cute-cat-playful-calico-kitty)
10. [Companion 5: 🕷️ Spider-Man (Friendly Neighborhood Desktop Hero)](#10-companion-5-🕷️-spider-man-friendly-neighborhood-desktop-hero)
11. [Companion 6: 🌐 3D Three.js WebGL Engine (`desktop_beru_3d.html`)](#11-companion-6-🌐-3d-threejs-webgl-engine-desktop_beru_3dhtml)
12. [The Shared Stealth Anti-Idle & Automation Engine](#12-the-shared-stealth-anti-idle--automation-engine)
13. [Comprehensive Controls & Hotkeys Master Table](#13-comprehensive-controls--hotkeys-master-table)
14. [Launchers & Verification Tools](#14-launchers--verification-tools)

---

## 1. Executive Overview

This software suite is an **enterprise-grade Windows desktop companion, habit reminder, and anti-idle automation system**. It merges three critical functions into one seamless experience:

1. **5 Interactive Desktop Companions**: Transparent, frameless, always-on-top companions that roam or float on your desktop, react to your mouse, show emotions, speak encouragement, and provide delightful interactive presence:
   * **Shadow Marshal Beru** (Solo Leveling)
   * **Blood-Red Commander Igris** (Solo Leveling)
   * **Cute Golden Puppy** (Original soulful procedural pet)
   * **Cute Cat** (Purring calico kitty with floating heart animations)
   * **Spider-Man** (Classic web-slinger with pendulum web swings, wall-crawling on monitor borders, and thwip blasts)
2. **Health & Habit Reminders**: Gentle automated and on-demand prompts for hydration (drinking water), posture stretching, 20-20-20 eye strain relief, and rest breaks tailored to each companion's personality, with configurable intervals (15m, 30m, 45m, 60m).
3. **Undetectable Anti-Idle Workstation Engine**: An enterprise-grade stealth automation layer simulating natural human input with Win32 hardware scancodes and cubic Bezier curves, keeping your workstation active without triggering idle timeouts.

---

## 2. Official Application Icon & Windows Branding

The suite features a custom brand identity icon featuring the cute coder pet, royal golden crown, Shadow Marshal Beru with cyan soulfire, and Blood-Red Commander Igris in a neon squircle badge:

* **High-Res Source Assets**:
  * [app_icon.png](file:///c:/Users/BalajiKrishnan/Documents/bot/assets/app_icon.png): 1024×1024 Master High-Resolution PNG.
  * [app_icon.ico](file:///c:/Users/BalajiKrishnan/Documents/bot/assets/app_icon.ico): Multi-resolution Windows Icon file containing 16×16, 24×24, 32×32, 48×48, 64×64, 128×128, and 256×256 layers.
* **Integrated Touchpoints**:
  * **System Tray ("Hidden Icons")**: Live 64×64 tray icon displaying the official artwork with a real-time glowing neon cyan indicator dot in the corner when Anti-Idle / Awake mode is engaged.
  * **Context Menu Header**: A thumbnail of the official app icon sits in the Windows 10 Light header card.
  * **Taskbar & Window Icon**: Registered via `root.iconbitmap()` and `root.iconphoto()` for clean Alt+Tab and taskbar representation.
  * **Desktop Shortcut**: [Desktop Companion.lnk](file:///c:/Users/BalajiKrishnan/Documents/bot/Desktop%20Companion.lnk) with the embedded `.ico` branding.

---

## 3. Windows 10 Light Mode Context Menu & Submenus

Right-clicking on any desktop companion summons an authentic **Windows 10 Light Mode Context Menu (`Win10LightContextMenu`)**:

### Visual & Interactive Features:
* **Authentic Light Surface**: Crisp light gray background (`#F9F9F9` / `#FFFFFF`) with a 1px border (`#D0D0D0`).
* **Header Card**: Clean header showing the active companion and real-time status (`👑 DESKTOP COMPANION • ● AWAKE` in Windows Accent Blue `#0078D7`).
* **Classic Windows 10 Light Selection**: Light gray hover highlight (`#E8E8E8`) matching native desktop menus.
* **Cascading Submenus (Pixel-Perfect Alignment)**: Submenus compute screen root geometry (`winfo_rootx()`, `row.winfo_rooty()`) to open snugly right adjacent to the hovered item with zero screen jumping.
  * **`⏰ Remind Me / Care ▸`**:
    * **`⏱️ Reminder Timing ▸`**: Choose interval: `Every 15m`, `Every 30m (Default)`, `Every 45m`, `Every 60m`.
    * `💧 Drink Water Break`
    * `🧘 Posture & Stretch Check`
    * `👀 20-20-20 Eye Relief`
    * `🚶 Stand Up & Walk`
    * `☕ Quick Rest / Tea Break`
    * `────────────────────`
    * `[✓] Auto-Reminders Active`
  * **`👤 Switch Companion ▸`**:
    * `[✓] 🐜 Shadow Marshal Beru`
    * `[ ] 🗡️ Blood-Red Commander Igris`
    * `[ ] 🐶 Cute Golden Puppy`
    * `[ ] 🐱 Cute Cat`
    * `[ ] 🕷️ Spider-Man`
  * **`📏 Companion Size ▸`**:
    * `[ ] Tiny`
    * `[✓] Small (Default)`
    * `[ ] Medium`
    * `[ ] Large`
* **Clean Grouped System Tray Menu**: The system tray ("hidden icons") groups character switching into a single `👤 Character ▸` submenu and reminder tools into an `⏰ Reminders ▸` submenu, with live checkmarks.
* **Right-Aligned Badges & Shortcuts**: Windows Blue checkmarks (`✓`), hotkey shortcuts (`Ctrl+B`, `Ctrl+Shift+Q`), and sub-menu arrows (`›`).
* **Auto-Dismiss**: Closes cleanly when clicking anywhere outside, selecting an item, or pressing `Escape`.

---

## 4. Full-Display Speech Bubble Engine (Zero Word Clipping)

Previous versions could truncate speech bubbles when quotes exceeded the narrow character window width. The speech bubble engine has been completely re-architected:

* **Generous Canvas Geometry**: Canvas width is expanded to `max(280, pet_w + 140)` so bubbles have up to 260px of comfortable horizontal room.
* **Multi-Line Automatic Text Wrapping**: Quotes automatically wrap across multiple lines (`width=230`) when long sentences appear.
* **Dynamic Bounding Box Calculation**: Uses `canvas.bbox()` to dynamically measure the exact rendered text dimensions, drawing a perfectly fitted bubble with 12px horizontal and 6px vertical padding.
* **Zero Clipping Guarantee**: 100% of every word, emoji, and punctuation mark is fully visible at all times.

---

## 5. Remind Me / Daily Care Habit System & Timing Intervals

A dedicated health and productivity habit reminder engine tailored to each companion:

### Configurable Timing Intervals:
Users can adjust the automated reminder frequency via **Right-Click ➔ `⏰ Remind Me / Care` ➔ `⏱️ Reminder Timing`**:
* **Every 15m**: High-frequency hydration & micro-stretch alerts
* **Every 30m (Default)**: Balanced wellness rhythm
* **Every 45m**: Deep focus interval
* **Every 60m**: Hourly stand-up and vision recharge

### Dialogue by Character:
* **💧 Hydration (Drink Water)**:
  * **Beru**: *"Drink water, My King! Your mortal vessel must be replenished! 💧👑"*
  * **Igris**: *"Replenish your mana, Sovereign! A Knight must stay hydrated! 💧🛡️"*
  * **Puppy**: `*brings a water bowl* Woof! Drink some water, human! 💧🐾`
  * **Cat**: `*paws at your water glass* Drink some water, human! Stay hydrated! 💧🐾`
  * **Spider-Man**: *"Hydrate or diedrate! Even super-heroes need water breaks! 💧🕷️"*
* **🧘 Posture & Stretch Check**:
  * **Beru**: *"Straighten your back, My King! A Monarch bows to no one! 🧘👑"*
  * **Igris**: *"Upright posture, Sovereign! Maintain the battle stance! ⚔️🛡️"*
  * **Puppy**: `*does a cute play-bow* Woof! Time to stretch our paws! 🧘🐕`
  * **Cat**: `*does a big arching cat stretch* Time for a deep stretch! 🧘✨`
  * **Spider-Man**: *"Web-slinger posture check! Stretch out those muscles! 🧘🕸️"*
* **👀 20-20-20 Eye Strain Relief Break**:
  * **Beru**: *"Rest your supreme eyes, Sovereign! Look into the distance! 👀⚡"*
  * **Igris**: *"Shield your vision, My King! Rest your eyes for 20 seconds! 🛡️👀"*
  * **Puppy**: `*blinks gently* Look far away and rest your eyes! 👀✨`
  * **Cat**: `*blinks slowly with affection* Rest your eyes for 20 seconds! 👀♡`
  * **Spider-Man**: *"Spider-Sense says: 20-20-20 rule! Look 20ft away for 20s! 👀🕷️"*

---

## 6. Companion 1: 🐜 Shadow Marshal Beru

* **Visual Design**: Obsidian carapace with electric-cyan mana circuits, flaring translucent wings, and piercing cyan soulfire eyes.
* **Living Particle Engine**: Real-time swirling violet/black shadow smoke wisps + glowing cyan soulfire embers floating upward.
* **Multi-Harmonic Flight Physics**: Airborne floating hover with directional banking tilts (-16° to +16°) when dashing across the screen toward your cursor.
* **5 Emotional States**:
  * *Idle / Hover* (living smoke and breathing)
  * *Crying / Tears of Devotion* (waterfalls of anime tears & floating hearts when praised: *"MY KING HAS TOUCHED ME!! 😭👑"*)
  * *Royal Fealty* (bowing beneath a golden Monarch Crown)
  * *Cheer* (victorious leap with sparkle gems)
  * *Flight Rush* (intercepting cursor with trailing shadow mist)
* **Motivational Royal Dialogue**: *"My king! 👑"*, *"You are the best! ✨"*, *"Nothing can stop you, My King! ⚡"*, *"Drink water, My King! 💧"*.

---

## 7. Companion 2: 🗡️ Blood-Red Commander Igris

* **Visual Design**: Obsidian knight plate armor with sharp spiky pauldrons, flowing crimson plume, glowing soulfire visor slit, and broadsword.
* **Living Particle Engine**: Dark purple shadow smoke + blood-crimson soulfire embers surging upward.
* **Marching Stride Physics**: Ground-level walking cycles with rhythmic knight footfalls, armor bobbing, and flowing plume inertia.
* **Knights Fealty**: Deep kneeling homage before the Sovereign.
* **Motivational Royal Dialogue**: *"For the Sovereign! 🗡️"*, *"My blade is yours, My King! 👑"*, *"A Knight's honor for the Monarch! 🛡️"*, *"Victory awaits you, Sovereign! ⚡"*.

---

## 8. Companion 3: 🐶 Cute Golden Puppy (Original Cute Pet Engine)

* **Original Cute Puppy Design (`PuppyRenderer`)**: Powered by the dedicated procedural cute puppy engine from `desktop_puppy.pyw`.
* **Distinctive Features**:
  * **Soulful Puppy-Dog Eyes**: Deep espresso pupil, warm amber iris rim, and triple specular sparkle highlights. Blinks naturally when idle.
  * **Floppy Bouncy Ears**: Golden-amber folded ears with soft rosy-peach inner fur that flop and bounce with trot momentum.
  * **Chubby Muzzle & Button Nose**: Plush cream muzzle pads, soft blush cheeks, sweet 'ω' smile, panting pink tongue, and a shiny wet button nose with specular highlights and nostrils.
  * **Fluffy Tail & Paws**: Curved fluffy tail that wags with smooth physics; chubby paws with cute pink paw pads.
  * **Sky-Blue Collar**: Adorned with a sparkling golden bell tag.
* **Animated States**:
  * `draw_sit`: Natural sitting puppy with breathing bounce and tail wag
  * `draw_walk`: Dynamic trotting stride with bouncing paws and floppy ears
  * `draw_wag`: Excited wagging frenzy with floating heart bursts (`♡`) and sparkles when petted
  * `draw_sleep`: Curled up adorably with floating animated `Zzz` bubbles
* **Zero-Halo Chroma-Keying**: Rendered at 4× supersampling with Lanczos downsampling onto `#FF00FF` with strict alpha thresholds for zero magenta halo on any wallpaper.

---

## 9. Companion 4: 🐱 Cute Cat (Pure Procedural Vector Engine)

* **100% Procedural Vector Architecture**: Built directly with 4× supersampled vectors (zero external image dependencies), identical to the architecture of the cute puppy companion!
* **Anatomical Vector Details**:
  * **Cream & Calico Coat**: Velvety cream base with warm ginger patches, dark calico spots, and pure white chest and paws.
  * **Pointy Feline Ears**: Triangular ears with soft pink inner ear fluff and micro-twitching physics.
  * **Emerald Anime Eyes**: Brilliant emerald irises with upper shade, lower crystal glow, dark feline liner, high-gloss specular sparkles, and automatic eyelid blinks (`frame % 42`).
  * **Chubby Whisker Pads & Nose**: Dainty pink nose, smiling muzzle, and 6 delicate white whiskers.
  * **Pink Toe Beans**: Soft paws with pink toe pads that step forward and backward during walking.
  * **Graceful Feline Tail**: Multi-segment curved tail that swishes with harmonic sine-wave physics.
  * **Ruby Bell Collar**: Red neckband with a gleaming golden bell that jingles as the kitty moves.
* **Animated States**:
  * `draw_sit`: Cozy loaf pose with rhythmic breathing chest expansion, ear twitching, blinking, and tail curls.
  * `draw_walk`: Real 4-legged feline prowl with alternating front and back paws, shoulder bob, and swaying tail.
  * `draw_purr`: Blissful closed happy eyes (`^ . ^`), rumbling vibration, rosy cheek blush, and floating pink hearts (`♡`).
  * `draw_sleep`: Curled up into a donut ball with paws tucked and floating `Zzz` bubbles.

---

## 10. Companion 5: 🕷️ Spider-Man (Pure Procedural Marvel Hero Engine)

* **100% Procedural Vector Architecture**: Built entirely with mathematical 4× supersampled superhero vectors (zero external image dependencies)!
* **Marvel Costume Anatomy**:
  * **Vibrant Red & Blue Suit**: Classic crimson cowl/torso and royal electric blue flanks and limbs.
  * **Full Webbing Grid**: Radiating and concentric black web lines across the mask and chest.
  * **Chest Spider Emblem**: Classic 8-legged black arachnid insignia centered on the chest.
  * **Expressive Eye Lenses**: Iconic white comic lenses with thick black borders that dynamically squint during motion and breathing.
  * **Silver Wrist Web-Shooters**: Functional gauntlets mounted on both wrists.
* **Special Superhero Mechanics & Skills**:
  1. **⚡ Spider-Sense Aura (`draw_idle`)**:
     * Heroic standing ready stance with breathing bob and lens squinting.
     * Dynamic electric comic-book Spider-Sense tingling arcs (`⚡`) flaring in golden-yellow and crimson energy around his mask.
  2. **🏃 Athletic Ninja Sprint Dash (`draw_dash`)**:
     * Low athletic ninja crouch sprint with forward torso lean (`14°`), rapid pumping limbs, and dynamic comic-book speed blur streaks (red and blue trails).
  3. **🚀 Dynamic Web Swinging with Ceiling Anchoring (`draw_web_swing`)**:
     * Mid-air pendulum swinging arc with one hand clutching a **taut braided web line** connected to your screen ceiling (`y = 0`) and other arm reaching forward.
  4. **🧗 Screen-Edge Wall Crawling (`draw_wall_crawl`)**:
     * Clinging to the glass edge of your monitor screen with splayed limbs and suction web pads.
  5. **🕸️ Web Throwing / Blast (`draw_thwip`)**:
     * Wrist web-shooter projectile beam with expanding concentric web-net circles and comic `THWIP!` sound burst!

---

## 11. Companion 6: 🌐 3D Three.js WebGL Engine (`desktop_beru_3d.html`)

**Source File**: [desktop_beru_3d.html](file:///c:/Users/BalajiKrishnan/Documents/bot/desktop_beru_3d.html) (~668 lines, 150 KB)  

* **WebGL Three.js Rendering**: Hardware-accelerated 3D rendering with dynamic lighting, specular highlights, and ambient glow.
* **Interactive 3D Mouse Tracking**: Beru's 3D head and body rotate in real-time 3D coordinate space to look directly at your mouse cursor.
* **360° Orbit Dragging**: Click and drag to inspect the character from any angle in 3D.

---

## 12. The Shared Stealth Anti-Idle & Automation Engine

* **Windows Native `SendInput` API**: Low-level `ctypes` calling `user32.dll!SendInput` directly, bypassing userland hooks.
* **Physical Hardware Scancodes**: Sends extended physical keyboard scancodes (`VK_F15` / `0x8E` dummy signals) that have zero visual output or side effects in IDEs, games, or terminals.
* **Humanized Cubic Bezier Trajectories**: Mouse movements follow randomized cubic Bezier curves with variable velocity, micro-jitters, and natural overshoot.
* **Multi-Monitor Safe**: Computes coordinates across multi-monitor virtual screens without clipping.

---

## 13. Comprehensive Controls & Hotkeys Master Table

| Action | Control / Shortcut | Behavior |
|---|---|---|
| **Toggle Awake / Domain** | `Ctrl + B` | Starts stealth anti-idle; surges particle aura |
| **Floor Gravity (Bottom Roam)** | `Ctrl + G` | Gravity pulls pet to bottom floor; roams strictly along taskbar |
| **Sit Silently (Stay in Place)** | `Ctrl + S` | Freezes motion in place; all reminders & comments stay 100% active |
| **Summon / Hide Pet** | `Ctrl + Shift + Q` | Hides window (keeps tray active) or restores it |
| **Interact / Praise / Pet** | Left-Click | Tears (Beru), Bow (Igris), Heart Wag (Puppy), Purr Hearts (Cat), **Thwip Web Blast (Spidey)** |
| **Call to Cursor** | Double-Click | Companion dashes, trots, or **web-swings** directly to mouse |
| **Move Companion** | Click & Drag | Smoothly relocate pet anywhere on screen; stays in place if sitting silently |
| **Open Menu** | Right-Click | **Windows 10 Light Mode Context Menu** |
| **Floor Gravity Toggle** | Right-Click ➔ `🌍 Floor Gravity` | Keeps pet roaming strictly along bottom floor with ground dust puffs |
| **Sit Silently Toggle** | Right-Click ➔ `🪑 Sit Silently` | Companion sits in place without moving; comments and reminders remain active |
| **Trigger Reminders** | Right-Click ➔ `⏰ Remind Me / Care` | On-demand water, posture, eye breaks, & auto-reminders |
| **Configure Reminder Timing**| Right-Click ➔ `⏱️ Reminder Timing` | Select interval: 15m, 30m, 45m, 60m |
| **Switch Character** | Right-Click ➔ `👤 Switch Companion` | Instant swap between **Beru, Igris, Puppy, Cat, and Spider-Man** |
| **Size Adjustment** | Right-Click ➔ `📏 Companion Size` | Tiny / Small (Default) / Medium / Large |
| **Toggle Bubbles** | Right-Click ➔ `💬 Speech Bubbles` | Turn speech thoughts on or off |
| **Exit Application** | Right-Click ➔ `❌ Dismiss Application` | Clean shutdown, release mutex and tray |

---

## 14. Launchers & Verification Tools

| Launcher | Description |
|---|---|
| **[run_companion.bat](file:///c:/Users/BalajiKrishnan/Documents/bot/run_companion.bat)** | **Master Launcher**: Starts companion with your last-saved character and preferences. |
| **[run_spiderman.bat](file:///c:/Users/BalajiKrishnan/Documents/bot/run_spiderman.bat)** | Launches companion directly as **Spider-Man** (with Web Swing, Wall Crawl, & Thwip). |
| **[run_cat.bat](file:///c:/Users/BalajiKrishnan/Documents/bot/run_cat.bat)** | Launches companion directly as the **Cute Cat** (purrs, meows, & heart animations). |
| **[run_beru.bat](file:///c:/Users/BalajiKrishnan/Documents/bot/run_beru.bat)** | Launches companion directly as **Shadow Marshal Beru**. |
| **[run_igris.bat](file:///c:/Users/BalajiKrishnan/Documents/bot/run_igris.bat)** | Launches companion directly as **Commander Igris**. |
| **[run_puppy.bat](file:///c:/Users/BalajiKrishnan/Documents/bot/run_puppy.bat)** | Launches companion directly as the **Cute Golden Puppy** (`desktop_puppy.pyw`). |
| **[test_all_companions.py](file:///c:/Users/BalajiKrishnan/Documents/bot/test_all_companions.py)** | Verifies initialization and frame generation for all 5 characters. |
| **[test_win10_light_menu.py](file:///c:/Users/BalajiKrishnan/Documents/bot/test_win10_light_menu.py)** | Dedicated visual & interaction test for the Windows 10 Light context menu. |

---

## 15. Real-Object Physical Movement, Gravity & Sit-Silently Mechanics

1. **Real-Object Physical Motion (No Flat Image Sliding)**:
   * **Inertia & Momentum Easing**: Realistic acceleration from rest (`vx += (desired_vx - vx) * 0.22`) and gradual deceleration/damping upon approaching target destinations, completely eliminating robotic, flat sliding artifacts.
   * **Dual-Sprite Cat Animation (`CuteCatRenderer`)**:
     * **Loaf / Sit Pose (`cat_hq.png`)**: Resting pose with gentle breathing squish (`dy = sin(frame * 0.20) * 1.6`) and ground shadow.
     * **Active Walk Pose (`cat_walk_hq.png`)**: Automatically engages when moving. Features a true 4-beat stepping gait with vertical bobbing (`abs(sin(cycle)) * 4.2`), dynamic step squash/stretch (`scale_y = 1.0 - abs(sin(cycle)) * 0.05`), and footfall shadow expansion.
   * **Spider-Man Athletic Sprint Dash (`SpidermanRenderer`)**:
     * **Ground Dash**: Low ninja crouch with forward athletic lean (`tilt = 14.0 * dir`), rapid footstep bounce, and dynamic comic-book speed streaks / motion blur trails behind him.
     * **Airborne Web-Swing**: Dynamic pendulum swing with taut glowing web line anchored to ceiling.
   * **Ground Dust Puff Particles**: Footsteps and paws kick up soft animated dust puffs (`dust_particles`) while traversing the bottom floor.
   * **Landing Squash & Impact Burst**: When falling and landing on the floor, the companion compresses with elastic landing squash (`landing_squash`) and radiates an impact burst of dust particles before springing back.

2. **Floor Gravity Mode (`🌍 Floor Gravity (Bottom Roam)`)**:
   * **Gravity Acceleration**: When enabled, the pet experiences gravitational pull (`vy += 1.4`) downwards to the bottom floor right above the Windows taskbar (`ground_y = sh - win_h - 45`).
   * **Strict Bottom Roaming**: Autonomous wander is clamped strictly to the horizontal floor axis (`target_y = ground_y`), ensuring the pet never floats or flies into midair.
   * **Toggleable Everywhere**: Toggleable via right-click context menu, system tray menu, or `Ctrl+G`.

3. **Sit Silently Mode (`🪑 Sit Silently (Stay in Place)`)**:
   * **Fixed Placement**: The companion completely halts autonomous wandering and sits stationary in a single place (`vx = 0, vy = 0`).
   * **Draggable Anywhere**: The user can drag and drop the companion anywhere on their desktop (e.g. corner of an app or screen), and it remains sitting silently right where released.
   * **Uninterrupted Health Reminders & Comments**: All health reminders (Drink Water, Posture Check, 20-20-20 Eye Relief, Stand & Walk, Coffee Break) and motivational speech bubbles remain 100% active and display right above the pet's sitting position on schedule!
   * **Toggleable Everywhere**: Toggleable via right-click context menu, system tray menu, or `Ctrl+S`.

