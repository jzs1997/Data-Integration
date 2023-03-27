import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import sys
import os
from pathlib import Path

import pysftp

BASEURL = "https://scoresdownload.collegeboard.org/pascoredwnld/"
USERNAME = ""
PASSWORD = ""

FTP_USERNAME = ""
FTP_PASSWORD = ""

ISODATEFORMAT = "%Y-%m-%dT%H:%M:%S%z"
FILELIST = []
DLFAILEDLIST = []
TIMEZONE = ZoneInfo("America/Los_Angeles")

FOLDERPATH = Path(__file__).parent

class SatDl():

    def __deleteFile(self, file):
        os.remove(file)
        return 

    def __loadLastExecutedDate(self, dateFile: str)->str:
        with open(dateFile, "r") as fp:
            strDate = fp.read()
        return strDate

    def __getParsedDate(self, tz: datetime.tzinfo)->str:
        nowDate = datetime.fromtimestamp(time.time(), tz=tz)
        return datetime.strftime(nowDate, ISODATEFORMAT)

    def __saveDate(self, strDate: str):
        with open("FromDate.txt", "w") as fp:
            fp.write(strDate)
        return 

    def __copy_to_slate(self, file):
        print(f"Copying file to Slate ftp server.\n")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection('ft.technolutions.net', username=FTP_USERNAME, password=FTP_PASSWORD, cnopts=cnopts) as sftp:
            with sftp.cd('/incoming/testscores'):           # temporarily chdir to testscores directory
                sftp.put(file)  	# upload file to testscores on ftp server
                print(f"File has been copied.\n")

    def __writeFile(self, logFile, method, fileList):
        with open(logFile, method) as fp:
                for file in fileList:
                    fp.writelines(file[0])
                    fp.writelines("\t")
                    fp.writelines(file[1])
                    fp.writelines("\n")
                fp.writelines("\n")
        return 

    def __upDateDownloadHistory(self, logFile, fileList):
        if os.path.exists(logFile) == False:
            self.__writeFile(logFile, "w", fileList)
        else:
            print(f"{logFile} already exists.")
            self.__writeFile(logFile, "a", fileList)
        return 

    def main(self):
        DLFINISHED = True
        #Request the login token
        r = requests.post(BASEURL + "login", json={"username" : USERNAME, "password":PASSWORD})
        token = json.loads(r.text).get("token", "")
        print(token)
        #Request for partial file derectory list since fromDate
        strFromDate = self.__loadLastExecutedDate("FromDate.txt")

        r = requests.post(BASEURL + "files/list", params={"fromDate": strFromDate}, json={"token": token})
        print(r.url)
        data = json.loads(r.text)

        with open("data.json", "w") as fp:
            fp.write(json.dumps(data))

        files = data.get("files", [])

        if(len(files) == 0):
            print("no files to download")
            sys.exit(0)

        for fileInfo in files:
            filename = fileInfo["fileName"]
            newFileName = "SAT_" + filename
            fileSizeKB = fileInfo["fileSize"] / 1000
            deliveryDate = fileInfo["deliveryDate"]
            postfix = newFileName[-3:]

            if postfix == "txt":
                FILELIST.append([newFileName, deliveryDate])
                r = requests.post(BASEURL + "file", params={"filename": filename}, json={"token": token})
                fileUrl = json.loads(r.text).get("fileUrl", "")
                if fileUrl != "":
                    r = requests.get(fileUrl)
                    print("Downloading file {0}, size: {1}KB.".format(newFileName, fileSizeKB))
                    if r.status_code == 200:
                        with open(newFileName, "wb") as fp:
                            fp.write(r.content)
                    else:
                        DLFINISHED = False
                        DLFAILEDLIST.append([newFileName, deliveryDate])
                        print("Error, status code: {}, failed to download file: {}.".format(r.status_code, filename))
                else:
                    print("CollegeBoard Higher Reporting Portal server did not return the fileUrl, failed to download {}.".format(filename))
                    print("Status Code: ", r.status_code)
                    print("Response Info: ", r.text)
                    DLFAILEDLIST.append([newFileName, deliveryDate])
                    DLFINISHED = False

        if DLFINISHED == False:
            print("Failed to download the following files, please download these files manually")
            for fn in DLFAILEDLIST:
                print(fn)

        self.__saveDate(self.__getParsedDate(TIMEZONE))
        self.__upDateDownloadHistory("dlhistory.txt", FILELIST)
        self.__upDateDownloadHistory("failed.txt", DLFAILEDLIST)

        for t in FILELIST:
            self.__copy_to_slate(t[0])
            self.__deleteFile(t[0])


if __name__ == "__main__":
    SatDl().main()

    