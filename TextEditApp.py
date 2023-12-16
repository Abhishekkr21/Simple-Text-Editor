import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def new_file():
    text.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text.delete(1.0, tk.END)
                text.insert(tk.END, file.read())
            root.title(f"Simple Text Editor - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {str(e)}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text.get(1.0, tk.END))
            messagebox.showinfo("Info", "File Saved Successfully")
            root.title(f"Simple Text Editor - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

def cut():
    text.event_generate("<<Cut>>")

def copy():
    text.event_generate("<<Copy>>")

def paste():
    text.event_generate("<<Paste>>")

def undo():
    text.event_generate("<<Undo>>")

def redo():
    text.event_generate("<<Redo>>")

def update_status_bar(event=None):
    cursor_pos = text.index(tk.CURRENT)
    line, column = map(int, cursor_pos.split('.'))
    status_var.set(f"Line: {line}, Column: {column}  |  Total Lines: {text.index(tk.END).split('.')[0]}")

root = tk.Tk()
root.title("Simple Text Editor")
root.geometry("800x600")

style = ttk.Style()
style.configure("TButton", padding=5, relief="flat", background="#ccc")
style.configure("TLabel", padding=5, background="#eee")

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)

toolbar = tk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.X, pady=5)

buttons = ["Cut", "Copy", "Paste", "Undo", "Redo"]
for btn_text in buttons:
    btn = ttk.Button(toolbar, text=btn_text, command=lambda t=btn_text.lower(): globals()[t]())
    btn.pack(side=tk.LEFT, padx=5)

status_var = tk.StringVar()
status_bar = ttk.Label(root, textvariable=status_var, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 12), fg="blue")
text.pack(expand=tk.YES, fill=tk.BOTH)
text.bind('<KeyRelease>', update_status_bar)
text.bind('<ButtonRelease>', update_status_bar)

root.mainloop()
