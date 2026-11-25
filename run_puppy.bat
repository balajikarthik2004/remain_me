@echo off
echo.
echo  ======================================================
echo    🐶 Cute Desktop Puppy — Original Edition
echo  ======================================================
echo.
echo  Controls:
echo    Ctrl+B       = Toggle Awake Mode
echo    Ctrl+Shift+Q = Summon / Hide Puppy
echo    Left-Click   = Pet Puppy (Watch him wag and bark happily!)
echo    Double-Click = Call Puppy to cursor
echo    Drag         = Move Puppy anywhere
echo    Right-Click  = Context menu
echo.
echo  *happy puppy wags* ♡
echo.

cd /d "%~dp0"
start "" pythonw "desktop_puppy.pyw"
if %ERRORLEVEL% NEQ 0 (
    start "" python "desktop_puppy.pyw"
)
timeout /t 2 >nul
