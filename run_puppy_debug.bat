@echo off
cd /d "%~dp0"
echo.
echo  === Desktop Widget Debug Mode ===
echo.
echo  Checking Python...
python --version
echo.
echo  Checking Pillow...
python -c "from PIL import Image; print('Pillow OK')"
echo.
echo  Checking pystray...
python -c "import pystray; print('pystray OK')"
echo.
echo  Launching (errors will show here)...
echo  =========================================
echo.
python desktop_puppy.pyw
echo.
echo  Exit code: %ERRORLEVEL%
echo.
pause
