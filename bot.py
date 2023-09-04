from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

import random

# Состояния бота
START, SELECT_OPPONENT, DUEL = range(3)

# Словарь для хранения пар "пользователь - оппонент"
opponent_dict = {}

# Функция для команды /start
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Привет! Я бот для дуэлей. Используй команду /shot, чтобы вызвать на дуэль кого-то из участников чата.")
    return START

# Функция для начала дуэли
def select_opponent(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Кого хотите вызвать на дуэль? Пожалуйста, укажите никнейм пользователя.")
    return SELECT_OPPONENT

# Функция для завершения дуэли и выбора победителя
def duel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    opponent_username = update.message.text

    # Проверяем, существует ли оппонент
    if opponent_username not in opponent_dict:
        update.message.reply_text("Оппонент не найден. Попробуйте еще раз.")
        return SELECT_OPPONENT

    opponent = opponent_dict[opponent_username]

    # Случайным образом выбираем победителя
    winner = random.choice([user, opponent])
    loser = opponent if winner == user else user

    update.message.reply_text(f"Победитель дуэли: {winner.mention_html()}!")
    update.message.reply_text(f"Проигравший дуэли: {loser.mention_html()}!")

    del opponent_dict[opponent_username]  # Удаляем оппонента из словаря

    return START

# Функция для обработки команды /shot
def shot(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Кого хотите вызвать на дуэль? Пожалуйста, укажите никнейм пользователя.")
    return SELECT_OPPONENT

# Функция для обработки ответов пользователей
def handle_text(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    opponent_username = update.message.text

    # Сохраняем оппонента в словаре
    opponent_dict[opponent_username] = user

    update.message.reply_text(f"Вы вызвали на дуэль {opponent_username}. Подождем, пока {opponent_username} ответит.")
    
    return DUEL

def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    updater = Updater(6145836799:AAEM_sBepc3AsTZHC7bWkMnT_Nx_PA78--I, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('shot', shot)],
        states={
            START: [MessageHandler(Filters.regex(r'^/shot$'), shot)],
            SELECT_OPPONENT: [MessageHandler(Filters.text & ~Filters.command, handle_text)],
            DUEL: [MessageHandler(Filters.text & ~Filters.command, duel)]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
