@echo off
setlocal
echo.
echo ======================================================
echo   Creating Windows Desktop Shortcut for Companion App
echo ======================================================
echo.

set SCRIPT_DIR=%~dp0
set TARGET_PYW=%SCRIPT_DIR%desktop_companion.pyw
set ICON_PATH=%SCRIPT_DIR%assets\app_icon.ico
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Desktop Companion.lnk

powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = 'pythonw.exe'; $s.Arguments = '\"%TARGET_PYW%\"'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.IconLocation = '%ICON_PATH%, 0'; $s.Description = 'Desktop Companion Suite with Beru, Igris, Puppy, Cat & Spider-Man'; $s.Save()"

if exist "%SHORTCUT_PATH%" (
    echo [SUCCESS] Shortcut created on your Desktop:
    echo "%SHORTCUT_PATH%"
    echo With custom app icon: "%ICON_PATH%"
) else (
    echo [ERROR] Could not create shortcut.
)
echo.
pause
