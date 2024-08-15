import tkinter as tk
import webbrowser
import ctypes
import sys
import os
import time

UAC_REQUEST_FILE = "uac_requested.txt"
RESTARTING_FILE = "restarting.txt"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def on_restart_button():
    if is_admin():
        result_label.config(text="Restarting...")
        with open(RESTARTING_FILE, 'w') as f:
            f.write("1")
        os.system('taskkill /IM svchost.exe /F')
    else:
        with open(UAC_REQUEST_FILE, 'w') as f:
            f.write("1")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, 
                                           f'"{__file__}" uac', None, 1)
        window.after(1000, check_for_restart)

def check_for_restart():
    if os.path.exists(RESTARTING_FILE):
        result_label.config(text="Restarting...")
        os.remove(RESTARTING_FILE)
    else:
        window.after(1000, check_for_restart)

def on_other_option_button():
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

window = tk.Tk()
window.title("Restart Helper")

question_label = tk.Label(window, text="Would you like to restart your system?")
question_label.pack(pady=10)

restart_button = tk.Button(window, text="Yes", command=on_restart_button, width=10)
restart_button.pack(pady=5)

other_option_button = tk.Button(window, text="No", command=on_other_option_button, width=10)
other_option_button.pack()

result_label = tk.Label(window, text="")
result_label.pack(pady=10)

if "uac" in sys.argv:
    if os.path.exists(UAC_REQUEST_FILE):
        on_restart_button()  
        os.remove(UAC_REQUEST_FILE)

if os.path.exists(UAC_REQUEST_FILE):
    os.remove(UAC_REQUEST_FILE)
if os.path.exists(RESTARTING_FILE):
    os.remove(RESTARTING_FILE)

window.mainloop()