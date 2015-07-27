# Cleanup eagle auto generated files
import os, glob

try:
    currentdir = os.path.realpath(__file__)
    os.chdir(os.path.dirname(currentdir))

    deleteditems = []
    directories = ["AirBoard_Shield", "Base_Shield", "lib"]
    for dir in directories:
        if os.path.isdir(dir):
            os.chdir(dir)
            for file in glob.glob("*.s#*"):
                os.remove(file)
                deleteditems.append(file)
            for file in glob.glob("*.b#*"):
                os.remove(file)
                deleteditems.append(file)
            for file in glob.glob("*.l#*"):
                os.remove(file)
                deleteditems.append(file)
            os.chdir(os.path.dirname(currentdir))

    if deleteditems:
        print("Deleted files:")
        for item in deleteditems:
            print(item)
    else:
        print("Nothing to be done !!")

    os.system('pause')
except ValueError:
    print ValueError
