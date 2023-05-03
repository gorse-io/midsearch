# Copyright 2023 MidSearch Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import os

from tqdm import tqdm
from telegram.constants import MessageEntityType
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import discord
import click
import requests


ENDPOINT = os.getenv('MIDSEARCH_ENDPOINT', 'http://localhost:8080/api/')


@click.group()
def cli():
    pass

################
# Telegram Bot #
################


async def telegram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type != 'private' and (
            update.message.entities is None or len(update.message.entities) == 0 or update.message.entities[0].type != MessageEntityType.MENTION):
        return
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
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    r = requests.get(
        f"{ENDPOINT}chat",
        params={'message': message.content},
        headers={'Accept': 'text/markdown'})
    await message.channel.send(r.text)


@cli.command()
def discord():
    client.run(os.getenv('DISCORD_BOT_TOKEN'))


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
