from telebot.types import Message
from bot.bot_token import bot
from bot.handlers.shared import send_available_subjects
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from bot.handlers.shared import get_subjects
from bot.exception_handler import log_exception
from bot.i18n.i18n import t
from bot.redis.redis_client import r
from bot.handlers.message_handlers.contexts.i_context_base import IContextBase


class Student(IContextBase):
    @staticmethod
    def __guard(func) -> callable:
        def wrapper(message: Message):
            is_student = r.hget(message.from_user.id, "is_student")
            if is_student == "1":
                return func(message.from_user.id)

        return wrapper

    @staticmethod
    @__guard
    def open_classroom(chat_id: int):
        try:
            locale = r.hget(chat_id, "locale")
            markup = ReplyKeyboardMarkupCreator.student_classroom_markup(chat_id, locale)

            bot.send_message(chat_id=chat_id,
                             text=t(chat_id, "YourClassroomIsHere", locale),
                             disable_notification=True,
                             reply_markup=markup)

        except Exception as e:
            log_exception(chat_id, cls.open_classroom, e)

    @staticmethod
    @__guard
    def student_courses(chat_id: int):
        try:
            locale = r.hget(chat_id, "locale")
            get_subjects(chat_id, "student", locale)

        except Exception as e:
            log_exception(chat_id, cls.student_courses, e)

    @staticmethod
    @__guard
    def subscribe_course(chat_id: int):
        try:
            locale = r.hget(chat_id, "locale")
            send_available_subjects(chat_id, locale)

        except Exception as e:
            log_exception(chat_id, cls.subscribe_course, e)
