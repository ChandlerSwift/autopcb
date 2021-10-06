#!/usr/bin/env python3

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# from https://www.studytonight.com/tkinter/text-editor-application-using-tkinter
def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("autopcb files", "*.py"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Text Editor Application - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Text Editor Application - {filepath}")


window = tk.Tk()
window.title("autopcb")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=600, weight=1)
window.columnconfigure(2, minsize=600, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

canvas = tk.Canvas(window, bg="white")

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")
canvas.grid(row=0, column=2, sticky="nsew")

def run():
    exec(txt_edit.get("1.0", tk.END)) # secure!
btn_run = tk.Button(fr_buttons, text="Run", command=run)
btn_run.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

window.mainloop()
