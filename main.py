from pyrogram import filters, Client
import configparser
from typing import Optional
from datetime import datetime
import logging
import csv

config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["api"]["id"]
api_hash = config["api"]["hash"]

app = Client("parsing", api_id, api_hash, sleep_threshold=2)
link = input("Enter chat link (may be empty): ")
trigger = input("Enter trigger message: ")

logging.basicConfig(filename="bot.log", level=logging.ERROR)

print("Starting interception...")


async def parsing(client, message: Optional, chat_link: Optional):
    if chat_link is not None:
        target = str((await client.get_chat(chat_link)).id)
        print(target)
    else:
        target = str(message.chat.id)

    if target is not None:
        filename = (
            f"{message.chat.title}_{message.chat.id}_{str(datetime.now())}.csv".replace(
                ":", "_"
            )
        )
        with open(
            file=filename,
            mode="w",
            newline="",
            encoding="utf-16",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(
                ["id", "first_name", "last_name", "user", "phone", "is_bot"]
            )
            async for member in client.get_chat_members(target):
                writer.writerow(
                    [
                        member.user.id,
                        member.user.first_name,
                        member.user.last_name,
                        member.user.username,
                        member.user.phone_number,
                        member.user.is_bot,
                    ]
                )
        print(f"Saved to {filename}. Exiting.")
        exit(0)
    else:
        print("The chat link has expired, please try again")
        client.loop.close()
    exit(0)


@app.on_message(filters.me & filters.text)
async def on_message_trigger(cli, msg):
    if msg.text != trigger:
        return

    print(f"Gotcha! Chat ID: {msg.chat.id};\tChat Name: {msg.chat.title}")

    if link == "":
        await parsing(client=app, message=msg, chat_link=None)
    else:
        await parsing(client=app, message=None, chat_link=link)


app.run()
