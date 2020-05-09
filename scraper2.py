import requests
from bs4 import BeautifulSoup

import pickle
import os.path
from time import sleep
import smtplib


URL = "Your kijiji URL"

headers = {"User-Agent": "Fill this"}

kijiji_url = "https://www.kijiji.ca"
saved_file = "apparts.pickle"


def load_apparts():
    if os.path.isfile(saved_file):
        with open(saved_file, "rb") as file:
            apparts = pickle.load(file)
    else:
        apparts = {}
    return apparts


def save_apparts(apparts):
    with open(saved_file, "wb") as file:
        pickle.dump(apparts, file)


def scrape():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.findAll("div", {"class": "search-item"})


def get_data(appart):
    title = appart.findAll("a", {"class": "title"})[0].text.strip()
    price = appart.findAll("div", {"class": "price"})[0].text.replace("$", "").strip()
    url_extension = appart.get("data-vip-url")
    url = kijiji_url + url_extension
    pieces = appart.findAll("div", {"class": "details"})[0].text.replace("Pièces:", "").strip()
    date = appart.findAll("span", {"class": "date-posted"})[0].text.strip()

    dic = {"price": price,
           "pieces": pieces,
           "url": url,
           "date": date
           }

    return title, dic


def send_mail(title, dic):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("your@email.com", "password")

    subject = title
    body = f"Check donc ce nouvel appart :\n{title}\nPrix : {dic['price']}\nPieces : {dic['pieces']}\nURL : {dic['url']}"
    message = f"Subject : {subject}\n\n{body}"

    server.sendmail(
        "your@email.com",
        "destination@email.com",
        message.encode("utf-8")
    )
    print(f"Sent an email for a new appartment : \n{title}")


def main():
    apparts = load_apparts()
    while True:
        scraped_apparts = scrape()
        for appart in scraped_apparts:
            title, dic = get_data(appart)
            if title not in apparts.keys() and "swap" not in title.lower():
                apparts[title] = dic
                send_mail(title, dic)
        save_apparts(apparts)
        print("\nloopdiloop\n")
        sleep(60)


if __name__ == '__main__':
    main()




