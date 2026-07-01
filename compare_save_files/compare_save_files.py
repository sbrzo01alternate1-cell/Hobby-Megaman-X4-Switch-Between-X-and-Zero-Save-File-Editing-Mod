import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print()
print()
print()



#Get the save files:
Original_Binary_Files_1 = os.listdir(f"{script_dir}{os.sep}save_files_1")
Original_Binary_Files_2 = os.listdir(f"{script_dir}{os.sep}save_files_2")
temp_list = []
for MyFile in Original_Binary_Files_1:
    MyFile = f"{script_dir}{os.sep}save_files_1{os.sep}{MyFile}"
    temp_list.append(MyFile)
Binary_Files_1 = temp_list.copy()
temp_list = []
for MyFile in Original_Binary_Files_2:
    MyFile = f"{script_dir}{os.sep}save_files_2{os.sep}{MyFile}"
    temp_list.append(MyFile)
Binary_Files_2 = temp_list.copy()


#Open the save files:
Save_File_Binary = {}
with open(Binary_Files_1[0], "rb") as f:
    Save_File_Binary[f"save_files_1{os.sep}{Original_Binary_Files_1[0]}"] = bytearray(f.read())
with open(Binary_Files_2[0], "rb") as f:
    Save_File_Binary[f"save_files_2{os.sep}{Original_Binary_Files_2[0]}"] = bytearray(f.read())
    


#Get the biggest length:
len1 = len(Save_File_Binary[list(Save_File_Binary.keys())[0]])
len2 = len(Save_File_Binary[list(Save_File_Binary.keys())[1]])
if len1 >= len2:
    Biggest_File = list(Save_File_Binary.keys())[0]
    Smaller_File = list(Save_File_Binary.keys())[1]
elif len2 > len1:
    Biggest_File = list(Save_File_Binary.keys())[1]
    Smaller_File = list(Save_File_Binary.keys())[0]

print(Biggest_File)
print(Smaller_File)

#Increase index by 1 until we reach the length of the biggest file:
print("CHANGES FOUND:")
for index in range(len(Save_File_Binary[Biggest_File])):
    if Save_File_Binary[Biggest_File][index] != Save_File_Binary[Smaller_File][index]:
        Biggest_File_Print = f"[{Biggest_File}]"
        Smaller_File_Print = f"[{Smaller_File}]"
        Index_Print = f"[{index}]"
        print(f"{Biggest_File_Print}{Index_Print} = {Save_File_Binary[Biggest_File][index]}")
        print(f"{Smaller_File_Print}{Index_Print} = {Save_File_Binary[Smaller_File][index]}")
