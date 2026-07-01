#First set the variables you want:
Save_File_Path = "/home/deck/.local/share/duckstation/memcards/Mega Man X4 (USA)_1.mcd"
Character_To_Set = "x" #Or Zero
command = [
    "/home/deck/Desktop/configure/appimages/DuckStation-x64.AppImage",
    "--appimage-extract-and-run",
    "/run/media/deck/Nintendo_Hates_S/configure/roms/Megaman X4 [SLUS-00561]/Megaman X4.bin"
]



import subprocess
#Open the save file path as binary:
with open(Save_File_Path, "rb") as f:
    Save_File_Binary = bytearray(f.read())

#Get the current character. This is set at character 8704. Refer to compare_save_files.py to see how I found that:
if Save_File_Binary[8704] == 0:
    print("Current character is X")
    Current_Character = "X"
if Save_File_Binary[8704] == 1:
    print("Current character is Zero")
    Current_Character = "Zero"

#See if we actually need to swap the characters:
if Character_To_Set.lower() == Current_Character.lower():
    print("Characters are the same, nothing to do. Opening game:")
    subprocess.Popen(command)
else:
    print("Swapping characters.")
    if Character_To_Set.lower() == "x":
        Save_File_Binary[8704] = 0
    else:
        Save_File_Binary[8704] = 1
    print("Saving file:")
    with open(Save_File_Path, "wb") as f:
        f.write(Save_File_Binary)
    print("Saved! Opening game:")
    subprocess.Popen(command)
