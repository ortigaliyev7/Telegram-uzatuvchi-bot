import logging import time from datetime import datetime, timedelta from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

Logger sozlash

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

Link va guruh ID

GROUP_LINK = "https://t.me/xiva_bozorim" ALLOWED_USERS = {}

/start komandasi

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [InlineKeyboardButton("5 ta odamga yuboraman", callback_data='share_5')], [InlineKeyboardButton("10 ta odamga yuboraman", callback_data='share_10')], [InlineKeyboardButton("15 ta odamga yuboraman", callback_data='share_15')] ] reply_markup = InlineKeyboardMarkup(keyboard) await update.message.reply_text("Salom! Nechta odamga guruh linkini yuborasiz?", reply_markup=reply_markup)

Tugmalarni qayta ishlovchi

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()

user_id = query.from_user.id
choice = query.data

if choice.startswith("share_"):
    count = int(choice.split("_")[1])
    ALLOWED_USERS[user_id] = {
        "required_shares": count,
        "shared": 0,
        "can_post": False,
        "post_limit": 3,
        "expires_at": datetime.now() + timedelta(hours=1)
    }
    await query.edit_message_text(
        text=f"Iltimos, quyidagi linkni {count} ta do‘stingizga yuboring:

{GROUP_LINK}\n\nYuborish tugagach, yozish imkoniyati ochiladi." )

/check buyrug‘i — qo‘lda tekshirish uchun

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if user_id not in ALLOWED_USERS: await update.message.reply_text("Siz hali linkni ulashmagansiz.") return

user_data = ALLOWED_USERS[user_id]

if user_data["shared"] >= user_data["required_shares"]:
    user_data["can_post"] = True
    await update.message.reply_text("Tabriklayman! Siz yozishingiz mumkin. Guruhga yozing!")
else:
    await update.message.reply_text(f"Hali {user_data['required_shares'] - user_data['shared']} ta odamga yuborishingiz kerak.")

Har safar linkni yuborganini hisoblash uchun bu yerga ulanish kerak

(Bu qism botni ilgari yozilgan kodga ulab ishlaydi, hozir soddalashtirilgan)

Botni ishga tushurish

if name == 'main': import os TOKEN = os.getenv("8072985796:AAEuLbXMMl6xabUEm8JuJ2nugM5xDpVnBxY")  # Render.com da .env orqali beriladi app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check", check))
app.add_handler(CallbackQueryHandler(button))

print("Bot ishga tushdi...")
app.run_polling()

