import json
import logging
from time import sleep
import urllib.request
import urllib.parse
import requests
import cssutils
from bs4 import BeautifulSoup
from PIL import Image
from zipfile import ZipFile
from OpenSSL import SSL
import os

cssutils.log.setLevel(logging.CRITICAL)


# This will mark the last update we've checked
try:
    f = open('updatefile', 'r')
    try:
        last_update = int(f.readline().strip())
    finally:
        f.close()
except IOError:
    last_update = 0
# Here, insert the token BotFather gave you for your bot.
TOKEN = '<token>'
# This is the url for communicating with your bot
URL = 'https://api.telegram.org/bot%s/' % TOKEN

# The Line store URL format.
LINE_URL = "https://store.line.me/stickershop/product/"

# The text to display when the sent URL doesn't match.
WRONG_URL_TEXT = ("That doesn't appear to be a valid URL. "
                  "To start, send me a URL that starts with " + LINE_URL)

if not os.path.exists(os.curdir + '/downloads'):
    os.mkdir('downloads')

def dl_stickers(page):
    images = page.find_all('span', attrs={"style": not ""})
    sticker_index = 1
    for i in images:
        imageurl = i['style']
        imageurl = cssutils.parseStyle(imageurl)
        imageurl = imageurl['background-image']
        imageurl = imageurl.replace('url(', '').replace(')', '')
        imageurl = imageurl[1:-15]
        filen = str(last_update) + '_' + str(sticker_index) + '.png'
        urllib.request.urlretrieve(imageurl, './downloads/' + filen)
        resize_sticker(Image.open('./downloads/'+filen), filen)
        sticker_index = sticker_index + 1

def resize_sticker(image, filename):
    edge = image.height if image.height > image.width else image.width
    img = Image.new('RGBA', (edge,edge), color=0)
    img.paste(image, (0,edge-image.height))
    img = img.resize((512,512), Image.LANCZOS)
    img.save('./downloads/' + filename)
    requests.post(URL + 'sendDocument', params=dict(
        chat_id = update['message']['chat']['id']
    ), files=dict(
        document = open('./downloads/' + filename, 'rb')
    ))

def send_stickers(page):
    dl_stickers(page)
    with ZipFile('stickers.zip', 'w') as stickerzip:
        for root, dirs, files in os.walk("downloads/"):
            for file in files:
                stickerzip.write(os.path.join(root, file))
                os.remove(os.path.join(root, file))
    requests.post(URL + 'sendDocument', params=dict(
        chat_id = update['message']['chat']['id']
    ), files=dict(
        document = open('stickers.zip', 'rb')
    ))
    print("sent;)")


# We want to keep checking for updates. So this must be a never ending loop
while True:
    # My chat is up and running, I need to maintain it! Get me all chat updates
    get_updates = json.loads(requests.get(URL + 'getUpdates',
                                          params=dict(offset=last_update)).content.decode())
    # Ok, I've got 'em. Let's iterate through each one
    for update in get_updates['result']:
        # First make sure I haven't read this update yet
        if last_update < update['update_id']:
            last_update = update['update_id']
            f = open('updatefile', 'w')
            f.write(str(last_update))
            f.close()
            # I've got a new update. Let's see what it is.
            if 'message' in update:
                if update['message']['text'][:42] == LINE_URL:
                    # It's a message! Let's send it back :D
                    sticker_url = update['message']['text']
                    user = update['message']['chat']['id']
                    request = requests.get(sticker_url).text
                    stickerpage = BeautifulSoup(request, "html.parser")
                    stickertitle = stickerpage.title.string
                    name = update['message']['from']['first_name']
                    requests.get(URL + 'sendMessage',
                                 params=dict(chat_id=update['message']['chat']['id'],
                                             text="Fetching \"" + stickertitle + "\""))
                    print(name + " (" + str(user) + ")"+ " requested " + sticker_url)
                    send_stickers(stickerpage)
                else:
                    requests.get(URL + 'sendMessage',
                                 params=dict(chat_id=update['message']['chat']['id'],
                                             text=WRONG_URL_TEXT))
    # Let's wait a few seconds for new updates
    sleep(1)


