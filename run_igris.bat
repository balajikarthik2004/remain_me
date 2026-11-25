@echo off
echo.
echo  ======================================================
echo    🗡️ Solo Leveling — Commander Igris Desktop App
echo  ======================================================
echo.
echo  Controls:
echo    Ctrl+B       = Toggle Shadow Domain (Awake Mode)
echo    Ctrl+Shift+Q = Summon / Hide Companion
echo    Left-Click   = Praise Igris (Knight's homage & royal bow!)
echo    Double-Click = Call Igris to cursor
echo    Drag         = Move companion anywhere
echo    Right-Click  = Windows 10/11 Fluent Dark Context Menu
echo.
echo  "My blade is sworn to you, Sovereign!"
echo.

cd /d "%~dp0"
start "" pythonw "desktop_companion.pyw" --char Igris
if %ERRORLEVEL% NEQ 0 (
    start "" python "desktop_companion.pyw" --char Igris
)
timeout /t 2 >nul
