@echo off
echo.
echo  ======================================================
echo    👑 Desktop Companion Suite — Professional Edition
echo  ======================================================
echo.
echo  Characters Available:
echo    - 🐜 Shadow Marshal Beru
echo    - 🗡️ Blood-Red Commander Igris
echo    - 🐶 Cute Golden Puppy
echo.
echo  Controls:
echo    Ctrl+B       = Toggle Awake / Shadow Domain
echo    Ctrl+Shift+Q = Summon / Hide Companion
echo    Left-Click   = Praise / Pet
echo    Double-Click = Call to cursor
echo    Drag         = Move anywhere
echo    Right-Click  = Windows 10/11 Fluent Dark Context Menu
echo.

cd /d "%~dp0"
start "" pythonw "desktop_companion.pyw"
if %ERRORLEVEL% NEQ 0 (
    start "" python "desktop_companion.pyw"
)
timeout /t 2 >nul
