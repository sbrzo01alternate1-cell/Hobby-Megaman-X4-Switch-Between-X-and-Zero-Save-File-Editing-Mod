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
    global ErrorTextCommandFailed
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
    try:
        RunCommand(command)
        try:
            ErrorText.hide()
        except:
            pass
    except FileNotFoundError:
        ErrorTextCommandFailed = ezText("ERROR: Command failed. Try entering command again.",relx=100, rely=100, relfont_size=2000, color="red")
    with open(SaveFilePath, "rb") as f:
        SaveFileBinary = bytearray(f.read())


def EnterEmulatorCommand():
    global ErrorTextCommandFailed
    try:
        ErrorTextCommandFailed.hide()
    except:
        pass
    if os.path.exists("SaveFilePath.txt"):
        if os.path.exists(SaveFilePath):
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
        else:
            ErrorText.hide()

    LaunchGameButton.hide()
    EnterEmulatorCommandButton.hide()

    global EntertheLaunchGameCommandhereText
    EntertheLaunchGameCommandhereText = ezText("Enter the Launch Game Command here:",relx=1000, rely=1000, relfont_size=2000)

    global EmulatorCommandTextBox
    if os.path.exists("LaunchGameCommand.txt"):
        with open("LaunchGameCommand.txt", "r", encoding="utf-8") as file:
            DefaultText = file.read().strip().split("\n")[0]
    else:
        DefaultText = "Enter the command to launch the emulator and the game here..."
    EmulatorCommandTextBox = ezInputTextBox(DefaultText, relx=500, rely=1500, relwidth=9000, relheight=2000, relfont_size=1500)

    global EnterthePathtotheSaveFileHereText
    EnterthePathtotheSaveFileHereText = ezText("Enter the Path to the Save File here:",relx=1000, rely=3500, relfont_size=2000)

    global EmulatorSaveFileTextBox
    if os.path.exists("SaveFilePath.txt"):
        with open("SaveFilePath.txt", "r", encoding="utf-8") as file:
            DefaultText = file.read().strip().split("\n")[0]
    else:
        DefaultText = "Enter the path to the save file here..."
    EmulatorSaveFileTextBox = ezInputTextBox(DefaultText, relx=500, rely=4000, relwidth=9000, relheight=2000, relfont_size=1500)

    global SaveCommandButton
    SaveCommandButton = ezButton("Save Information", relx=3600, rely=8000, relwidth=2500, relheight=500, command=SaveCommand)
    global GoBackButton
    GoBackButton = ezButton("Go Back", relx=4000, rely=8700, relwidth=1500, relheight=500, command=GoBack)


def SaveCommand():
    global SaveFileBinary
    global SaveFilePath
    global File1Text
    global CharacterSelectOptions1
    global CharacterSelectText1
    global File2Text
    global CharacterSelectOptions2
    global CharacterSelectText2
    global File3Text
    global CharacterSelectOptions3
    global CharacterSelectText3
    global ErrorText
    with open("LaunchGameCommand.txt", "w", encoding="utf-8") as file:
        file.write(EmulatorCommandTextBox.GetText())
    with open("SaveFilePath.txt", "w", encoding="utf-8") as file:
        file.write(EmulatorSaveFileTextBox.GetText())
    if os.path.exists("SaveFilePath.txt"):
        with open("SaveFilePath.txt", "r", encoding="utf-8") as file:
            SaveFilePath = file.read().strip().split("\n")[0]
        print(SaveFilePath)
        if os.path.exists(SaveFilePath):
            with open(SaveFilePath, "rb") as f:
                SaveFileBinary = bytearray(f.read())
    if os.path.exists(SaveFilePath):
        try:
            ErrorText.hide()
        except:
            pass
        if SaveFileBinary[8704] < 2:
            File1Text = ezText("File 1:",relx=1000, rely=100, relfont_size=2000)
            CharacterSelectOptions1 = ezRadioButtonGroup(["X", "Zero"], orientation="horizontal", relx=3000, rely=700, relwidth=1500, relheight=500, default_selection=SaveFileBinary[8704])
            CharacterSelectText1 = ezText("Character Select",relx=100, rely=700, relfont_size=1700)
            File1Text.hide()
            CharacterSelectOptions1.hide()
            CharacterSelectText1.hide()

        if SaveFileBinary[8746] < 2:
            File2Text = ezText("File 2:",relx=1000, rely=1400, relfont_size=2000)
            CharacterSelectOptions2 = ezRadioButtonGroup(["X", "Zero"], orientation="horizontal", relx=3000, rely=2000, relwidth=1500, relheight=500, default_selection=SaveFileBinary[8746])
            CharacterSelectText2 = ezText("Character Select",relx=100, rely=2000, relfont_size=1700)
            File2Text.hide()
            CharacterSelectOptions2.hide()
            CharacterSelectText2.hide()

        if SaveFileBinary[8788] < 2:
            File3Text = ezText("File 3:",relx=1000, rely=2700, relfont_size=2000)
            CharacterSelectOptions3 = ezRadioButtonGroup(["X", "Zero"], orientation="horizontal", relx=3000, rely=3300, relwidth=1500, relheight=500, default_selection=SaveFileBinary[8788])
            CharacterSelectText3 = ezText("Character Select",relx=100, rely=3300, relfont_size=1700)
            File3Text.hide()
            CharacterSelectOptions3.hide()
            CharacterSelectText3.hide()
    else:
        if (not 'ErrorText' in locals()) and (not 'ErrorText' in globals()):
            ErrorText = ezText("ERROR: Save File Path wasn't found. Try entering\nemulator command again.",relx=100, rely=100, relfont_size=2000, color="red")
        else:
            ErrorText.show()
        
def GoBack():
    global SaveCommandButton
    global GoBackButton
    global EmulatorCommandTextBox
    global EntertheLaunchGameCommandhereText
    global EnterthePathtotheSaveFileHereText
    global EmulatorSaveFileTextBox
    global SaveFileBinary
    global SaveFilePath
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
    if os.path.exists("SaveFilePath.txt"):
        if os.path.exists(SaveFilePath):
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
    if os.path.exists(SaveFilePath):
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

if os.path.exists("SaveFilePath.txt"):
    if os.path.exists(SaveFilePath):
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
    else:
        global ErrorText
        ErrorText = ezText("ERROR: Save File Path wasn't found. Try entering\nemulator command again.",relx=100, rely=100, relfont_size=2000, color="red")
        print(ErrorText)



LaunchGameButton = ezButton("Launch Game", relx=4000, rely=8700, relwidth=2000, relheight=500, command=LaunchGame)
EnterEmulatorCommandButton = ezButton("Enter Emulator Command", relx=3200, rely=9400, relwidth=3500, relheight=500, command=EnterEmulatorCommand)



@SetGlobalVariables
def MainLoop():
    rglobals.root.after(20, MainLoop) #Do the main loop again, but NO DRAWING occurs here.

FPS=30
StartProgram(MainLoop,FPS)


