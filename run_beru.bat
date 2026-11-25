@echo off
echo.
echo  ======================================================
echo    👑 Solo Leveling — Shadow Marshal Beru Desktop App
echo  ======================================================
echo.
echo  Controls:
echo    Ctrl+B       = Toggle Shadow Domain (Awake Mode)
echo    Ctrl+Shift+Q = Summon / Hide Companion
echo    Left-Click   = Praise Beru (Tears of devotion & royal joy!)
echo    Double-Click = Call Beru to cursor
echo    Drag         = Move companion anywhere
echo    Right-Click  = Windows 10/11 Fluent Dark Context Menu
echo.
echo  "I live only to serve you, My King!"
echo.

cd /d "%~dp0"
start "" pythonw "desktop_companion.pyw" --char Beru
if %ERRORLEVEL% NEQ 0 (
    start "" python "desktop_companion.pyw" --char Beru
)
timeout /t 2 >nul
