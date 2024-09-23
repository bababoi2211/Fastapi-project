from pathlib import Path
import os
# packing all the file of the folder
path = Path.cwd()
data = (os.listdir())

for i in data:   
    #region check for space in the name
    new_name = i.replace(" ","")
    os.rename(i,new_name)
    #endregion
    text =i.split(".")[-1:]
    str_text = "".join(text)

    if str_text != "py":   
        os.makedirs(f"{path}\{str_text} ",exist_ok=True)
        print(f"{path}\{str_text}")
        # os.system(f"move {i} {str_text}")
        os.system(f"move {new_name} {str_text}")
# # print(os.readlink(r"C:\Users\DANI\Desktop\Session01"))


#UNPACKING ALLL THE FOLDERS
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
            
# unpacking_data()