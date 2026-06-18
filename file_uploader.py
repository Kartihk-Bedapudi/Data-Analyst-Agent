import os
import shutil
import tkinter as tk
from tkinter import filedialog

def upload_pdf():
    root = tk.Tk()
    root.withdraw()
    
    root.attributes('-topmost',True)
    source_path = filedialog.askopenfilename(
        title = "select pdf to upload",
        filetypes = [("PDF documents","*.pdf")]
    )
    if not source_path:
        print("file uploadation cancelled, no file uploaded.")
        return
    return source_path