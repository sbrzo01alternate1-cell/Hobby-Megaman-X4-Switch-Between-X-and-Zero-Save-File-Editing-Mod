import os
import sys
# Make sure Python finds the package in the current folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import subprocess

#this first line ACTUALLY calls global variables. The "r" at the front stands for real globals:
#I didn't name it "globals" because there is a built in globals() function... but it doesn't work...
from ezGUI.eztkinter import StartProgram
from ezGUI.eztkinter import rglobals
from ezGUI.eztkinter import SetGlobalVariables
from ezGUI.eztkinter import ezWindow
from ezGUI.eztkinter import ezImage
from ezGUI.eztkinter import ezText
from ezGUI.eztkinter import ezLine
from ezGUI.eztkinter import ezRectangle
from ezGUI.eztkinter import ezButton
from ezGUI.eztkinter import ezOval
from ezGUI.eztkinter import ezPolygon
from ezGUI.eztkinter import ezScroll
from ezGUI.eztkinter import ezSound
from ezGUI.eztkinter import ezRadioButtonGroup
from ezGUI.eztkinter import ezFolderInput
from ezGUI.eztkinter import ezInputText
from ezGUI.eztkinter import ezInputTextBox

global SaveFileBinary

def RunCommand(CommandString):
    CommandList = []
    StoreSection = ""
    StoreSection2 = ""
    #print()
    #print()
    #print(CommandString)
    index = 0
    while index < len(CommandString):
        #print(f"CommandString[index]: {CommandString[index]}")
        if CommandString[index] == '"':
            #print("Detected start double quote! Raising index by 1.")
            index = index + 1
            while CommandString[index] != '"' and index < len(CommandString):
            #    print(f"Inside double quote: CommandString[index]: {CommandString[index]}")
                StoreSection2 = StoreSection2 + CommandString[index]
                index = index + 1
            #print("Leaving double quote.")
            #print(f"Left double quote. Raising index by 1")
            index = index + 1
            CommandList.append(f'{StoreSection2}')
            StoreSection2 = ""
            #if index < len(CommandString):
            #    print(f"CommandString[index]: {CommandString[index]}")
        if index < len(CommandString):
            if CommandString[index] != " ":
                StoreSection = StoreSection + CommandString[index]
            else:
                if len(StoreSection) > 0:
                    CommandList.append(StoreSection)
                StoreSection = ""
        index = index + 1
    if len(StoreSection) > 0:
        CommandList.append(StoreSection)
    #print(CommandList)
    subprocess.run(CommandList)

def LaunchGame():
    global SaveFileBinary
    OverwriteSaveFile = False
    if SaveFileBinary[8704] < 2:
        SaveFileBinary[8704] = CharacterSelectOptions1.GetInt()
        OverwriteSaveFile = True
    if SaveFileBinary[8746] < 2:
        SaveFileBinary[8746] = CharacterSelectOptions2.GetInt()
        OverwriteSaveFile = True
    if SaveFileBinary[8788] < 2:
        SaveFileBinary[8788] = CharacterSelectOptions3.GetInt()
        OverwriteSaveFile = True
    if OverwriteSaveFile:
        with open(SaveFilePath, "wb") as f:
            f.write(SaveFileBinary)
    with open("LaunchGameCommand.txt", "r", encoding="utf-8") as file:
        command = file.read().strip().split("\n")[0]
    RunCommand(command)
    with open(SaveFilePath, "rb") as f:
        SaveFileBinary = bytearray(f.read())


def EnterEmulatorCommand():
    if SaveFileBinary[8704] < 2:
        File1Text.hide()
        CharacterSelectOptions1.hide()
        CharacterSelectText1.hide()

    if SaveFileBinary[8746] < 2:
        File2Text.hide()
        CharacterSelectOptions2.hide()
        CharacterSelectText2.hide()

    if SaveFileBinary[8788] < 2:
        File3Text.hide()
        CharacterSelectOptions3.hide()
        CharacterSelectText3.hide()

    LaunchGameButton.hide()
    EnterEmulatorCommandButton.hide()
    global EmulatorCommandTextBox
    if os.path.exists("LaunchGameCommand.txt"):
        with open("LaunchGameCommand.txt", "r", encoding="utf-8") as file:
            DefaultText = file.read().strip().split("\n")[0]
    else:
        DefaultText = "Enter the command to launch the emulator and the game here..."
    EmulatorCommandTextBox = ezInputTextBox(DefaultText, relx=500, rely=600, relwidth=9000, relheight=2000, relfont_size=1500)

    global EmulatorSaveFileTextBox
    if os.path.exists("SaveFilePath.txt"):
        with open("SaveFilePath.txt", "r", encoding="utf-8") as file:
            DefaultText = file.read().strip().split("\n")[0]
    else:
        DefaultText = "Enter the path to the save file here..."
    EmulatorSaveFileTextBox = ezInputTextBox(DefaultText, relx=500, rely=3300, relwidth=9000, relheight=2000, relfont_size=1500)

    global SaveCommandButton
    SaveCommandButton = ezButton("Save Information", relx=3600, rely=8000, relwidth=2500, relheight=500, command=SaveCommand)
    global GoBackButton
    GoBackButton = ezButton("Go Back", relx=4000, rely=8700, relwidth=1500, relheight=500, command=GoBack)
    global EntertheLaunchGameCommandhereText
    EntertheLaunchGameCommandhereText = ezText("Enter the Launch Game Command here:",relx=1000, rely=100, relfont_size=2000)
    global EnterthePathtotheSaveFileHereText
    EnterthePathtotheSaveFileHereText = ezText("Enter the Path to the Save File here:",relx=1000, rely=2700, relfont_size=2000)


def SaveCommand():
    with open("LaunchGameCommand.txt", "w", encoding="utf-8") as file:
        file.write(EmulatorCommandTextBox.GetText())
    with open("SaveFilePath.txt", "w", encoding="utf-8") as file:
        file.write(EmulatorSaveFileTextBox.GetText())

def GoBack():
    global SaveCommandButton
    global GoBackButton
    global EmulatorCommandTextBox
    global EntertheLaunchGameCommandhereText
    global EnterthePathtotheSaveFileHereText
    global EmulatorSaveFileTextBox
    SaveCommandButton.hide()
    GoBackButton.hide()
    EmulatorCommandTextBox.hide()
    EntertheLaunchGameCommandhereText.hide()
    EnterthePathtotheSaveFileHereText.hide()
    EmulatorSaveFileTextBox.hide()
    SaveCommandButton.delete()
    GoBackButton.delete()
    EmulatorCommandTextBox.delete()
    EntertheLaunchGameCommandhereText.delete()
    EnterthePathtotheSaveFileHereText.delete()
    EmulatorSaveFileTextBox.delete()
    SaveCommandButton = None
    GoBackButton = None
    EmulatorCommandTextBox = None
    EntertheLaunchGameCommandhereText = None
    EnterthePathtotheSaveFileHereText = None
    EmulatorSaveFileTextBox = None

    if SaveFileBinary[8704] < 2:
        File1Text.show()
        CharacterSelectOptions1.show()
        CharacterSelectText1.show()

    if SaveFileBinary[8746] < 2:
        File2Text.show()
        CharacterSelectOptions2.show()
        CharacterSelectText2.show()

    if SaveFileBinary[8788] < 2:
        File3Text.show()
        CharacterSelectOptions3.show()
        CharacterSelectText3.show()


    LaunchGameButton.show()
    EnterEmulatorCommandButton.show()
    del SaveCommandButton
    del GoBackButton
    del EmulatorCommandTextBox


if os.path.exists("SaveFilePath.txt"):
    with open("SaveFilePath.txt", "r", encoding="utf-8") as file:
        SaveFilePath = file.read().strip().split("\n")[0]
print(SaveFilePath)

with open(SaveFilePath, "rb") as f:
    SaveFileBinary = bytearray(f.read())

print(SaveFileBinary[8704])
if SaveFileBinary[8704] == 0:
    print("file 1 Current character is X")
    CurrentCharacter1 = "X"
if SaveFileBinary[8704] == 1:
    print("file 1 Current character is Zero")
    CurrentCharacter1 = "Zero"

if SaveFileBinary[8746] == 0:
    print("file 2 Current character is X")
    CurrentCharacter2 = "X"
if SaveFileBinary[8746] == 1:
    print("file 2 Current character is Zero")
    CurrentCharacter2 = "Zero"

if SaveFileBinary[8788] == 0:
    print("file 3 Current character is X")
    CurrentCharacter3 = "X"
if SaveFileBinary[8788] == 1:
    print("file 3 Current character is Zero")
    CurrentCharacter3 = "Zero"

MyezWindow = ezWindow(title="Megaman X4 Swap X and Zero, save file editor",background="#BBBBBB")
MyezScroll = ezScroll()


if SaveFileBinary[8704] < 2:
    File1Text = ezText("File 1:",relx=1000, rely=100, relfont_size=2000)
    CharacterSelectOptions1 = ezRadioButtonGroup(["X", "Zero"], orientation="horizontal", relx=3000, rely=700, relwidth=1500, relheight=500, default_selection=SaveFileBinary[8704])
    CharacterSelectText1 = ezText("Character Select",relx=100, rely=700, relfont_size=1700)

if SaveFileBinary[8746] < 2:
    File2Text = ezText("File 2:",relx=1000, rely=1400, relfont_size=2000)
    CharacterSelectOptions2 = ezRadioButtonGroup(["X", "Zero"], orientation="horizontal", relx=3000, rely=2000, relwidth=1500, relheight=500, default_selection=SaveFileBinary[8746])
    CharacterSelectText2 = ezText("Character Select",relx=100, rely=2000, relfont_size=1700)

if SaveFileBinary[8788] < 2:
    File3Text = ezText("File 3:",relx=1000, rely=2700, relfont_size=2000)
    CharacterSelectOptions3 = ezRadioButtonGroup(["X", "Zero"], orientation="horizontal", relx=3000, rely=3300, relwidth=1500, relheight=500, default_selection=SaveFileBinary[8788])
    CharacterSelectText3 = ezText("Character Select",relx=100, rely=3300, relfont_size=1700)



LaunchGameButton = ezButton("Launch Game", relx=4000, rely=8700, relwidth=2000, relheight=500, command=LaunchGame)
EnterEmulatorCommandButton = ezButton("Enter Emulator Command", relx=3200, rely=9400, relwidth=3500, relheight=500, command=EnterEmulatorCommand)


print()
print()
print()
print(dir(rglobals))
print()
print()
print(MyezWindow)


@SetGlobalVariables
def MainLoop():
    rglobals.root.after(20, MainLoop) #Do the main loop again, but NO DRAWING occurs here.

FPS=30
StartProgram(MainLoop,FPS)



"""
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
#"""