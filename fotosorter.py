import os
import random
import shutil
from dataclasses import dataclass, field
from typing import List, Optional

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}

@dataclass
class ImageState:
    path: str
    offered: List[str] = field(default_factory=list)
    selection: Optional[str] = None  # None => skipped

class FotoSorterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # hide until setup complete
        self.src_dir = filedialog.askdirectory(title="Select folder with pictures to sort")
        if not self.src_dir:
            raise SystemExit("No source directory selected")
        self.dest_dir = filedialog.askdirectory(title="Select destination for sorted folders")
        if not self.dest_dir:
            raise SystemExit("No destination directory selected")
        self.categories: List[str] = []
        self.images: List[ImageState] = []
        self.processed: List[ImageState] = []
        self.current_state: Optional[ImageState] = None
        self.photo_label = None
        self.button_frame = None
        self.skip_button = None
        self.option1_button = None
        self.option2_button = None
        self.photo_cache = None
        self._show_category_window()
        # start the Tk event loop so the category window is displayed
        self.root.mainloop()

    def _show_category_window(self):
        win = tk.Toplevel()
        win.title("Define Categories")
        entries = []
        for i in range(8):
            e = tk.Entry(win, width=30)
            e.grid(row=i, column=0, padx=5, pady=2)
            entries.append(e)
        def start_sorting():
            self.categories = [e.get().strip() for e in entries if e.get().strip()]
            if len(self.categories) < 2:
                messagebox.showerror("Error", "Please provide at least two categories")
                return
            win.destroy()
            self._gather_images()
            self._setup_sort_window()
        tk.Button(win, text="Start Sorting", command=start_sorting).grid(row=8, column=0, pady=10)

    def _gather_images(self):
        for fname in os.listdir(self.src_dir):
            ext = os.path.splitext(fname)[1].lower()
            if ext in SUPPORTED_EXTS:
                path = os.path.join(self.src_dir, fname)
                self.images.append(ImageState(path=path))
        random.shuffle(self.images)
        if not self.images:
            messagebox.showinfo("No images", "No supported images found in the selected folder")
            self.root.destroy()
            raise SystemExit

    def _setup_sort_window(self):
        self.root.deiconify()
        self.root.title("FotoSorter")
        self.photo_label = tk.Label(self.root)
        self.photo_label.pack(expand=True, fill=tk.BOTH)
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)
        self.skip_button = tk.Button(self.button_frame, text="Skip", width=20, command=self._skip)
        self.skip_button.pack(side=tk.LEFT, padx=5)
        self.option1_button = tk.Button(self.button_frame, text="", width=20)
        self.option1_button.pack(side=tk.LEFT, padx=5)
        self.option2_button = tk.Button(self.button_frame, text="", width=20)
        self.option2_button.pack(side=tk.LEFT, padx=5)
        self._next_image()

    def _next_image(self):
        if not self.images:
            self._finish_sorting()
            return
        self.current_state = self.images[0]
        self._display_current_image()
        options = self._pick_options(self.current_state)
        if options is None:
            # no more unique categories; mark as skipped
            self.current_state.selection = None
            self.processed.append(self.images.pop(0))
            self._next_image()
            return
        c1, c2 = options
        self.option1_button.config(text=c1, command=lambda: self._choose(c1))
        self.option2_button.config(text=c2, command=lambda: self._choose(c2))

    def _pick_options(self, state: ImageState):
        remaining = [c for c in self.categories if c not in state.offered]
        if len(remaining) < 2:
            return None
        choices = random.sample(remaining, 2)
        state.offered.extend(choices)
        return choices

    def _display_current_image(self):
        path = self.current_state.path
        img = Image.open(path)
        w, h = img.size
        win_w = self.root.winfo_width() or 800
        win_h = self.root.winfo_height() or 600
        max_w = win_w
        max_h = int(win_h * 0.66)
        img.thumbnail((max_w, max_h))
        self.photo_cache = ImageTk.PhotoImage(img)
        self.photo_label.config(image=self.photo_cache)

    def _choose(self, category):
        self.current_state.selection = category
        self.processed.append(self.images.pop(0))
        self._next_image()

    def _skip(self):
        state = self.current_state
        if len(state.offered) >= len(self.categories):
            state.selection = None
            self.processed.append(self.images.pop(0))
        else:
            # move current image to end of list
            self.images.append(self.images.pop(0))
        self._next_image()

    def _finish_sorting(self):
        result = messagebox.askyesno("Confirm", "Move images to category folders?")
        if result:
            for state in self.images_processed():
                target = state.selection if state.selection else "skipped"
                dest_folder = os.path.join(self.dest_dir, target)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(state.path, dest_folder)
        self.root.destroy()

    def images_processed(self):
        return self.processed

if __name__ == "__main__":
    FotoSorterApp()
