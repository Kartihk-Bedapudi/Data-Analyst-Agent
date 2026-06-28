import tkinter as tk
from tkinter import filedialog

def upload_file():
    root = tk.Tk()
    root.withdraw()
    
    root.attributes('-topmost',True)
    source_path = filedialog.askopenfilename(
        title = "select file to work with",
        filetypes = [("CSV Files", "*.csv"),("Excel Files", "*.xlsx")]
    )
    if not source_path:
        print("file uploadation cancelled, no file uploaded.")
        root.destroy()
        return
    root.destroy()
    return source_path
