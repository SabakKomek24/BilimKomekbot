from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = '8000747163:AAF8BnG3ixJz8x1r6c8d6r5_NQ4m5egpXuU'

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Қай сынып? / Какой класс?")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_data:
        user_data[chat_id] = {'step': 'class', 'class': '', 'subject': '', 'task': ''}

    step = user_data[chat_id]['step']

    if step == 'class':
        user_data[chat_id]['class'] = text
        user_data[chat_id]['step'] = 'subject'
        await update.message.reply_text("Қай пән? / Какой предмет?")
    elif step == 'subject':
        user_data[chat_id]['subject'] = text
        user_data[chat_id]['step'] = 'task'
        await update.message.reply_text("Тапсырманы жазыңыз / Напишите задание")
    elif step == 'task':
        user_data[chat_id]['task'] = text
        await update.message.reply_text("Как решение будет готово, отправим вам.")
        # тут ты получаешь задание
        print(f"Новое задание от @{update.effective_user.username or 'неизвестно'}")
        print("Сынып / Класс:", user_data[chat_id]['class'])
        print("Пән / Предмет:", user_data[chat_id]['subject'])
        print("Тапсырма / Задание:", user_data[chat_id]['task'])

        user_data[chat_id]['step'] = 'class'  # сброс для нового задания

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
