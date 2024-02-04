from bot.bot_token import bot
import logging
from bot.handlers import registration, localization
from bot.handlers.tutor import reply_tutor_keyboard, tutor_course_keyboard
from bot.handlers.student import reply_student_keyboard
from bot.handlers.admin import reply_admin_keyboard
from bot.handlers.shared import private_courses, shared


logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


if __name__ == '__main__':
    logging.info('Starting bot..')

    logging.info('Initializing handlers')

    logging.info('Starting polling')
    bot.infinity_polling()
