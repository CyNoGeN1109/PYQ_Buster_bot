from bot_token import file_bot_token
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# CONFIG
# =========================

BOT_TOKEN = file_bot_token()
ADMIN_PASSWORD = "PASSWORD#cynogen"

# Chat IDs where admin mode is enabled
ADMIN_SESSIONS = set()

# =========================
# DATA (FINAL – AS YOU GAVE)
# =========================

NEET_PAPERS = {
    "2017": {
        "Set A": "BQACAgUAAxkBAAMUaVJvuxWjlBkmogHYnucaxIRqkTUAAmcfAAKcGplWPwMrA8_jn8E2BA",
        "Set B": "BQACAgUAAxkBAAMVaVJvu5DsE5a1MGeLix-vNnl23j4AAmgfAAKcGplWbK0Z1moyQh42BA",
        "Set C": "BQACAgUAAxkBAAMWaVJvu6PJdzrFU6v3il6aT7fBfl0AAmkfAAKcGplW-uv5yjtxuto2BA",
        "Set D": "BQACAgUAAxkBAAMXaVJvuxZLNsmbrqg_kCiVnOkM09kAAmofAAKcGplWENjp7IL6YdM2BA"
    },
    "2018": {
        "Paper": "BQACAgUAAxkBAAMMaVJvAzqt5Y6h9--cci6K2Iw9QfEAAmAfAAKcGplWLt2GU2u1THE2BA"
    },
    "2019": {
        "Paper": "BQACAgUAAxkBAAMNaVJvA51Y0X0zYyxNVFJVvyTq8EgAAmMfAAKcGplWMsjaWj5yC_o2BA"
    },
    "2020": {
        "Paper": "BQACAgUAAxkBAAMOaVJvA9E9frmzGrvLvuEgFzzvrWcAAmQfAAKcGplWfW3InqADjx02BA"
    },
    "2021": {
        "Paper": "BQACAgUAAxkBAAMSaVJvGFInnz8ckV4vMLCTMEGdqVYAAmUfAAKcGplWwYRT9I926_w2BA"
    },
    "2022": {
        "Paper": "BQACAgUAAxkBAAMKaVJuZ20Y20pNECbo8dGz2XMuI3UAAlYfAAKcGplWzgYkSf2L7cM2BA"
    },
    "2023": {
        "Paper": "BQACAgUAAxkBAAMIaVJuRTRQmKMVl5Nbdihj6aU9XK4AAlUfAAKcGplWfeqCmq8Io-w2BA"
    },
    "2024": {
        "Paper": "BQACAgUAAxkBAAMGaVJsl3c38KzGlWSeIihS9RHt03gAAkwfAAKcGplWjcXOF1lMKBA2BA"
    },
    "2025": {
        "Paper": "BQACAgUAAxkBAAMEaVJsNCdCETy0CXcZVfC5i-ZQiyUAAksfAAKcGplWctd1zUIj9Yo2BA"
    }
}

# =========================
# USER MODE
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📚 Exams", callback_data="EXAMS")]]
    await update.message.reply_text(
        "👋 Welcome to PYQ Bot\nSelect an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "Select Exam:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🧬 NEET", callback_data="NEET")]]
        )
    )

async def show_neet_years(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton(year, callback_data=f"NEET_YEAR_{year}")]
        for year in NEET_PAPERS.keys()
    ]
    await q.edit_message_text(
        "📆 Select Year:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_neet_sets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    year = q.data.replace("NEET_YEAR_", "")
    papers = NEET_PAPERS.get(year, {})
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"NEET_PAPER_{year}_{name}")]
        for name in papers.keys()
    ]
    await q.edit_message_text(
        f"📄 NEET {year} – Select Paper:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_neet_paper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data.replace("NEET_PAPER_", "")
    year, paper_name = data.split("_", 1)
    file_id = NEET_PAPERS.get(year, {}).get(paper_name)

    if not file_id:
        await q.edit_message_text("❌ Paper not found.")
        return

    await context.bot.send_document(
        chat_id=q.message.chat_id,
        document=file_id,
        caption=(
            f"📄 NEET {year} {paper_name} Question Paper\n\n"
            "⚠️ Disclaimer:\n"
            "These question papers are shared for educational purposes.\n"
            "We do not claim ownership.\n\n"
            "🚀 A product of @cynogengroup"
        )
    )

# =========================
# ADMIN MODE
# =========================

async def admin_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Usage: /admin <password>")
        return

    if context.args[0] == ADMIN_PASSWORD:
        ADMIN_SESSIONS.add(update.effective_chat.id)
        await update.message.reply_text(
            "✅ Admin mode ON\nSend any PDF to get its file_id.\nUse /exitadmin to logout."
        )
    else:
        await update.message.reply_text("❌ Wrong password")

async def admin_logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ADMIN_SESSIONS.discard(update.effective_chat.id)
    await update.message.reply_text("🔒 Admin mode OFF")

async def admin_file_id_extractor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id not in ADMIN_SESSIONS:
        return

    if not update.message or not update.message.document:
        return

    file_id = update.message.document.file_id
    await update.message.reply_text(f"FILE_ID:\n{file_id}")

# =========================
# MAIN
# =========================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # User flow
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_exams, pattern="^EXAMS$"))
    app.add_handler(CallbackQueryHandler(show_neet_years, pattern="^NEET$"))
    app.add_handler(CallbackQueryHandler(show_neet_sets, pattern="^NEET_YEAR_"))
    app.add_handler(CallbackQueryHandler(send_neet_paper, pattern="^NEET_PAPER_"))

    # Admin flow
    app.add_handler(CommandHandler("admin", admin_login))
    app.add_handler(CommandHandler("exitadmin", admin_logout))
    app.add_handler(MessageHandler(filters.Document.ALL, admin_file_id_extractor))

    print("🚀 PYQ Bot running | Admin + User mode enabled")
    app.run_polling()

if __name__ == "__main__":
    main()