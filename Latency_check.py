import math
import os
from typing import List
import requests
import argparse
import time
import pyimgur
from datetime import datetime, timedelta
import matplotlib.pylab as plt
from skpy import Skype
from skpy import SkypeAuthException

from settings import *


def upload_picture():
    """Defines account specifications and uploads the picture
    :return: link to the image
    """
    im = pyimgur.Imgur(IMAGEHOST_ID)
    chart_name = datetime.now().strftime("%H_%M")+'.png'
    uploaded_image = im.upload_image(os.path.join(PATH + chart_name), title="Chart for demonstration")
    return uploaded_image.link


def create_chat(login, password):
    """Defines Skype account and target contact
    :return:
    """
    return Skype(login, password).contacts[SKYPE_CONTACT].chat


def ping_server(site: str, count: int):
    """Sends requests to a *site* web-site and counts the average latency for *count* of tries
    :param site:
    :param count:
    :raises: ConnectionError
    :return: average_ping
    """
    total_ping = 0
    for i in range(count):
        total_ping += requests.get(site).elapsed.total_seconds()
    x = math.ceil((total_ping / count) * 1000)   # переводим в мс
    return x


def make_chart(x, y):
    """builds a chart on the basis of x, y params
    :param x: - data for X axis
    :param y - data for Y axis
    """
    plt.plot(x, y, 'b')  # axis and color
    plt.gcf().autofmt_xdate()
    plt.xlabel('Time')
    plt.ylabel('Ping')
    plt.title('Changes of ping over time')
    chart_name = datetime.now().strftime("%H_%M") + '.png'
    plt.savefig(chart_name, format='png', dpi=CHART_DPI)
    plt.clf()


def system_args():
    """Contains the arguments for the program to run with"""
    parser = argparse.ArgumentParser(description="Latency check")
    parser.add_argument('-url', action="store", dest='url', default="https://google.ru", help="IP or name to ping")
    parser.add_argument('-c', action="store", dest='tries', default=5, type=int, help="Number of tries")
    parser.add_argument('-time', action="store", dest='time_runs', default=60, type=int,
                        help='How long should your programme run')
    return parser.parse_args()


def write_report(name, data: List):
    """Creates a .csv file with *name* name of list *data*
    :param name of a file
    :param data list of dictionaries"""
    with open(name+".csv", "w", newline="") as file:
        file.write("time;ping\n")
        for stats in data:
            file.write(f"{stats['time']:%H:%M:%S};{stats['ping']}\n")


if __name__ == "__main__":
    print(f"* The program started working at {datetime.now():%H:%M:%S}")
    my_login = os.environ.get('MY_LOGIN')
    my_password = os.environ.get('MY_PASSWORD')
    if my_password is None:
        raise SystemExit("Set environment value for MY_PASSWORD and try again.")
    if my_login is None:
        raise SystemExit("Set environment value for MY_LOGIN and try again.")

    parsed_args = system_args()
    tries, url, time_runs = parsed_args.tries, parsed_args.url, parsed_args.time_runs
    date_end = datetime.now() + timedelta(minutes=time_runs)
    data_array = []
    last_report = datetime.now()
    try:
        ch = create_chat(my_login, my_password)
    except SkypeAuthException:
        raise SystemExit("Authentication error. Please, check your Skype login and password!")
    else:
        while datetime.now() < date_end:
            try:
                ping_server_value = ping_server(url, tries)
            except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
                raise SystemExit("Can't connect to the URL, please, try another one.")
            else:
                if ping_server_value > BORDER_PING:
                    ch.sendMsg(f"Средняя задержка отклика с сайта {url} составила {ping_server_value} мс")

                data_array.append({"time": datetime.now(), "ping": ping_server_value})

                if last_report + timedelta(seconds=REPORT_INTERVAL) < datetime.now():
                    last_report = datetime.now()
                    make_chart([i["time"] for i in data_array], [i["ping"] for i in data_array])
                    link = upload_picture()
                    try:
                        ch.sendMsg(f"Отчет за прошедшие 5 минут доступен по ссылке {link}")
                    except SkypeAuthException:
                        print("Check Login and Password settings. If they are correct, try later.")
                    print(f"The report for the past {REPORT_INTERVAL / 60} minutes has been sent to Skype {SKYPE_CONTACT}")
                time.sleep(TRIES_INTERVAL)

        write_report(datetime.now().strftime("%d_%b_%H_%M_%S"), data_array)
        print(f"""Thanks for using my programme! 
The report about the session {datetime.now():%H_%M_%S}.csv has been formed
and placed to the project directory.""")



