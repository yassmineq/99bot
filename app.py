import logging
import threading
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# تسجيل الأخطاء والأنشطة
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# توكن البوت
TOKEN = "8117846251:AAGcT76XbQhm8ViR2yJ7TZu1BdXXxroqROI"

# وقت الانتظار قبل إرسال رابط الإنستغرام (بالثواني)
WAIT_TIME = 300  # 5 دقائق

# قواميس لتتبع المستخدمين والوقت
user_timers = {}

# أمر البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # إنشاء زر
    keyboard = [[InlineKeyboardButton("ابدأ", callback_data="start_pressed")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "اضغط على الزر لزيارة الرابط 👇",
        reply_markup=reply_markup
    )

    # بدء عداد 5 دقائق
    if user_id in user_timers:
        user_timers[user_id].cancel()
    timer = threading.Timer(WAIT_TIME, send_instagram_link, args=(context, user_id))
    user_timers[user_id] = timer
    timer.start()

# عند الضغط على الزر
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # إذا ضغط على الزر، إرسال رابط Google
    if query.data == "start_pressed":
        await query.edit_message_text("🔗 رابطك: https://www.google.com")

        # إلغاء مؤقت الإنستغرام
        if user_id in user_timers:
            user_timers[user_id].cancel()
            del user_timers[user_id]

# إرسال رابط إنستغرام بعد 5 دقائق إذا لم يضغط على الزر
def send_instagram_link(context, user_id):
    asyncio.run_coroutine_threadsafe(
        context.bot.send_message(chat_id=user_id, text="⏳ انتهى الوقت! رابطك: https://www.instagram.com"),
        context.application.loop
    )
    if user_id in user_timers:
        del user_timers[user_id]

# تشغيل البوت
if __name__ == "__main__":
    import asyncio
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("🚀 البوت شغال...")
    app.run_polling()
