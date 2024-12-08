from telebot import service_utils
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from typing import List

from src.common.config import web_app_link
from src.common.redis_configuration import redis_instance as r

from src.bot.src.services.i18n.i18n import t


class ReplyKeyboardMarkupCreator:
    @classmethod
    def main_menu_markup(cls, user_id, locale: str) -> ReplyKeyboardMarkup:
        # TODO - rethink implementation, because KeyboardButton does not pass telegramInitData to front app.
        is_tutor = int(r.hget(user_id, "is_tutor") or 0)
        is_student = int(r.hget(user_id, "is_student") or 0)
        is_admin = int(r.hget(user_id, "is_admin") or 0)
        is_super_admin = int(r.hget(user_id, "is_super_admin") or 0)

        markup = CustomReplyKeyboardMarkup(resize_keyboard=True)

        top_row = []

        if is_tutor or is_student:
            schedule_btn = KeyboardButton(text=t(user_id, "ScheduleIKBtn", locale),
                                          web_app=WebAppInfo(url=f"{web_app_link}/schedule"))
            top_row.append(schedule_btn)

        # if is_tutor:
        #     office_btn = KeyboardButton(text=t(user_id, "OfficeKBtn", locale))
        #     top_row.append(office_btn)
        #
        # if is_student:
        #     classroom_btn = KeyboardButton(text=t(user_id, "ClassroomKBtn", locale))
        #     top_row.append(classroom_btn)

        if top_row.__len__() > 0:
            markup.add_row(top_row)

        if is_admin or is_super_admin:
            admin_panel_btn = KeyboardButton(text=t(user_id, "AdminPanelKBtn", locale),
                                             web_app=WebAppInfo(url=f"{web_app_link}/admin-panel"))
            markup.add(admin_panel_btn)

        # TODO markup.add(profile_btn, support_btn)
        # bottom_row = []
        # profile_btn = KeyboardButton(text=t(user_id, "ProfileKBtn", locale))
        # support_btn = KeyboardButton(text=t(user_id, "SupportKBtn", locale))
        # if bottom_row.__len__() > 0:
        #     markup.add_row(bottom_row)

        return markup

    @classmethod
    def student_classroom_markup(cls, user_id: int, locale: str) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        my_courses_btn = KeyboardButton(text=t(user_id, "MyClassesKBtn", locale))
        add_course_btn = KeyboardButton(text=t(user_id, "SubscribeCourseKBtn", locale))
        main_menu_btn = KeyboardButton(text=t(user_id, "MainMenuKBtn", locale))

        markup.add(my_courses_btn, add_course_btn).add(main_menu_btn)

        return markup

    @classmethod
    def tutor_office_markup(cls, user_id: int, locale: str) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        students_btn = KeyboardButton(text=t(user_id, "StudentsKBtn", locale))
        courses_btn = KeyboardButton(text=t(user_id, "CoursesKBtn", locale))
        add_course_btn = KeyboardButton(text=t(user_id, "AddCourseKBtn", locale))
        main_menu_btn = KeyboardButton(text=t(user_id, "MainMenuKBtn", locale))

        markup.add(students_btn).add(courses_btn, add_course_btn).add(main_menu_btn)

        return markup


class CustomReplyKeyboardMarkup(ReplyKeyboardMarkup):
    def add_row(self, buttons: List[KeyboardButton], row_width=None):
        if row_width is None:
            row_width = self.row_width

        for row in service_utils.chunks(buttons, row_width):
            button_array = []
            for button in row:
                if service_utils.is_string(button):
                    button_array.append({'text': button})
                elif service_utils.is_bytes(button):
                    button_array.append({'text': button.decode('utf-8')})
                else:
                    button_array.append(button.to_dict())
            self.keyboard.append(button_array)

        return self
