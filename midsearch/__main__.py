import glob
import os

import click
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from tqdm import tqdm

load_dotenv()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply = requests.get(
        "http://localhost:5000/api/chat",
        params={'message': update.message.text},
        headers={'Accept': 'text/markdown'}).text
    await update.message.reply_markdown(reply)


@click.group()
def cli():
    pass


@cli.command()
def telegram():
    app = ApplicationBuilder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()
    app.add_handler(MessageHandler(filters.TEXT, hello))
    app.run_polling()


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
            requests.post('http://localhost:5000/api/document/' + file_name, data={
                'content': content,
            })


if __name__ == '__main__':
    cli()
