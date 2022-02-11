import argparse
import requests as r
from datetime import datetime
from subprocess import Popen#,CREATE_NEW_CONSOLE
import os

url = "https://ws.engr.illinois.edu/labtrack/computers.asp?lab=C4D3EACD-BAEA-4E70-8D23-3A80B66F60EF"
linkdata = r.get(url)
data = linkdata.json()['data']
time_format = "%m/%d/%Y %H:%M:%S %p"
def createRDPfiles(computer_n:int):
    n = f"0{computer_n}"if computer_n < 10 else str(computer_n)
    base = f"""
allow desktop composition:i:1
allow font smoothing:i:1
alternate shell:s:
audiocapturemode:i:0
audiomode:i:0
authentication level:i:0
autoreconnection enabled:i:1
bandwidthautodetect:i:1
bitmapcachepersistenable:i:1
compression:i:1
connection type:i:7
desktopheight:i:1200
desktopwidth:i:1920
disable cursor setting:i:0
disable full window drag:i:0
disable menu anims:i:0
disable themes:i:0
disable wallpaper:i:0
displayconnectionbar:i:1
drivestoredirect:s:*
enableworkspacereconnect:i:0
full address:s:ECEB-3026-{n}.EWS.ILLINOIS.EDU
gatewaybrokeringtype:i:0
gatewaycredentialssource:i:4
gatewayhostname:s:rdpgateway.illinois.edu
gatewayprofileusagemethod:i:1
gatewayusagemethod:i:2
kdcproxyname:s:
keyboardhook:i:2
negotiate security layer:i:1
networkautodetect:i:1
prompt for credentials:i:0
promptcredentialonce:i:1
rdgiskdcproxy:i:0
redirectclipboard:i:1
redirectcomports:i:0
redirectposdevices:i:0
redirectprinters:i:1
redirectsmartcards:i:1
remoteapplicationmode:i:0
screen mode id:i:2
session bpp:i:32
shell working directory:s:
smart sizing:i:1
use multimon:i:0
use redirection server name:i:0
videoplaybackmode:i:1
winposstr:s:0,3,0,0,1280,720
    """
    with open(f"ECEB-3026-{n}.EWS.ILLINOIS.EDU.rdp","w") as f:
        f.write(base)
class Computer:
    def __init__(self,computer_name,last_login, last_logout,n):
        self.occupied = True
        self.name = computer_name
        self.number =n
        # print(last_login)
        self.dt_login = datetime.strptime(last_login,time_format)
        self.dt_logout =  datetime.strptime(last_logout,time_format)
        if self.dt_login < self.dt_logout:
            self.occupied = False
    def __str__(self):
        return self.name
    def __int__(self) -> int:
        return self.number
    def cleanPrint(self):
        colour = 31 if self.occupied else 32
        print(f"\033[1;{colour}m{self.number}\033[0m    ",end="")
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--command","-cmd",default="None",help="Run only a specific command",type=str,choices=["Display","Connect"])
    args = parser.parse_args()
    # print(args)
    l = []
    rows = [[]*8]
    cou =0
    for comp in data:
        
        c = Computer(comp['computer'],comp['last_login'],comp['last_logoff'],cou+1)
        l.append(c)
        cou +=1
    # print(l)
    del l[-1]
    backboi = l.copy()

        
    backboi.reverse()
    if args.command =="Display" or args.command == "None":
        for c in backboi:
            c.cleanPrint()
            if int(c) % 5 ==0:
                print(" ")
        print("\n")
    # cmd run
    if args.command !="Connect" and args.command != "None":
        quit()
    myList = os.listdir(os.getcwd())
    print(len(myList))
    if len(myList) !=48:
        gen = input("Create rdp files? Y/N if no you will have to download from the website")
        if gen.upper() == "Y":
            for x in range(1,44):  #there are 44 computers
                createRDPfiles(x)
        myList = os.listdir(os.getcwd())
        if  len(myList) ==0:
            raise("Empty Directory install possible lab machines to the same directory")
    first_empty = None
    for c in backboi:
        # print(f"{str(c).upper()}.rdp")
        if not c.occupied and f"{str(c).upper()}.rdp" in myList:
            first_empty = str(c).upper()
    if first_empty is not None:
        print(first_empty)
        a = Popen(f"mstsc /v:{first_empty}")#,creationflags=CREATE_NEW_CONSOLE)
    else:
        print("Couldn't connect!")

    input()
