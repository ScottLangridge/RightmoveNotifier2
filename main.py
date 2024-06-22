from bs4 import BeautifulSoup
import requests
import re
from time import sleep

from secrets import secrets

def get_property_ids():
    content = requests.get(secrets["url"]).content
    soup = BeautifulSoup(content, "html.parser")

    property_ids = [i.attrs["id"].strip("property-") for i in soup.find_all('div', id=re.compile(r'^property-\d+$'))]
    return set(property_ids)


def notify(property_ids):
    title = "New properties on your search!"
    msg = "New properties on your search:\n"
    for pid in property_ids:
        msg += "www.rightmove.co.uk/properties/" + pid + "\n"

    url = 'https://api.pushover.net/1/messages.json'
    post_data = {'user': secrets["user_token"], 'token': secrets["api_token"], 'title': title, 'message': msg}
    response = requests.post(url, data=post_data)
    print(response)


def main_loop():
    seen_ids = set()

    while True:
        try:
            fetched_ids = get_property_ids()
            unseen_ids = fetched_ids - seen_ids
            seen_ids.update(unseen_ids)
            if len(unseen_ids) > 0:
                notify(unseen_ids)

        except:
            pass

        sleep(60)


main_loop()
