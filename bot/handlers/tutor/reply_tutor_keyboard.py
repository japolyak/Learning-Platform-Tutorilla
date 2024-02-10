from telebot.types import Message, CallbackQuery
from bot.api.clients.tutor_client import TutorClient
from bot.bot_token import bot
from bot.markups.inline_keyboard_markups import InlineKeyboardMarkupCreator
from bot.markups.reply_keyboard_markup import ReplyKeyboardMarkupCreator
from ...api.api_models import SubjectDto
from ...enums import CallBackPrefix
from .shared import get_tutor_subjects


@bot.message_handler(regexp="Office")
def restore_redis(message: Message):
    markup = ReplyKeyboardMarkupCreator.tutor_office_markup()
    bot.send_message(chat_id=message.from_user.id, text="Office is here", disable_notification=True, reply_markup=markup)


@bot.message_handler(regexp="My courses")
def my_courses(message: Message):
    get_tutor_subjects(message.from_user.id)


@bot.message_handler(regexp="Add course")
def add_course(message: Message):
    request = TutorClient.available_subjects_tutor(user_id=message.from_user.id)

    if not len(request.json()):
        bot.send_message(chat_id=message.from_user.id, text="No available subjects", disable_notification=True)
        return

    response_data = [SubjectDto(**s) for s in request.json()]

    if not len(response_data):
        bot.send_message(chat_id=message.from_user.id, text="No available subjects", disable_notification=True)
        return

    msg_text = "Choose course to teach"

    markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)

    bot.send_message(chat_id=message.from_user.id, text=msg_text, disable_notification=True, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: (call.data.startswith(CallBackPrefix.AddCourse)))
def add_course_callback(call: CallbackQuery):
    subject_id = int(call.data.split(" ")[1])

    request = TutorClient.add_course(user_id=call.from_user.id, subject_id=subject_id)

    if not request.ok:
        request = TutorClient.available_subjects_tutor(user_id=call.from_user.id)

        response_data = [SubjectDto(**s) for s in request.json()]

        markup = InlineKeyboardMarkupCreator.add_course_markup(courses=response_data)
        bot.send_message(chat_id=call.from_user.id, text="Oops, try again or try later",
                         disable_notification=True, reply_markup=markup)
        return

    bot.send_message(chat_id=call.from_user.id, text="Course added successfully", disable_notification=True)
