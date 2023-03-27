## README

### Prerequisite:
+ Python >= 3.10.7
+ Latest version pip

### Usage:

+ If this is the first time for you to use this, run env_install.bat first
+ Execute run.bat
+ Codes will be also available on GitHub, but all usernames and passwords will be removed 
+ For the daily report uploading part, "credentials_upgrads.json" is the core file, and for security concerns, this file is also not available on GitHub repository, you can download it here: https://cloud.google.com/, and follow this instruction:
  + Make sure you are logging in using the Undergrad Admission's Gmail account.
  + Click "Console" on the top-right corner
  + Open the navigation menu, move your mouse cursor onto "APIs & Services", go to "Credentials."
  + Click "Gmail Download"
  + There is a downloading icon in "Client secrets", download the .json file and rename it "credentials_ugrdops.json", put this file in folder "app"
  + Execute the code using command "python app.py", then you need to log in using the ugrops Gmail account manually. 

### Separate Execution

+ First of all, open the Command Prompt or Windows PowerShell, go to the corresponding folder
+ ACT-Run: python main.py
+ SAT: python satdl.py
+ daily_report: python app.py


### Tips on SAT Score uploading

+ If it is your first time to run this script, you should go to slate to check the uploading date of the latest SAT score, and go to file FromDate.txt, replace the date in FromDate.txt with the date of the latest SAT Score file.


### Tips:
+ To avoid uploading duplicated files, you'd better only have one person running this script
