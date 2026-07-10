import os
import sys
import subprocess
import venv
# Make sure Python finds the package in the current folder
script_dir = os.path.dirname(os.path.abspath(__file__))
venv_dir = os.path.join(script_dir, ".venv")
os.chdir(script_dir)
sys.path.append(script_dir)

if not os.path.exists("ezGUI"):
    print("ezGUI not found. Downloading backend repository...")
    repo_url = "https://github.com/sbrzo01alternate1-cell/Hobby-Python-EZ-GUI.git"
    
    try:
        # Clone the repo into a temporary folder named 'temp_repo'
        subprocess.run(["git", "clone", repo_url, "temp_repo"], check=True)
        
        # Move the ezGUI folder out of the clone into your main directory
        os.rename("temp_repo/ezGUI", "ezGUI")
        
        # Clean up the rest of the cloned repository files
        import shutil
        shutil.rmtree("temp_repo")
        print("ezGUI successfully installed!")
        
    except Exception as e:
        print(f"Error downloading ezGUI: {e}")
        print("Please ensure you have Git installed and an active internet connection.")
        sys.exit(1)

# 1. Check if we are currently running inside a virtual environment
is_venv = sys.prefix != sys.base_prefix
if not is_venv:
    # 2. Check if the folder '.venv' already exists
    if not os.path.exists(venv_dir):
        #print("Creating virtual environment ('.venv'). This takes a moment...")
        try:
            # FIX: with_pip goes here, clear goes in .create()
            builder = venv.EnvBuilder(with_pip=True)
            builder.create(venv_dir)
            print("Virtual environment created successfully!")
        except subprocess.CalledProcessError:
            # Fallback for Steam Deck if system pip is stripped out
            print("Standard pip initialization failed. Creating bare environment...")
            builder = venv.EnvBuilder(with_pip=False)
            builder.create(venv_dir)
            print("Bare virtual environment created! You may need to install pip manually.")
    # Optional: stop execution here so they don't pollute global python
    # sys.exit(0)


# 3. Locate the specific pip executable based on the operating system
if sys.platform == "win32":
    pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
else:
    # Linux (Steam Deck) and macOS
    pip_path = os.path.join(venv_dir, "bin", "pip")

venv_python = pip_path.replace("pip", "python")
try:
    # Running 'python -c "import PIL"' returns exit code 0 if found, non-zero if missing
    subprocess.run([venv_python, "-c", "import PIL"], check=True, capture_output=True)
    Pillow_Installed = True
except (subprocess.CalledProcessError, FileNotFoundError):
    print("Pillow is NOT installed in the virtual environment.")
    Pillow_Installed = False

# 4. Run the virtual environment's pip to install Pillow
if os.path.exists(pip_path):
    venv_python = pip_path.replace("pip", "python")
    if not Pillow_Installed:
        print("Upgrading pip")
        try:
            # We pass -m pip using the venv's python interpreter to ensure it targets the correct path
            # If your fallback skipped pip, we use the absolute pip path directly
            subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            #subprocess.run([venv_python, "-m", "pip", "install", "pillow"], check=True)
            print("Pip successfully upgraded in the virtual environment!")
        except subprocess.CalledProcessError as e:
            pass
            print(f"Failed to update pip automatically: {e}")
            print("You may need to run the installation manually inside the environment.")
    if not Pillow_Installed:
        print("Installing pillow")
        try:
            # We pass -m pip using the venv's python interpreter to ensure it targets the correct path
            # If your fallback skipped pip, we use the absolute pip path directly
            subprocess.run([venv_python, "-m", "pip", "install", "pillow"], check=True)
            print("successfully installed pillow in the virtual environment!")
        except subprocess.CalledProcessError as e:
            pass
            print(f"Failed to install pillow automatically: {e}")
            print("You may need to run the installation manually inside the environment.")
else:
    pass
    print(f"Could not locate pip at {pip_path}. The environment might be incomplete.")

if not is_venv:
    if not Pillow_Installed:
        print()
        print()
        print()
    print("ERROR: The program was not run with its virtual environment. Please relaunch the program with this:")
    if sys.platform == "win32":
        pass
        print(f"{os.path.join(venv_dir, 'Scripts', 'python.exe')} {os.path.abspath(__file__)}")
    else:
        pass
        print(f"{os.path.join(venv_dir, 'bin', 'python')} {os.path.abspath(__file__)}")
    print()
    print("The program is going to crash now. Oopsies...")
    print()



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


