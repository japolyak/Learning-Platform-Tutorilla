from telebot import service_utils
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from typing import Literal, List

from src.common.config import web_app_link
from src.common.models import PaginatedList, SubjectDto, Role, PrivateClassDto, ClassStatus, BlaTutorCourseDto

from src.bot.src.enums import Emoji
from src.bot.src.handlers.callback_query_handler.callback_prefix import CallBackPrefix
from src.bot.src.services.i18n.i18n import t
from src.common.redis_configuration import redis_instance as r


class InlineKeyboardMarkupCreator:
    @classmethod
    def main_menu_markup(cls, user_id, locale: str) -> InlineKeyboardMarkup:
        # TODO - remove it from here!
        is_tutor = int(r.hget(user_id, "is_tutor") or 0)
        is_student = int(r.hget(user_id, "is_student") or 0)
        is_admin = int(r.hget(user_id, "is_admin") or 0)
        is_super_admin = int(r.hget(user_id, "is_super_admin") or 0)

        markup = CustomInlineKeyboardMarkup()

        top_row = []

        if is_tutor or is_student:
            schedule_btn = InlineKeyboardButton(text=t(user_id, "ScheduleIKBtn", locale),
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
            admin_panel_btn = InlineKeyboardButton(text=t(user_id, "AdminPanelKBtn", locale),
                                                   web_app=WebAppInfo(url=f"{web_app_link}/admin-panel"))
            markup.add(admin_panel_btn)

        # TODO markup.add(profile_btn, support_btn)
        # bottom_row = []
        # profile_btn = KeyboardButton(text=t(user_id, "ProfileKBtn", locale))
        # support_btn = KeyboardButton(text=t(user_id, "SupportKBtn", locale))
        # if bottom_row.__len__() > 0:
        #     markup.add_row(bottom_row)

        return markup

    @staticmethod
    def locale_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        english = InlineKeyboardButton("English", callback_data=f"{CallBackPrefix.SetUserLocale} en-US")

        markup.add(english)

        return markup

    @staticmethod
    def timezone_markup(locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        plus_one = InlineKeyboardButton("Central Europe - Warsaw, Paris, Barcelona",
                                        callback_data=f"{CallBackPrefix.SetTimeZone} 2 {locale}")
        plus_two = InlineKeyboardButton("East Europe - Kyiv, Bucharest, Helsinki",
                                        callback_data=f"{CallBackPrefix.SetTimeZone} 3 {locale}")

        markup.add(plus_one)
        markup.add(plus_two)

        return markup

    @staticmethod
    def choose_occupation(user_id: int, locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        teacher_btn = InlineKeyboardButton(text=t(user_id, "TeachIKBtn", locale),
                                           callback_data=f"{CallBackPrefix.BecomeTutor} {locale}")
        student_btn = InlineKeyboardButton(text=t(user_id, "StudyIKBtn", locale),
                                           callback_data=f"{CallBackPrefix.BecomeStudent} {locale}")

        markup.add(teacher_btn, student_btn)

        return markup

    @staticmethod
    def subjects_panel_markup(courses: List[BlaTutorCourseDto], user_id: int, locale: str) -> InlineKeyboardMarkup:
        # TODO - rewrite with paging
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=f"{c.subject_name} - {c.price}$",
                                 callback_data=f"{CallBackPrefix.GetTutorCoursesForPanel} {c.id} {locale}"))
            for c
            in courses]

        markup.add(InlineKeyboardButton(text=t(user_id, "ReturnToOfficeIKBtn", locale),
                                        callback_data=f"{CallBackPrefix.BackToOffice} {locale}"))

        return markup

    @staticmethod
    def  subjects_markup(subjects: List[SubjectDto], role: Literal[Role.Tutor, Role.Student], query_info: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=subject.name, switch_inline_query_current_chat=f"{role} {query_info}_{subject.name}"))
            for subject
            in subjects]

        return markup

    @staticmethod
    def add_course_markup(courses: List[SubjectDto], locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name,
                                 callback_data=f"{CallBackPrefix.AddCourse} {course.id} {course.name} {locale}"))
            for course
            in courses]

        return markup

    @staticmethod
    def sub_course_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Subscribe_{course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def subscribe_course_markup(course_id: int, user_id: int, locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        subscribe_btn = InlineKeyboardButton(text=t(user_id, "SubscribeIKBtn", locale),
                                             callback_data=f"{CallBackPrefix.SubscribeCourse} {course_id} {locale}")
        return_btn = InlineKeyboardButton(text=t(user_id, "ReturnToSelectSubjectsIKBtn", locale),
                                          callback_data=f"{CallBackPrefix.ReturnToSelect} {locale}")

        markup.add(subscribe_btn).add(return_btn)

        return markup

    @staticmethod
    def private_course_markup(
            private_course_id: int,
            role: Literal[Role.Tutor, Role.Student],
            locale,
            user_id: int,
            hide_all_classes_btn=False
    ) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        if web_app_link is not None:
            # TODO - think about adding role to an url
            plan_class_btn = InlineKeyboardButton(text=t(user_id, "PlanClassIKBtn", locale),
                                                  web_app=WebAppInfo(url=f"{web_app_link}/private-course/{private_course_id}"))
            markup.add(plan_class_btn)

        if not hide_all_classes_btn:
            all_classes_btn = InlineKeyboardButton(text=t(user_id, "AllClassesIKBtn", locale),
                                                   callback_data=f"{CallBackPrefix.CourseClasses} {private_course_id} {role} {locale}")
            markup.add(all_classes_btn)

        back_btn = InlineKeyboardButton(text=t(user_id, "BackIKBtn", locale),
                                        callback_data=f"{CallBackPrefix.BackToChoosePrivateCourse} {role} {locale}")

        markup.add(back_btn)

        return markup

    @staticmethod
    def course_classes_markup(paginated_list: PaginatedList[PrivateClassDto], go_back_id: int, role: str,
                              inline_message_id: str, locale: str, user_id: int) -> InlineKeyboardMarkup:
        markup = CustomInlineKeyboardMarkup()

        for i in paginated_list.items:
            callback_data = f"{CallBackPrefix.PrivateClass} {i.id} {locale}"
            button_date = i.schedule_datetime.strftime("%d-%m-%Y %H:%M")

            match i.status:
                case ClassStatus.Paid:
                    button_text = f"{Emoji.ClassPaid.value} {button_date}"
                case ClassStatus.Occurred:
                    button_text = f"{Emoji.ClassOccurred.value} {button_date}"
                case _:
                    button_text = f"{Emoji.ClassScheduled.value} {button_date}"

            markup.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

        back_btn_text = f"{Emoji.BackArrow.value}"
        current_btn_text = f"{paginated_list.current_page}/{paginated_list.pages}"
        next_btn_text = f"{Emoji.NextArrow.value}"

        back_btn_callback = f"{CallBackPrefix.LoadPage} {paginated_list.current_page - 1} {go_back_id} {role} {inline_message_id} {locale}" if paginated_list.current_page > 1 else CallBackPrefix.EmptyCallback
        current_btn_callback = CallBackPrefix.EmptyCallback
        next_btn_callback = f"{CallBackPrefix.LoadPage} {paginated_list.current_page + 1} {go_back_id} {role} {inline_message_id} {locale}" if paginated_list.current_page < paginated_list.pages else CallBackPrefix.EmptyCallback

        row = [
            InlineKeyboardButton(text=back_btn_text, callback_data=back_btn_callback),
            InlineKeyboardButton(text=current_btn_text, callback_data=current_btn_callback),
            InlineKeyboardButton(text=next_btn_text, callback_data=next_btn_callback),
        ]

        markup.add_row(row)

        back_to_course_btn_callback = f"{CallBackPrefix.BackToPrivateCourse} {go_back_id} {inline_message_id} {role} {locale}"

        markup.add(
            InlineKeyboardButton(text=f"{Emoji.BackArrow.value} {t(user_id, "BackToCourseIKBtn", locale)}",
                                 callback_data=back_to_course_btn_callback
                                 )
        )

        return markup

    @staticmethod
    def course_markup(user_id: int, locale: str, tutor_course_id: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        # textbooks = InlineKeyboardButton(text=t(user_id, "TextbooksIKBtn", locale),
        #                                  callback_data=f"{CallBackPrefix.CourseTextbooks} {locale} {tutor_course_id}")
        # add_textbooks = InlineKeyboardButton(text=t(user_id, "AddTextbooksIKBtn", locale),
        #                                      callback_data=f"{CallBackPrefix.AddTextbooks} {locale} {tutor_course_id}")
        back = InlineKeyboardButton(text=t(user_id, "BackToCoursesIKBtn", locale),
                                    callback_data=f"{CallBackPrefix.BackToCourses} {locale}")

        # markup.add(textbooks, add_textbooks).add(back)
        markup.add().add(back)

        return markup


class CustomInlineKeyboardMarkup(InlineKeyboardMarkup):
    def add_row(self, buttons: List[InlineKeyboardButton], row_width=None):
        if row_width is None:
            row_width = self.row_width

        for row in service_utils.chunks(buttons, row_width):
            button_array = [button for button in row]
            self.keyboard.append(button_array)

        return self
