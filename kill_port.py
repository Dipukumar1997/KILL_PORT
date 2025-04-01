import tkinter as tk
from tkinter import messagebox
import os
import subprocess

def kill_port():
    port = entry.get().strip()
    if not port.isdigit():
        messagebox.showerror("Error", "Please enter a valid port number")
        return
    
    try:
        port = int(port)
        if os.name == 'nt':  # Windows
            cmd = f'netstat -ano | findstr :{port}'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            lines = result.stdout.strip().split("\n")
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    os.system(f'taskkill /F /PID {pid}')
                    messagebox.showinfo("Success", f"Killed process {pid} on port {port}")
        else:  # Linux & Mac
            cmd = f'lsof -i :{port} | grep LISTEN'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            lines = result.stdout.strip().split("\n")
            
            for line in lines:
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    os.system(f'kill -9 {pid}')
                    messagebox.showinfo("Success", f"Killed process {pid} on port {port}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Kill Process by Port")
root.geometry("300x150")

label = tk.Label(root, text="Enter Port:")
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="Kill Process", command=kill_port)
button.pack(pady=10)

root.mainloop()