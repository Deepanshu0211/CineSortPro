import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import threading
import time

class ModernMovieSorter(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
      
        self.title("CineSort Pro")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.style = tb.Style("darkly")
        
       
        self.bg_color = "#1a1a2e"
        self.card_color = "#16213e"
        self.accent_color = "#ff5722"
        self.text_color = "#e2e2e2"
        self.configure(bg=self.bg_color)
        
      
        self.file_path = tk.StringVar()
        self.category_var = tk.StringVar(value="Movie")
        self.name_var = tk.StringVar()
        self.rating_var = tk.StringVar(value="A")
        self.base_dir = tk.StringVar(value="Sorted_Videos")
        
      
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
       
        self.animate_startup()

    def create_header(self):
        """Create the application header with logo and title"""
        header_frame = tk.Frame(self, bg=self.bg_color, height=80)
        header_frame.pack(fill="x", pady=(20, 10))
        
       
        logo_frame = tk.Frame(header_frame, bg=self.bg_color, width=70, height=70)
        logo_frame.pack(side="left", padx=20)
        
        logo_label = tk.Label(logo_frame, text="🎬", font=("Arial", 40), bg=self.bg_color, fg=self.accent_color)
        logo_label.pack()
        
        
        title_frame = tk.Frame(header_frame, bg=self.bg_color)
        title_frame.pack(side="left")
        
        main_title = tk.Label(title_frame, text="CineSort", font=("Helvetica", 28, "bold"), 
                             bg=self.bg_color, fg=self.accent_color)
        main_title.pack(anchor="w")
        
       
    def create_main_content(self):
        """Create the main content area with cards for different sections"""
        content_frame = tk.Frame(self, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
       
        left_column = tk.Frame(content_frame, bg=self.bg_color)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_column = tk.Frame(content_frame, bg=self.bg_color)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        
        self.create_drop_area(left_column)
        
       
        self.create_sorting_options(right_column)

    def create_drop_area(self, parent):
        """Create the file drop area with visual feedback"""
       
        card = self.create_card(parent, "Select Your Media")
        
        
        self.drop_frame = tk.Frame(card, bg=self.card_color, height=200, relief="flat", bd=2)
        self.drop_frame.pack(fill="x", pady=15, padx=15)
        
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self.on_drop)
        
       
        inner_frame = tk.Frame(self.drop_frame, bg=self.card_color)
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        drop_icon = tk.Label(inner_frame, text="📁", font=("Arial", 36), 
                            bg=self.card_color, fg=self.accent_color)
        drop_icon.pack()
        
        drop_label = tk.Label(inner_frame, text="Drag & Drop Video File", 
                             font=("Helvetica", 14), bg=self.card_color, fg=self.text_color)
        drop_label.pack(pady=5)
        
        drop_sublabel = tk.Label(inner_frame, text="or", font=("Helvetica", 10), 
                                bg=self.card_color, fg=self.text_color)
        drop_sublabel.pack(pady=2)
        
        
        browse_btn = tb.Button(inner_frame, text="Browse Files", bootstyle=(SUCCESS, OUTLINE), 
                              command=self.open_file_dialog, width=15)
        browse_btn.pack(pady=5)
        

        self.file_info_frame = tk.Frame(card, bg=self.card_color)
        self.file_info_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.file_label = tk.Label(self.file_info_frame, text="No file selected", 
                                  font=("Helvetica", 10), bg=self.card_color, fg="gray")
        self.file_label.pack(anchor="w")
        
        
        dir_frame = tk.Frame(card, bg=self.card_color)
        dir_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        dir_label = tk.Label(dir_frame, text="Output Directory:", font=("Helvetica", 11), 
                            bg=self.card_color, fg=self.text_color)
        dir_label.pack(side="left")
        
        dir_entry = tb.Entry(dir_frame, textvariable=self.base_dir, width=20, 
                            font=("Helvetica", 11))
        dir_entry.pack(side="left", padx=5)
        
        dir_btn = tb.Button(dir_frame, text="...", bootstyle=INFO, width=3, 
                           command=self.select_output_dir)
        dir_btn.pack(side="left")

    def create_sorting_options(self, parent):
        """Create the section for sorting options"""
       
        card = self.create_card(parent, "Sorting Options")
        
       
        category_frame = tk.Frame(card, bg=self.card_color)
        category_frame.pack(fill="x", padx=15, pady=10)
        
        category_label = tk.Label(category_frame, text="Media Type:", 
                                font=("Helvetica", 12), bg=self.card_color, fg=self.text_color)
        category_label.pack(anchor="w")
        
        category_options = ["Movie", "Series"]
        category_combo = tb.Combobox(category_frame, textvariable=self.category_var, 
                                    values=category_options, font=("Helvetica", 12), bootstyle=PRIMARY)
        category_combo.pack(fill="x", pady=5)
        
       
        name_frame = tk.Frame(card, bg=self.card_color)
        name_frame.pack(fill="x", padx=15, pady=10)
        
        name_label = tk.Label(name_frame, text="Title:", font=("Helvetica", 12), 
                             bg=self.card_color, fg=self.text_color)
        name_label.pack(anchor="w")
        
        name_entry = tb.Entry(name_frame, textvariable=self.name_var, 
                             font=("Helvetica", 12), bootstyle=PRIMARY)
        name_entry.pack(fill="x", pady=5)
        
        
        rating_frame = tk.Frame(card, bg=self.card_color)
        rating_frame.pack(fill="x", padx=15, pady=10)
        
        rating_label = tk.Label(rating_frame, text="Rating:", font=("Helvetica", 12), 
                               bg=self.card_color, fg=self.text_color)
        rating_label.pack(anchor="w")
        
       
        star_frame = tk.Frame(rating_frame, bg=self.card_color)
        star_frame.pack(fill="x", pady=5)
        
        ratings = ["A", "B", "C", "D", "E"]
        rating_buttons = []
        
        for i, rating in enumerate(ratings):
            btn = tb.Button(star_frame, text=rating, bootstyle=(SUCCESS, OUTLINE), 
                           width=5, command=lambda r=rating: self.set_rating(r))
            btn.pack(side="left", padx=5)
            rating_buttons.append(btn)
        
        self.rating_buttons = rating_buttons
        self.update_rating_buttons()
        
      
        action_frame = tk.Frame(card, bg=self.card_color)
        action_frame.pack(fill="x", padx=15, pady=(15, 20))
        
        cancel_btn = tb.Button(action_frame, text="Reset", bootstyle=(DANGER, OUTLINE), 
                              width=15, command=self.reset_form)
        cancel_btn.pack(side="left", padx=5)
        
        submit_btn = tb.Button(action_frame, text="Sort Media", bootstyle=SUCCESS, 
                              width=15, command=self.submit)
        submit_btn.pack(side="right", padx=5)

    def create_footer(self):
        """Create the application footer"""
        footer = tk.Frame(self, bg=self.bg_color, height=40)
        footer.pack(fill="x", pady=10)
        
        version_label = tk.Label(footer, text="v1.0.0", font=("Helvetica", 8), 
                                bg=self.bg_color, fg="gray")
        version_label.pack(side="right", padx=20)
        
        status_frame = tk.Frame(footer, bg=self.bg_color)
        status_frame.pack(side="left", padx=20)
        
        self.status_indicator = tk.Canvas(status_frame, width=10, height=10, 
                                         bg=self.bg_color, highlightthickness=0)
        self.status_indicator.pack(side="left")
        self.status_indicator.create_oval(2, 2, 8, 8, fill="green", outline="")
        
        self.status_label = tk.Label(status_frame, text="Ready", font=("Helvetica", 8), 
                                    bg=self.bg_color, fg="gray")
        self.status_label.pack(side="left", padx=5)

    def create_card(self, parent, title):
        """Helper function to create a card with title"""
        container = tk.Frame(parent, bg=self.bg_color)
        container.pack(fill="both", expand=True)
        
        
        title_bar = tk.Frame(container, bg=self.accent_color, height=30)
        title_bar.pack(fill="x")
        
        title_label = tk.Label(title_bar, text=title, font=("Helvetica", 12, "bold"), 
                              bg=self.accent_color, fg="white")
        title_label.pack(side="left", padx=15, pady=5)
        
       
        card_content = tk.Frame(container, bg=self.card_color)
        card_content.pack(fill="both", expand=True)
        
        return card_content

    def animate_startup(self):
        """Add subtle animations when the app starts"""
       
        self.attributes("-alpha", 0.0)
        
        def fade_in():
            alpha = self.attributes("-alpha")
            if alpha < 1.0:
                self.attributes("-alpha", alpha + 0.1)
                self.after(20, fade_in)
                
        fade_in()

    def open_file_dialog(self):
        """Open file dialog to select a video file"""
        file_path = filedialog.askopenfilename(
            title="Select a video file", 
            filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov;*.wmv")]
        )
        if file_path:
            self.file_path.set(file_path)
            self.update_file_info(file_path)

    def select_output_dir(self):
        """Open dialog to select output directory"""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.base_dir.set(dir_path)

    def on_drop(self, event):
        """Handle file drop event"""
        file_path = event.data.strip().replace('{', '').replace('}', '')
        if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv')):
            self.file_path.set(file_path)
            self.update_file_info(file_path)
            
           
            orig_bg = self.drop_frame.cget("bg")
            self.drop_frame.config(bg=self.accent_color)
            self.after(100, lambda: self.drop_frame.config(bg=orig_bg))
        else:
            messagebox.showwarning("Invalid File", "Please drop a valid video file")

    def update_file_info(self, file_path):
        """Update the file information display"""
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  
        
        info_text = f"Selected: {file_name} ({file_size:.1f} MB)"
        self.file_label.config(text=info_text, fg=self.accent_color)
        
       
        if not self.name_var.get():
            
            clean_name = os.path.splitext(file_name)[0]
            clean_name = clean_name.replace('_', ' ').replace('-', ' ')
            self.name_var.set(clean_name)

    def set_rating(self, rating):
        """Set the selected rating"""
        self.rating_var.set(rating)
        self.update_rating_buttons()

    def update_rating_buttons(self):
        """Update the rating buttons to show the selected rating"""
        current_rating = self.rating_var.get()
        ratings = ["A", "B", "C", "D", "E"]
        
        for i, btn in enumerate(self.rating_buttons):
            if ratings[i] == current_rating:
                btn.configure(bootstyle=SUCCESS)
            else:
                btn.configure(bootstyle=(SUCCESS, OUTLINE))

    def reset_form(self):
        """Reset all form fields"""
        self.file_path.set("")
        self.name_var.set("")
        self.rating_var.set("A")
        self.update_rating_buttons()
        self.file_label.config(text="No file selected", fg="gray")

    def submit(self):
        """Process the video file"""
        file_path = self.file_path.get()
        category = self.category_var.get()
        name = self.name_var.get().strip()
        rating = self.rating_var.get()
        base_dir = self.base_dir.get()
        
        if not file_path or not category or not name or not rating:
            messagebox.showerror("Missing Information", "All fields must be filled out!")
            return
        
        
        self.status_indicator.create_oval(2, 2, 8, 8, fill="orange", outline="")
        self.status_label.config(text="Processing...")
        
        
        def process_file():
            try:
                dest_path = self.handle_video(file_path, base_dir, category, name, rating)
                
               
                self.after(0, lambda: self.process_complete(True, dest_path))
            except Exception as e:
                
                self.after(0, lambda: self.process_complete(False, str(e)))
        
        threading.Thread(target=process_file).start()

    def handle_video(self, file_path, base_dir, category, name, rating):
        """Move the video file to the appropriate directory"""
        category_path = os.path.join(base_dir, category)
        name_path = os.path.join(category_path, name.lower())
        rating_path = os.path.join(name_path, rating)
        
        os.makedirs(rating_path, exist_ok=True)
        
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(rating_path, file_name)
        
        shutil.move(file_path, dest_path)
        return dest_path

    def process_complete(self, success, message):
        """Handle process completion"""
        if success:
            
            messagebox.showinfo("Success", f"File sorted successfully!\nLocation: {message}")
            
           
            self.reset_form()
            
            
            self.status_indicator.create_oval(2, 2, 8, 8, fill="green", outline="")
            self.status_label.config(text="Ready")
        else:
            
            messagebox.showerror("Error", f"Failed to sort file: {message}")
            
            
            self.status_indicator.create_oval(2, 2, 8, 8, fill="red", outline="")
            self.status_label.config(text="Error")
            
            
            self.after(3000, lambda: (
                self.status_indicator.create_oval(2, 2, 8, 8, fill="green", outline=""),
                self.status_label.config(text="Ready")
            ))

if __name__ == "__main__":
    app = ModernMovieSorter()
    app.mainloop()