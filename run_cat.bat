@echo off
echo.
echo  ======================================================
echo    🐱 Cute Cat — Gentle Desktop Companion
echo  ======================================================
echo.
echo  Behaviors:
echo    * Soft purring with animated floating hearts
echo    * Playful pounces and cat-walk prowls
echo    * Gentle health and stretching reminders
echo.
echo  Controls:
echo    Left-Click   = Pet Kitty (Purrs and shows love!)
echo    Double-Click = Call Kitty to cursor
echo    Drag         = Move Kitty anywhere
echo    Right-Click  = Windows 10 Light Context Menu
echo.
echo  *Purrrr... Meow!*
echo.

cd /d "%~dp0"
start "" pythonw "desktop_companion.pyw" --char Cat
if %ERRORLEVEL% NEQ 0 (
    start "" python "desktop_companion.pyw" --char Cat
)
timeout /t 2 >nul
