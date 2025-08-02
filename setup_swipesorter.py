import os
import json

project_name = "SwipeSorter"
categories = ["memes", "wallpapers", "trash"]

# Create project directory
os.makedirs(project_name, exist_ok=True)

# Create main.py with basic GUI stub
main_py_content = '''\
import os
import shutil
from tkinter import *
from PIL import Image, ImageTk
import json

# Load config
with open("categories.json") as f:
    CATEGORIES = json.load(f)

SOURCE_DIR = "unsorted"
files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
index = 0

def move_image(direction):
    global index
    if index >= len(files): return
    file = files[index]
    src = os.path.join(SOURCE_DIR, file)
    dest_dir = CATEGORIES.get(direction)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(src, os.path.join(dest_dir, file))
    index += 1
    load_image()

def load_image():
    if index >= len(files):
        label.config(text="No more images!")
        return
    img_path = os.path.join(SOURCE_DIR, files[index])
    img = Image.open(img_path)
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

root = Tk()
root.title("SwipeSorter")

image_label = Label(root)
image_label.pack()

Button(root, text="⬅ Left", command=lambda: move_image("left")).pack(side=LEFT)
Button(root, text="⬇ Down", command=lambda: move_image("down")).pack(side=LEFT)
Button(root, text="➡ Right", command=lambda: move_image("right")).pack(side=LEFT)

label = Label(root, text="")
label.pack()

load_image()
root.mainloop()
'''

with open(os.path.join(project_name, "main.py"), "w") as f:
    f.write(main_py_content)

# Create categories config
categories_config = {
    "left": "wallpapers",
    "right": "memes",
    "down": "trash"
}
with open(os.path.join(project_name, "categories.json"), "w") as f:
    json.dump(categories_config, f, indent=4)

# Create README
with open(os.path.join(project_name, "README.md"), "w") as f:
    f.write("# SwipeSorter\n\nSort your unsorted images into categories with swipe-like gestures.\n")

# Create unsorted folder and category folders
unsorted_path = os.path.join(project_name, "unsorted")
os.makedirs(unsorted_path, exist_ok=True)

for cat in categories:
    os.makedirs(os.path.join(project_name, cat), exist_ok=True)

print(f"Project '{project_name}' set up successfully.")
