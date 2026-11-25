@echo off
echo.
echo  ======================================================
echo    🕷️ Spider-Man — Friendly Neighborhood Desktop Hero
echo  ======================================================
echo.
echo  Special Abilities:
echo    * Web Swing: Pendulum swing anchored from ceiling!
echo    * Wall Crawl: Climbs vertically when near screen edges!
echo    * Web Blast: Thwip! Shoots high-speed webbing!
echo.
echo  Controls:
echo    Left-Click   = High-five Spidey (Thwip web shot!)
echo    Double-Click = Swing over to cursor
echo    Drag         = Relocate Spider-Man
echo    Right-Click  = Windows 10 Light Context Menu
echo.
echo  "With great power comes great responsibility!"
echo.

cd /d "%~dp0"
start "" pythonw "desktop_companion.pyw" --char Spiderman
if %ERRORLEVEL% NEQ 0 (
    start "" python "desktop_companion.pyw" --char Spiderman
)
timeout /t 2 >nul
