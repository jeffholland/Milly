Welcome to milly! I found that other notepad/journaling/productivity apps just weren't cutting it for me, so I made my own. It's simple, it's customizable, and it's got plenty of keyboard shortcuts (see shortcuts.txt).

For help with the installation, or any other questions, feedback, or bug reports, email holland.musictech@gmail.com.



How to run Milly:

These instructions are only for Mac (Windows instructions are coming soon!)

Because I don't yet have an Apple Developer license, I can't distribute Milly like a typical app. So you can either run it using the Python interpreter (easier but less convenient), or build it as an app to run on your system (harder but more convenient after you've completed the installation process).

First download the source package from Github, move it to the folder you prefer, and...

1. To run milly in the Python interpreter:
    - Make sure you have Python 3 installed - if not, go to https://www.python.org/downloads/ to download and install it. Run "python3 --version" to make sure it's working.
    - Open Terminal or your shell program of choice, cd to the folder where you have placed milly, and run "python3 src/milly.py"
    - Done!

2. To build and install milly as an app on your system:
    - Make sure you have Python 3 installed - if not, go to https://www.python.org/downloads/ to download and install it. Run "python3 --version" to make sure it's working.
    - Follow the Quickstart instructions at https://pyinstaller.org/en/stable/ to install pyinstaller. This will require the use of Terminal or your shell program of choice.
    - From the shell, cd to the folder where you have placed milly, and run "./install.sh". This script will run pyinstaller, create the milly app, move it to your Applications, and open two Finder windows for your convenience - the Applications folder (which should now contain the milly app) and the folder that contains the milly icon (milly.png).
    - Right-click on the milly app and click Get Info. Then drag the milly.png icon to the top-left corner of the info window. This will set the app icon.
    - You can now run the milly app from your Applications folder. Optional, but I recommend dragging it to your dock for maximum convenience.
    - Done! You can now delete the milly source folder if you want. "cd .. && rm -r milly" will do the trick.