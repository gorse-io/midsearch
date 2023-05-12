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
import logging

from discord.ui import View
from dotenv import load_dotenv
from graia.ariadne.message import Source
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import config, HttpClientConfig, WebsocketClientConfig
from graia.ariadne.model import Friend
from tqdm import tqdm
from telegram.constants import MessageEntityType
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.helpers import escape_markdown
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import discord
import click
import requests

load_dotenv()  # take environment variables from .env.

ENDPOINT = os.getenv('MIDSEARCH_ENDPOINT', 'http://localhost:8080/api/')
API_KEY = os.getenv('MIDSEARCH_API_KEY')


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


class Client:

    def __init__(self, endpoint: str, api_key: str):
        if endpoint is None or len(endpoint) == 0:
            raise ValueError("endpoint must not be empty")
        self.endpoint = endpoint
        self.api_key = api_key

    def chat(self, message: str):
        r = requests.post(
            f"{self.endpoint}chat",
            headers={'Accept': 'application/json', 'X-Api-Key': self.api_key},
            data={'message': message})
        r.raise_for_status()
        return r.json()

    def add_document(self, id: str, content: str):
        r = requests.post(
            f"{self.endpoint}document/",
            headers={'Accept': 'application/json', 'X-Api-Key': self.api_key},
            data={'id': id, 'content': content})
        r.raise_for_status()

    def delete_document(self, id: str):
        r = requests.delete(
            f"{self.endpoint}document/",
            params={'id': id},
            headers={'Accept': 'application/json', 'X-Api-Key': self.api_key})
        r.raise_for_status()

    def list_documents(self, n: int = 10, offset: int = 0):
        r = requests.get(
            f"{self.endpoint}documents",
            params={'n': n, 'offset': offset},
            headers={'Accept': 'application/json', 'X-Api-Key': self.api_key})
        r.raise_for_status()
        return r.json()

    def list_all_documents(self):
        offset = 0
        while True:
            documents = self.list_documents(n=100, offset=offset)
            yield from documents
            if len(documents) < 100:
                break
            offset += 100


@click.group()
def cli():
    pass

################
# Telegram Bot #
################


async def telegram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = await context.bot.get_me()
    if update.message.chat.type != 'private':
        if update.message.entities is None or len(update.message.entities) == 0:
            return
        entity = update.message.entities[0]
        if entity.type != MessageEntityType.MENTION:
            return
        mention_username = update.message.text[entity.offset:entity.offset + entity.length]
        if mention_username != f'@{bot.username}':
            return
    logging.info(
        f'Telegram bot received message, user_id={update.message.from_user.username}, chat_type={update.message.chat.type}')
    r = requests.get(
        f"{ENDPOINT}chat",
        params={'message': update.message.text},
        headers={
            'Accept': 'text/markdown',
            'User-Agent': 'Telegram',
            'X-Api-Key': API_KEY,
            'X-User-Id': update.message.from_user.username,
        })
    if r.status_code == 200:
        keyboard = [[
            InlineKeyboardButton("\U0001F44D", callback_data="1"),
            InlineKeyboardButton("\U0001F44E", callback_data="0"),
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_markdown_v2(escape_markdown(r.text, version=2), reply_markup=reply_markup)
    else:
        await update.message.reply_text(r.text)


async def telegram_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    logging.info(f'Telegram bot received button, data={query.data}')
    keyboard = [[
        InlineKeyboardButton(
            "\U0001F60A" if query.data == "1" else "\U0001F44D", callback_data="1"),
        InlineKeyboardButton(
            "\U0001F62D" if query.data == "0" else "\U0001F44E", callback_data="0"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if query.message.reply_markup != reply_markup:
        await query.message.edit_reply_markup(reply_markup)
    else:
        await query.answer()


@cli.command()
def telegram():
    """Start Telegram bot."""
    app = ApplicationBuilder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()
    app.add_handler(MessageHandler(filters.TEXT, telegram_handler))
    app.add_handler(CallbackQueryHandler(telegram_button))
    app.run_polling()


###############
# Discord Bot #
###############

intents = discord.Intents.default()
client = discord.Client(intents=intents)


class RatingView(View):

    def __init__(self, conversation_id: str):
        super().__init__()
        self.conversation_id = conversation_id

    @discord.ui.button(emoji='👍')
    async def upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info(
            f'Discord bot received button, conversation_id={self.conversation_id}')
        await interaction.response.defer()
        await interaction.message.remove_reaction('👎', client.user)
        await interaction.message.add_reaction('👍')

    @discord.ui.button(emoji='👎')
    async def downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info(
            f'Discord bot received button, conversation_id={self.conversation_id}')
        await interaction.response.defer()
        await interaction.message.remove_reaction('👍', client.user)
        await interaction.message.add_reaction('👎')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user or message.content == '':
        return
    logging.info(f'Discord bot received message, user_id={message.author}')
    r = requests.get(
        f"{ENDPOINT}chat",
        params={'message': message.content},
        headers={
            'Accept': 'text/markdown',
            'User-Agent': 'Discord',
            'X-Api-Key': API_KEY,
            'X-User-Id': str(message.author),
        })
    if r.status_code == 200:
        conversation_id = r.headers.get('X-Conversation-Id')
        await message.channel.send(r.text, view=RatingView(conversation_id))
    else:
        await message.channel.send(r.text)


@cli.command()
def discord():
    """Start Discord bot."""
    client.run(os.getenv('DISCORD_BOT_TOKEN'))


#############
# Mirai Bot #
#############


app = Ariadne(config(
    int(os.getenv('MIRAI_BOT_QQ')),
    os.getenv('MIRAI_VERIFY_KEY'),
    HttpClientConfig(os.getenv('MIRAI_HTTP_URL')),
    WebsocketClientConfig(os.getenv('MIRAI_WS_URL')),
))


@app.broadcast.receiver("FriendMessage")
async def friend_message_listener(app: Ariadne, friend: Friend, chain: MessageChain):
    logging.info(f'Mirai bot received message, user_id={friend.id}')
    r = requests.get(
        f"{ENDPOINT}chat",
        params={'message': str(chain)},
        headers={
            'Accept': 'text/markdown',
            'User-Agent': 'Mirai',
            'X-Api-Key': API_KEY,
            'X-User-Id': str(friend.id),
        })
    await app.send_message(friend, r.text)


@cli.command()
def mirai():
    Ariadne.launch_blocking()


@cli.command()
@click.argument('dir')
@click.option('-v', '--verbose', is_flag=True)
def sync(dir: str, verbose: bool = False):
    """Sync markdown files (Non-existing files will be deleted)."""
    client = Client(ENDPOINT, API_KEY)
    # List all documents in the server.
    existed_documents = {document['id']
                         for document in client.list_all_documents()}
    # List all documents in the local.
    markdown_files = glob.glob(f'{dir}/**/*.md', recursive=True)
    for file in tqdm(markdown_files, desc='Update documents', disable=verbose):
        file_name = file[len(dir):]
        if file_name.startswith('/'):
            file_name = file_name[1:]
        if verbose:
            print(f'Update {file_name}')
        with open(file) as f:
            content = ''.join(f.readlines())
            client.add_document(file_name, content)
        existed_documents.discard(file_name)
    # Delete non-existing documents.
    for document_id in tqdm(existed_documents, desc='Delete documents', disable=verbose):
        if verbose:
            print(f'Delete {document_id}')
        client.delete_document(document_id)


@cli.command()
@click.argument('dir')
@click.option('-v', '--verbose', is_flag=True)
def add(dir: str, verbose: bool = False):
    """Add markdown files (Non-existing files will be keeped)."""
    client = Client(ENDPOINT, API_KEY)
    markdown_files = glob.glob(f'{dir}/**/*.md', recursive=True)
    for file in tqdm(markdown_files, desc='Add documents', disable=verbose):
        file_name = file[len(dir):]
        if file_name.startswith('/'):
            file_name = file_name[1:]
        if verbose:
            print(f'Add {file_name}')
        with open(file) as f:
            content = ''.join(f.readlines())
            client.add_document(file_name, content)


if __name__ == '__main__':
    cli()
