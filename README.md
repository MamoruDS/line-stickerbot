# line-stickerbot
This project is forked from [line-stickerbot](https://github.com/alexskc/line-stickerbot).  
A Telegram bot for downloading Line stickers. It takes a URL sent to the bot from a user, downloads the page, and finds the relevant image links. Then, it downloads the images, rescales them to the appropriate size, and sends them all back to the user in a .zip archive.

## Getting Started
Create your sticker fetch bot via [@BotFather](https://t.me/BotFather) on Telegram.  
Replace `<token>` in `main.py` with the token the `BotFather` gave you, and run `main.py`.  
Send a line sticker shop link to your bot then you will receive stickers with file format.  
After bot fetched all sticker, it will send you a zip arhcive contian all stickers.

## Dependencies

This bot uses a few modules to make my life easier. Run this command if you don't have them.
```shell
pip install -r requirements.txt
```
* `bs4` for parsing the HTML of the sticker page.
* `cssutils` for getting the url of the sticker image.
* `pillow` for resizing the downloaded images.
