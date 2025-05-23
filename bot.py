from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import TELEGRAM_TOKEN, LINK_ENTREGA
from pagamentos import gerar_link_pagamento
import sqlite3
from datetime import datetime

def salvar_pedido(produto, status, comprador):
    conn = sqlite3.connect("dashboard.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (produto, status, comprador, data) VALUES (?, ?, ?, ?)",
                   (produto, status, comprador, datetime.now().strftime('%Y-%m-%d %H:%M')))
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Comprar", callback_data='comprar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Olá! Bem-vindo ao bot de vendas.\nClique abaixo para comprar:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print(f"➡️ Botão clicado! Dados recebidos: {query.data}")
    if query.data == 'comprar':
        link = gerar_link_pagamento()
        await query.edit_message_text(
            f"Para continuar, clique no link para pagar:\n{link}\n\nApós o pagamento, envie /confirmar"
        )

async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    produto = "Produto X"
    comprador = user.username or user.first_name
    salvar_pedido(produto, "Pago", comprador)
    await update.message.reply_text(f"✅ Pagamento confirmado!\nAqui está seu link de entrega: {LINK_ENTREGA}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("confirmar", confirmar))
    print("Bot rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()
