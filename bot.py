import logging
import random
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from deep_translator import GoogleTranslator
import nest_asyncio

nest_asyncio.apply()


# 🔹 Вставте ваші API-токени
TELEGRAM_TOKEN = "8155784197:AAGzjgSTvjImosbbWVSxUgI9HcLRH3qLN0A"
OPENAI_API_KEY = "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"

# 🔹 Логування
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔹 Ініціалізація ChatGPT API
openai.api_key = OPENAI_API_KEY

# 📌 База відповідей (100 унікальних)
motivation = [f"Мотивація {i}: Використовуй Python на максимум! 🐍" for i in range(1, 101)]
jokes = [f"Жарт {i}: Парсер працює, але чи працює він добре? 🤔" for i in range(1, 101)]
support = [f"Підтримка {i}: Ти впораєшся, навіть якщо `import pandas` не спрацював! 💪" for i in range(1, 101)]
prediction = [f"Передбачення {i}: Сьогодні тобі доведеться переробляти звіт 3 рази! 📊" for i in range(1, 101)]

# 📌 Функція для команди /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👋 Привіт! Я бот-аналітик. Ось що я вмію:\n"
        "🟢 /motivation – Мотивація\n"
        "🟢 /joke – Жарт\n"
        "🟢 /support – Підтримка\n"
        "🟢 /prediction – Передбачення\n"
        "🟢 Напиши будь-яке питання, і я спробую відповісти! (ChatGPT 🤖)"
    )

# 📌 Обробка команд
async def get_response(update: Update, context: CallbackContext) -> None:
    command = update.message.text[1:]  # Видаляємо "/"
    responses = {
        "motivation": motivation,
        "joke": jokes,
        "support": support,
        "prediction": prediction
    }
    if command in responses:
        await update.message.reply_text(random.choice(responses[command]))

# 📌 Інтеграція з ChatGPT API
async def chatgpt_response(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        chatgpt_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(chatgpt_reply)
    except Exception as e:
        await update.message.reply_text("⚠ Виникла помилка при отриманні відповіді від ChatGPT.")

# 📌 Переклад тексту
async def translate_text(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text.replace("/translate ", "")
    translated_text = GoogleTranslator(source="auto", target="en").translate(user_text)
    await update.message.reply_text(f"🔠 Переклад: {translated_text}")

# 📌 Основна функція запуску бота
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["motivation", "joke", "support", "prediction"], get_response))
    app.add_handler(CommandHandler("translate", translate_text))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_response))  # Обробка тексту ChatGPT

    print("✅ Бот запущений...")
    app.run_polling()

if __name__ == "__main__":
    main()
