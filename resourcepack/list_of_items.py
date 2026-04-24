# make a list of items in the folder of textures in /defaultpack/assets/minecraft/textures
import os

path = "defaultpack/assets/minecraft/textures/item"
files = os.listdir(path)

with open("list_of_items.txt", "w") as f:
    for file in files:
        if file.endswith(".png"):
            file = file.replace(".png", "")
            f.write(f"{file}, ")
