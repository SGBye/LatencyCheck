import sys
import requests
from skpy import Skype
from getpass import getpass

URL = sys.argv[1]
Tries = int(sys.argv[2])
TotalPing = 0
PingList = []

for i in range(Tries):
    PingList.append(requests.get(URL).elapsed.total_seconds())
    TotalPing += requests.get(URL).elapsed.total_seconds()

AveragePing = TotalPing / Tries
print(getpass())
sk = Skype("xx4epTuKxx", getpass())

ch = sk.contacts["live:ctac1995_2"].chat
ch.sendMsg("Средняя задержка отклика с сайта %s составила %f" % (URL, AveragePing))