import json
import random
from src.instadm import InstaDM
from tkinter import *
import threading
from selenium import webdriver
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient, events, sync
from selenium.webdriver.common.keys import Keys

w = Tk()
w.geometry('500x500')
w.title('Send Messages On Instagram And Whatsapp')
site_label = Label(w, text='Please Enter Site Url To Scrap',
                   bg='Black', fg='white')
site_label.pack(pady=10)
site = Entry(w, bg='black', fg='white', width=40)
site.pack(pady=5)


def scraped():
    r = site.get()
    content = requests.get(r)
    soup = BeautifulSoup(content.content, 'html5lib')
    mess = open('messages.txt', 'r+', encoding="utf-8")
    mess.truncate()
    mess.write(soup.text)


scrap_button = Button(w, text='Scrap The Site',
                      bg='Green', fg='White', command=scraped)
scrap_button.pack(pady=20)

lable = Label(
    w, text='Make Sure You Have Usernames in "username.txt"\nWhatsapp Numbers in "W_Numbers.txt"')
lable.pack(pady=20)

f = open('accounts.json', )
accounts = json.load(f)

with open('usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

with open('messages.txt', 'r') as f:
    messages = f.read()
    print(messages)


def send_message_telegram():
    with open('numbers.txt', 'r') as f:
        for user_details in f:

            api_id = 0000000
            api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
            try:
                client = TelegramClient('session_name', api_id, api_hash)
                client.start()
                client.send_message(user_details, messages)

            except:
                pass


def whatsa():
    driver = webdriver.Chrome('chromedriver.exe')

    with open('W_Numbers.txt', 'r') as f:
        for line in f:
            driver.get(
                f'https://web.whatsapp.com/send?phone={line}&text={messages} text&app_absent=1')
            time.sleep(10)
            send_button = driver.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]')
            send_button.click()
            time.sleep(10)


def start_it():
    while True:
        if not usernames:
            print('Finished usernames.')
            break

        for account in accounts:
            if not usernames:
                break
            # Auto login
            insta = InstaDM(username=account["username"],
                            password=account["password"], headless=False)

            for i in range(1000):

                if not usernames:
                    break

                username = usernames.pop()
                # Send message
                insta.sendMessage(
                    user=username, message=messages)

            insta.teardown()


def thred_instagram():
    threading.Thread(target=start_it).start()


def thred_whatsapp():
    threading.Thread(target=whatsa).start()


button_instagram = Button(w, text='Start The Process For Instagram',
                          bg='Green', fg='white', command=thred_instagram)
button_instagram.pack(pady=20)

button_whatsapp = Button(w, text='Start The Process For whatsapp',
                         bg='Green', fg='white', command=thred_whatsapp)
button_whatsapp.pack(pady=20)

send_button = Button(w, text="Start for Telegram", bg='green',
                     fg='white', command=send_message_telegram)
send_button.pack(pady=20)

w.mainloop()
