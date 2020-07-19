import csv
from threading import Thread
import threading
import schedule
import time
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import smtplib 
import os.path
from os import path
import pandas as pd

class MailServer(Thread):
    thread_stop = False

    def __init__(self, app_input):
        super(MailServer, self).__init__()
        print('MailServer -> init')
        self.scheduler = schedule.Scheduler()
        self.app = app_input
        if path.exists("userID.csv"):
            df=pd.read_csv("userID.csv")
            self.mail=Mail(self.app)
            self.__email=df['email'].tolist()
            self.__state=df['state'].tolist()
            self.__district=df['district'].tolist()
            self.__case=df['case'].tolist()
            self.__cured=df['cured'].tolist()
            self.__active=df['active'].tolist()
            self.__death=df['death'].tolist()
        else:
            self.__email = []

    def send_email(self):
        print("send_email -> call", threading.get_ident())
        with self.app.app_context():
            for id in range(len(self.__email)):
                msg=Message("COVID-19 Stats",
                    sender="dshrishikesh@gmail.com",
                    recipients=[self.__email[id]])
                
                msg.body="State: {} \nDistrict: {} \nCases: {} \nCured: {} \nActive: {} \nDeath: {} \n".format(self.__state[id], self.__district[id], self.__case[id], self.__cured[id], self.__active[id], self.__death[id])
                self.mail.send(msg)

    def run(self):
        print("mail_server -> started", threading.get_ident())
        self.scheduler.every().day.at("01:17").do(self.send_email)
        # self.scheduler.every(30).seconds.do(self.send_email)
        # self.send_email()
        while not self.thread_stop:
            self.scheduler.run_pending() 
            time.sleep(1) 