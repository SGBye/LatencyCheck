import sys
import requests
from skpy import Skype
from getpass import getpass

URL = sys.argv[1]
Tries = int(sys.argv[2])
TotalPing = 0

for i in range(Tries):
    TotalPing += requests.get(URL).elapsed.total_seconds()

AveragePing = TotalPing / Tries

sk = Skype("ctac1995@gmail.com", getpass())
ch = sk.contacts["xx4eptukxx"].chat
ch.sendMsg("Средняя задержка отклика с сайта %s составила %f" % (URL, AveragePing))