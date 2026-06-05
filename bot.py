from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_1 = os.environ.get("CHANNEL_1")
CHANNEL_2 = os.environ.get("CHANNEL_2")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 NeedKYC", callback_data="channel_1")],
        [InlineKeyboardButton("🛍 ShopYourStore", callback_data="channel_2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Bienvenue ! Choisis un canal pour obtenir ton lien d'invitation :",
        reply_markup=reply_markup
    )

from telegram.ext import CallbackQueryHandler

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "channel_1":
        channel_id = CHANNEL_1
        name = "NeedKYC"
    else:
        channel_id = CHANNEL_2
        name = "ShopYourStore"

    link = await context.bot.create_chat_invite_link(channel_id, member_limit=1)
    await query.edit_message_text(f"✅ Ton lien pour *{name}* :\n{link.invite_link}", parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
