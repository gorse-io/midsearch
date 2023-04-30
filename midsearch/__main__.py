import click
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
from dotenv import load_dotenv


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


if __name__ == '__main__':
    cli()
