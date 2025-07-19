import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from transformers import pipeline

# Replace with your bot token from @BotFather
TELEGRAM_TOKEN = "7926638614:AAGYivbmUo0qgnE-Rco3kP5LfJQBdSK1K0o"

logging.basicConfig(level=logging.INFO)
logging.info("Loading local AI model (flan-t5-small)...")

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

def local_ai_answer(prompt: str) -> str:
    try:
        result = qa_pipeline(prompt, max_new_tokens=100)
        return result[0]['generated_text']
    except Exception as e:
        logging.error(f"Local model error: {e}")
        return "Sorry, I couldn't generate a response."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm your offline AI Tutor 🤖. Ask me any question!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    answer = local_ai_answer(user_question)
    await update.message.reply_text(answer)

if __name__ == '__main__':
    logging.info("Starting bot...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
