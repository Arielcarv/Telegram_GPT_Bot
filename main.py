import os
import openai
import logging
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from telegram import Update
from datetime import datetime


API_TOKEN=os.getenv('API_TOKEN')
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    echo = f"{update.message.text[6:]} {update.message.text[-3:] * 2}" 
    await context.bot.send_message(chat_id=update.effective_chat.id, text=echo)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can use the following commands: \n"
        "  - /echo <msg-to-repeat>\n"
        "  - /start\n"
        "  - /help\n"
        "  - /gpt <your question>\n"
    )


def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Update {update} caused the error {context.error}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    if user_message in ["hi", "hello", "coé", "oi"]:
        await update.message.reply_text(f"Hello, how can I help you?")
    if user_message in ["time?", "time", "hora"]:
        await update.message.reply_text(f" TIME - {datetime.now()}")
    # return f"You sent the following: {user_message}"


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    question = str(update.message.text[5:].capitalize())
    print(f"QUESTION: {question}")
    response = chatGPT_message(question)
    await update.message.reply_text(
        f"Question: {question}.\n"
        f"Answer: {response['choices'][0]['message']['content']}"
    )


def chatGPT_message(question):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{question}"},
        ]
    )
    return response


if __name__=='__main__':
    application = ApplicationBuilder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("gpt", gpt))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_error_handler(CommandHandler("error", error))

    application.run_polling()
