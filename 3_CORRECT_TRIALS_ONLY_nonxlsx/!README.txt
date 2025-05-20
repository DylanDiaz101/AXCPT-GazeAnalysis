This script was written by Dylan M. Diaz (dylandiaz101@yahoo.com | https://github.com/DylanDiaz101/AXCPT-GazeAnalysis)
>>>>>>> df0cb06 (update README files)
for the CSUSB Learning Research Institute under directions from PI: Dr. Jason Reimer
(jreimer@csusb.edu)

----------------------------------- DIRECTIONS TO RUN PROGRAM -------------------------

To run program, add your eprime .gazedata files into !INPUT then run main.py

After running, make sure to clear !INPUT, and !OUTPUT folders!


----------------------------------- FIRST TIME SETUP ----------------------------------
IF YOU ARE RUNNING THIS PROGRAM FOR THE FIRST TIME YOU MUST FOLLOW THE FOLLOWING STEPS:

1. 
Install Python3 if you have not done so already on your system
Be sure that upon loading the installation window that you tick/check the
"Add Python 3.X to PATH" option.
You can install Python here: https://www.python.org/

2. Open main.py on your IDE or Python IDLE 
(right click main.py --> edit with --> Python IDLE)

3. Open command prompt (if on windows) or terminal (if on mac)

4. 
If on Windows run the following commands:

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

and then

python get-pip.py

If on MacOS run the following command:

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

5. now enter each of these commands separately and let each download:

If on Windows:
	
	pip install numpy

	pip install pandas

	pip install openpyxl

	pip install matplotlib

If on MacOs/Linux you may have to install using sudo commands (i.e sudo pip3 install numpy):

	pip3 install numpy

	pip3 install pandas

	pip3 install openpyxl

	pip3 install matplotlib


6. run the module (FN + F5 on MacOS, F5 on Windows and wait until finished)

7. Check the !OUTPUT folder for the final results

8. Clear the !INPUT and !OUTPUT folders for the next run

9. Done!

-------------------------------- COMMON ERRORS ---------------------------------

1. Warnings?
You may see warnings output when running the script, this is expected and not a worry.

2. File/Path not found errors or similar
ENSURE that you have the !INPUT and !OUTPUT folders AND they must be named accordingly. 
The program will not work otherwise.

3. 
Output xlsx is blank OR getting unexpected outputs/results?

Please ensure your !INPUT folder is actually populated with the files you want to convert.

4. Python not found or python not defined/is not a recognized command etc.
Please reinstall Python3 at https://www.python.org/ and make sure upon starting the .exe for the installation, at the bottom of the screen you will see "Add Python 3.X to PATH", TICK/CHECK this option and then hit install now.

5. pip is not a recognized command or similar error regarding pip
Please check steps 3, 4 and 5 in the FIRST TIME SETUP section above
See here for more detailed steps:
Windows - https://www.geeksforgeeks.org/how-to-install-pip-on-windows/
Mac - https://www.geeksforgeeks.org/how-to-install-pip-in-macos/