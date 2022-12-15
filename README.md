# CUCO Installer & Fixer
> This script allows the correction of the CUCO blocked machines by (re)installing the CUCO Agent according to the manufacturer/model of the equipment.
> It is based on the official .bat installation script with some corrections for some machines where CUCO isn't preloaded on Windows and minor bugs

![CUCO Blocked Computer](https://th.bing.com/th/id/R.3936007a23392b96fe80a0b676d2d858?rik=d5ey2KIN9Strhg&riu=http%3a%2f%2fwww.agrupamento-correlha.com%2fwp-content%2fuploads%2f2021%2f06%2f1.jpg&ehk=%2boloRVM1IGWUypsIZROIiDIpr7%2fZyr4hBPsGV3%2f3gCw%3d&risl=&pid=ImgRaw&r=0)


## Instructions
Make sure you are in a PC with at least Windows 10 and in this list
https://cuco.inforlandia.com/bios-and-firmware-compatibility/

### Running from executable file
	1. Disable your antivirus temporarly if it is not Windows Defender since it can cause problems with CUCO
	2. Execute the "Cuco Installer & Fixer.exe" 
	3. Accept the UAC Prompt
	4. Wait for the conclusion of the script and you are good to go

### Running from source (if method 1 fails or you want to run from source)
	1. Install Python 3.11.1. During the installation make sure you check the "Add to Path" option to simplify your life
	2. Open a Command Prompt and execute the following commands to install all the dependencies
		python -m pip install -U setuptools pip
		python -m pip install -U wheel wmi httpx
	3. Disable your antivirus temporarly if it is not Windows Defender since it can cause problems with CUCO
	4. Execute the script by one of this ways: 
		- Right Click it two times if you installed Python Launcher
		- Opening a Command Prompt and executing:
			python source.py
	5. Accept the UAC Prompt
	6. Wait for the conclusion of the script and you are good to go
	





