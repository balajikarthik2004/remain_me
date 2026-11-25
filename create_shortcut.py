import os
import subprocess

lnk_path = os.path.abspath('Desktop Companion.lnk')
pyw_path = os.path.abspath('desktop_companion.pyw')
work_dir = os.path.abspath('.')
ico_path = os.path.abspath(os.path.join('assets', 'app_icon.ico'))

ps_script = f"""
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut('{lnk_path}')
$s.TargetPath = 'pythonw.exe'
$s.Arguments = '\"{pyw_path}\"'
$s.WorkingDirectory = '{work_dir}'
$s.IconLocation = '{ico_path},0'
$s.Description = 'Desktop Companion Suite'
$s.Save()
"""

with open("temp_make_shortcut.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "temp_make_shortcut.ps1"], capture_output=True, text=True)
if os.path.exists("temp_make_shortcut.ps1"):
    os.remove("temp_make_shortcut.ps1")

print("STDOUT:", res.stdout.strip())
if res.stderr:
    print("STDERR:", res.stderr.strip())
print("Shortcut created successfully:", os.path.exists(lnk_path))
