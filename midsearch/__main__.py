import glob
import os

import click
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from tqdm import tqdm


ENDPOINT = os.getenv('MIDSEARCH_ENDPOINT', 'http://localhost:5000/api/')


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()


@click.group()
def cli():
    pass


@cli.command()
def telegram():
    app = ApplicationBuilder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()
    app.add_handler(MessageHandler(filters.TEXT, hello))
    app.add_handler(CallbackQueryHandler(button))
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
            requests.post(f'{ENDPOINT}document/' + file_name, data={
                'content': content,
            })


if __name__ == '__main__':
    cli()
