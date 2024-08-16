import tkinter as tk
import webbrowser
import ctypes
import sys
import os

UAC_REQUEST_FILE = "uac_requested.txt"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin privileges: {e}")
        return False

def on_restart_button():
    if is_admin():
        result_label.config(text="Restarting...")
        try:
            os.system('taskkill /IM svchost.exe /F') 
        except Exception as e:
            result_label.config(text=f"Error during restart: {e}")
    else:
        try:
            with open(UAC_REQUEST_FILE, 'w') as f:
                f.write("1")
        except Exception as e:
            result_label.config(text=f"Error creating UAC file: {e}")
            return

        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, 
                                               f'"{__file__}" uac', None, 1)
            window.destroy() 
        except Exception as e:
            result_label.config(text=f"Error requesting UAC elevation: {e}")

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
        try:
            os.remove(UAC_REQUEST_FILE)
            on_restart_button() 
        except Exception as e:
            result_label.config(text=f"Error during UAC handling: {e}")

window.mainloop()
