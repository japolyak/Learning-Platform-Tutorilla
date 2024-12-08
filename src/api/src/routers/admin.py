from fastapi import status, APIRouter
from typing import Literal

from src.common.models import UserDto, UserRequestDto, Role, ItemsDto, StatisticsDto

from src.api.src.bot_client.message_sender import send_decline_message
from src.api.src.contexts.db_contex import DbContext
from src.api.src.contexts.user_context import UserContext
from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.user_crud import UserCRUD
from src.api.src.database.crud.admin_crud import AdminCRUD
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(path=APIEndpoints.Admin.RequestsStatistics, status_code=status.HTTP_200_OK,
            response_model=StatisticsDto, summary="Get requests statistics")
async def get_requests_statistics(user: UserContext, db: DbContext):
    if user.role not in [Role.Admin,]:
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    students, tutors = AdminCRUD.requests_statistics(db)

    response_model = StatisticsDto(students_requests=students, tutors_requests=tutors)

    return ResponseBuilder.success_response(content=response_model)


@router.get(path=APIEndpoints.Admin.GetRequests, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[UserRequestDto], summary="Get all requests by role")
async def get_requests(role: Literal[Role.Student, Role.Tutor], user: UserContext, db: DbContext):
    if user.role not in [Role.Admin,]:
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    requests = AdminCRUD.get_users_requests(db=db, role=role)

    if not requests:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    mapped_requests = [UserRequestDto(id=r[0],
                                      user_id=r[1],
                                      user_first_name=r[2],
                                      user_last_name=r[3],
                                      user_email=r[4],
                                      user_role=r[5]
                                      ) for r in requests]

    return ResponseBuilder.success_response(content=ItemsDto[UserRequestDto](items=mapped_requests))


@router.put(path=APIEndpoints.Admin.AcceptRole, status_code=status.HTTP_200_OK, response_model=UserDto,
            summary="Accept user role request")
async def accept_role(request_id: int, user: UserContext, db: DbContext):
    if user.role not in [Role.Admin, ]:
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    db_user = UserCRUD.get_user_by_request_id(db=db, request_id=request_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')
    elif db_user.is_tutor and db_user.is_student:
        return ResponseBuilder.error_response(message='User has all possible roles')

    response_model = UserCRUD.accept_role_request(db=db, request_id=request_id, user=db_user)

    if not response_model:
        return ResponseBuilder.error_response(message='Role request was not found')

    return ResponseBuilder.success_response(content=response_model)


@router.put(path=APIEndpoints.Admin.DeclineRole, status_code=status.HTTP_200_OK, summary="Decline user role request")
async def decline_student_role(request_id: int, user: UserContext, db: DbContext):
    if user.role not in [Role.Admin, ]:
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    db_user = UserCRUD.get_user_by_request_id(db=db, request_id=request_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    declination = UserCRUD.decline_role_request(db=db, request_id=request_id)

    if not declination:
        return ResponseBuilder.error_response(message='Role request was not found')

    send_decline_message(db_user.id)

    return ResponseBuilder.success_response()
