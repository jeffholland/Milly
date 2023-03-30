==========================================

Welcome to milly! I found that other notepad/journaling/productivity apps just weren't cutting it for me, so I made my own. It's simple, it's customizable, and it's got plenty of keyboard shortcuts (see shortcuts.txt).

For help with the installation, or any other questions, feedback, or bug reports, email holland.musictech@gmail.com.

<<<<<<< HEAD
====================================================================
=======
==========================================

>>>>>>> 5d81f1ecc1cb7a4e4781ca62457cbb97ff4802be


==========================================

<<<<<<< HEAD
Because I don't have an Apple Developer license, I can't distribute Milly like a typical app. So you can either run it using the Python interpreter, or build it as an app to run on your system. (If you want to do the second method, I recommend trying the first method first, just to make sure the app runs properly on your system).
=======
Platform notes:
>>>>>>> 5d81f1ecc1cb7a4e4781ca62457cbb97ff4802be

MAC: Milly was mainly developed on Mac and has been tested on Intel and Apple Silicon Macs, so you should be golden.

WINDOWS: You should be able to follow along with Git Bash or Cygwin or another Unix shell client. With Windows command prompt, you're on your own.

LINUX OR ANYTHING ELSE: Good luck.

==========================================


==========================================

How to install milly:

First, clone the source package from Github. Then, make sure you have Python 3 installed. If not, go to https://www.python.org/downloads/ to download and install it. From the Terminal, run "python3 --version" to make sure it's working. 
    (Troubleshooting: If you get an "xcrun error", you may need to install command line developer tools by running the command "xcode-select --install").

1. To run milly in the Python interpreter:
    - Open Terminal or your shell program of choice, cd to the folder where you have placed milly, and run "python3 src/milly.py" (or "py src/milly.py" on Windows). Done!

2. To build and install milly as an app on your system:
    - Follow the Quickstart instructions at https://pyinstaller.org/en/stable/ to install pyinstaller.
    - On Mac, run "./install.sh". This script will run pyinstaller, create the milly app, move it to your Applications, and open two Finder windows for your convenience - the Applications folder (which should now contain the milly app) and the folder that contains the milly icon (milly.png). Right-click on the milly app and click Get Info. Then drag the milly.png icon to the top-left corner of the info window. This will set the app icon. You can now run the milly app from your Applications folder. Optional, but I recommend dragging it to your dock for maximum convenience.
        (Troubleshooting: if the script fails because it says "pyinstaller not found", first run "python3 -m PyInstaller myscript.py" and then run ./install.sh again)
<<<<<<< HEAD
    - Right-click on the milly app and click Get Info. Then drag the milly.png icon to the top-left corner of the info window. This will set the app icon.
    - You can now run the milly app from your Applications folder. Optional, but I recommend dragging it to your dock for maximum convenience.
    - Done! You can now delete the milly source folder if you want. "cd .. && rm -r milly" will do the trick. Or if you want to keep the source code but remove those extra build folders, run "rm -rf build dist".
=======
    - On Windows, run "pyinstaller --onefile src/milly.py", cd to the dist folder, and run "explorer .". This should open the dist folder in File Explorer and you can run the .exe file by double-clicking on it. You can drag it to your Taskbar (or whatever they're calling it these days) for maximum convenience.
    - Done! You can now delete the milly source folder if you want. "cd .. && rm -r milly" will do the trick.

==========================================
>>>>>>> 5d81f1ecc1cb7a4e4781ca62457cbb97ff4802be
