from pathlib import Path
import os

def unpacking_data():
    path = Path.cwd()
    packed_data = os.listdir()

    for i in packed_data:
        new_name = i.replace(" ","")
        os.rename(i,new_name)
        if new_name != "main.py":
            os.chdir(f"{i}")
            print(Path.cwd())
            inside_data = os.listdir()
            for x in inside_data:
                os.system(f"move {x} {path}")
            os.chdir(f"{path}")
            os.removedirs(f"{path}\{i}")
            
unpacking_data()