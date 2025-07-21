from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import pandas as pd
from datetime import datetime
import os
import asyncio
import nest_asyncio
from app import App

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Добрый день!
Я могу помочь Вам с Вашими вопросами по ревматоидному артриту. Мои ответы основаны на последних научных исследованиях. Буду рад помочь!
Но учтите, я не врач и не могу назначать лечение. Лучше всего будет проконсультироваться с врачом''')
    
    # Отправка второго сообщения с аудио
    await update.message.reply_text('''Для начала рекомендую послушать этот небольшой подкаст. 
Он немного погрузит в тему болезни''')
    
    audio_path = '/content/drive/MyDrive/Итоговый проект/data/audio/The Future of Rheumatoid Arthritis Therapies.ogg'
    with open(audio_path, 'rb') as audio_file:
        await update.message.reply_audio(audio_file)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    try:
        app = context.bot_data['app']
        result = app.process_query(user_query)
        if result['type'] == 'video':
            # Сначала отправляем текстовый ответ
            await update.message.reply_text(result['answer'])
            # Затем отправляем видео
            if os.path.exists(result['video_path']):
                with open(result['video_path'], 'rb') as video_file:
                    await update.message.reply_video(video_file)
            else:
                await update.message.reply_text(f'Извините, видеофайл {result["video_path"]} не найден.')
        else:
            await update.message.reply_text(result['answer'])
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        await update.message.reply_text("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.")

def start_tg(TOKEN_TG, OPENAI_API_KEY):
    nest_asyncio.apply()
    app = ApplicationBuilder().token(TOKEN_TG).build()
    app.bot_data['app'] = App(api_key=OPENAI_API_KEY)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()