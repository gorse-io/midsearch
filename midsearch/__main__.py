from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from wechaty import Wechaty, Message, MessageType
from tqdm import tqdm
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

import discord
import openai
import requests
import click
import asyncio
import glob
import os

# openai.proxy = {}
# openai.proxy['http'] = 'http://127.0.0.1:7890'
# openai.proxy['https'] = 'http://127.0.0.1:7890'
openai.proxy = 'http://192.168.101.22:7890'

chat = ChatOpenAI()


ENDPOINT = os.getenv('MIDSEARCH_ENDPOINT', 'http://localhost:5000/api/')


@click.group()
def cli():
    pass

################
# Telegram Bot #
################


async def telegram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = requests.get(
        f"{ENDPOINT}chat",
        params={'message': update.message.text},
        headers={'Accept': 'text/markdown'})
    if r.status_code == 200:
        keyboard = [[
            InlineKeyboardButton("\U0001F44D", callback_data="1"),
            InlineKeyboardButton("\U0001F44E", callback_data="2"),
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_markdown(r.text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(r.text)


async def telegram_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()


@cli.command()
def telegram():
    app = ApplicationBuilder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()
    app.add_handler(MessageHandler(filters.TEXT, telegram_handler))
    app.add_handler(CallbackQueryHandler(telegram_button))
    app.run_polling()


###############
# Discord Bot #
###############

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@cli.command()
def discord():
    client.run(os.getenv('DISCORD_BOT_TOKEN'))


##############
# WeChat Bot #
##############

async def message_handler(message: Message):
    if message.type() == MessageType.MESSAGE_TYPE_TEXT:
        r = chat([HumanMessage(content=message.text())])
        await message.say(r.content)


async def wechaty_main():
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print(
        'Scan QR Code to login: {}\nhttps://wechaty.wechaty.js/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logged in'.format(user)))
    bot.on('message', message_handler)
    await bot.start()


@cli.command()
def wechat():
    asyncio.run(wechaty_main())


@cli.command()
@click.argument('dir')
def ingest(dir: str):
    markdown_files = glob.glob(f'{dir}/*.md')
    for file in tqdm(markdown_files):
        file_name = file[len(dir):]
        if file_name.startswith('/'):
            file_name = file_name[1:]
        with open(file) as f:
            content = ''.join(f.readlines())
            requests.post(f'{ENDPOINT}document/' + file_name, data={
                'content': content,
            })


if __name__ == '__main__':
    cli()
