import sys
print(f"Python: {sys.version}")
try:
    import tkinter as tk
    print("tkinter: OK")
except Exception as e:
    print(f"tkinter: FAIL - {e}")
try:
    import pyautogui
    print("pyautogui: OK")
except Exception as e:
    print(f"pyautogui: FAIL - {e}")
try:
    import keyboard
    print("keyboard: OK")
except Exception as e:
    print(f"keyboard: FAIL - {e}")
try:
    import ctypes
    print("ctypes: OK")
except Exception as e:
    print(f"ctypes: FAIL - {e}")

# Quick syntax check on the main file
import os, py_compile
script = os.path.join(os.path.dirname(__file__), "desktop_puppy.pyw")
try:
    py_compile.compile(script, doraise=True)
    print(f"desktop_puppy.pyw: SYNTAX OK")
except py_compile.PyCompileError as e:
    print(f"desktop_puppy.pyw: SYNTAX ERROR - {e}")
