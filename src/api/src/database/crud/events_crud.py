from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import and_, or_
from typing import Literal, Tuple, Union

from src.api.src.database.models import PrivateClass, PrivateCourse, TutorCourse, Subject, User
from src.core.models import Role


class EventCRUD:
    CompareInt = Union[InstrumentedAttribute[int], int]
    EventType =  Tuple[CompareInt, CompareInt]

    @classmethod
    def event_has_collisions(cls, db: Session, student_id: int, tutor_id: int, start: int, duration: int) -> bool:
        hour_in_ms = 60000

        new_class = (start, start + duration * hour_in_ms)
        old_class = (PrivateClass.start_time_unix, PrivateClass.start_time_unix + PrivateClass.duration * hour_in_ms)

        rows = (
            db
            .query(PrivateClass)
            .join(PrivateClass.private_course)
            .join(PrivateCourse.tutor_course)
            .where(
                or_(
                    PrivateCourse.student_id == student_id,
                    TutorCourse.tutor_id == tutor_id
                )
            )
            .where(
                or_(
                    cls._overlaps(new_class, old_class),
                    cls._overlaps(old_class, new_class),
                    and_(new_class[0] == old_class[0], new_class[1] == old_class[1])
                )
            )
        )

        return rows.count() > 0

    @staticmethod
    def create_class_event(db: Session, private_course_id: int, start_time_unix: int, duration: int) -> PrivateClass:
        new_class = PrivateClass(private_course_id=private_course_id, start_time_unix=start_time_unix, duration=duration)

        db.add(new_class)
        db.commit()
        db.refresh(new_class)

        return new_class

    @staticmethod
    def get_events_between_dates(user_id: int, role: Literal[Role.Tutor, Role.Student], start_time_unix: int, end_time_unix: int, db: Session):
        classes = (
            db
            .query(PrivateClass.id, PrivateClass.duration, PrivateClass.start_time_unix, Subject.name, User.first_name)
            .join(PrivateClass.private_course)
            .join(PrivateCourse.tutor_course)
            .join(TutorCourse.subject)
            .filter(
                start_time_unix <= PrivateClass.start_time_unix,
                end_time_unix >= PrivateClass.start_time_unix
            )
        )

        if role == Role.Tutor:
            classes = (
                classes
                .join(PrivateCourse.student)
                .filter(TutorCourse.tutor_id == user_id)
            )
        else:
            classes = (
                classes
                .join(TutorCourse.tutor)
                .filter(PrivateCourse.student_id == user_id)
            )

        return classes.all()

    @classmethod
    def _overlaps(cls, x: EventType, y: EventType):
        """
        Checks if two events overlap

            x_1 :----: x_2
        y_1 :------------: y_2

        or

        x_1 :------------: x_2
            y_1 :----: y_2
        """

        return or_(
            and_(x[0] > y[0], x[0] < y[1]),
            and_(x[1] > y[0], x[1] < y[1])
        )
