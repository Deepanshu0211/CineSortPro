import os
import shutil
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Frame, Label
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def create_directory_structure(base_dir, category, name, rating):
    try:    
        category_path = os.path.join(base_dir, category)
        name_path = os.path.join(category_path, name.lower())
        rating_path = os.path.join(name_path, rating)
        os.makedirs(rating_path, exist_ok=True)
        return rating_path
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def handle_video(file_path, base_dir, category, name, rating):
    if not file_path or not category or not name or not rating:
        messagebox.showerror("Error", "All fields must be filled out!")

        return
    
    dest_folder = create_directory_structure(base_dir, category, name, rating)
    file_name = os.path.basename(file_path)
    dest_path = os.path.join(dest_folder, file_name)
    
    shutil.move(file_path, dest_path)
    messagebox.showinfo("Success", f"File moved to: {dest_path}")
    return dest_path

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov")])
    if file_path:
        file_entry.delete(0, "end")
        file_entry.insert(0, file_path)
        file_label.config(text=f"Selected: {os.path.basename(file_path)}", foreground="green")

def submit():
    file_path = file_entry.get()
    category = category_var.get()
    name = name_entry.get().strip()
    rating = rating_var.get()
    base_dir = "Sorted_Videos"
    
    handle_video(file_path, base_dir, category, name, rating)

def drop(event):
    file_path = event.data.strip().replace('{', '').replace('}', '')
    file_entry.delete(0, "end")
    file_entry.insert(0, file_path)
    file_label.config(text=f"Selected: {os.path.basename(file_path)}", foreground="green")

root = TkinterDnD.Tk()
root.title("Video Sorter")
root.geometry("550x450")


root.resizable(False, False)

tb.Label(root, text="Movie Sorter", font=("Arial", 22, "bold"), bootstyle=PRIMARY).pack(pady=10)

drag_frame = Frame(root, width=500, height=100, bg="#2c3e50", relief="ridge", bd=2)
drag_frame.pack(pady=10)
drag_label = Label(drag_frame, text="Drag & Drop Video Here", fg="black", bg="#2c3e50", font=("Arial", 12))
drag_label.pack(expand=True)

drag_frame.drop_target_register(DND_FILES)
drag_frame.dnd_bind("<<Drop>>", drop)

file_frame = tb.Frame(root)
file_frame.pack(pady=5)
file_entry = tb.Entry(file_frame, width=50, font=("Arial", 12))
file_entry.pack(side="left", padx=5)
tb.Button(file_frame, text="Browse", bootstyle=SUCCESS, command=open_file_dialog).pack(side="left")
file_label = tb.Label(root, text="No file selected", bootstyle=SECONDARY)
file_label.pack()

tb.Label(root, text="Category:", font=("Arial", 12)).pack(pady=5)
category_var = tb.StringVar(value="Movie")
tb.Combobox(root, textvariable=category_var, values=["Movie", "Series"], font=("Arial", 12)).pack()

tb.Label(root, text="Enter Name:", font=("Arial", 12)).pack(pady=5)
name_entry = tb.Entry(root, width=40, font=("Arial", 12))
name_entry.pack()

tb.Label(root, text="Rating:", font=("Arial", 12)).pack(pady=5)
rating_var = tb.StringVar(value="A")
tb.Combobox(root, textvariable=rating_var, values=["A", "B", "C", "D", "E"], font=("Arial", 12)).pack()

tb.Button(root, text="Sort File", bootstyle=PRIMARY, command=submit, width=20).pack(pady=20)

root.mainloop()