from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

# create user
router = APIRouter(prefix="/users", tags=["users"])


class UserCreateRequest(BaseModel):
    name: str
    email: str



class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str


@router.post("/", response_model=UserResponse)
async def create_user_api(
        user_create_request: UserCreateRequest,
):
    # 아직 저장 로직은 없음
    return UserResponse(
        id=0,
        name=user_create_request.name,
        email=user_create_request.email,
        created_at=str(datetime.now())
=======
@router.get("/", response_model=UserResponse)
async def get_user_api(
        user_id: int,
        user_service=Depends(get_user_service)
):
    user = user_service.get_user(
        user_id=user_id
    )
    return UserResponse(
        id=user.get('id'),
        name=user.get('name'),
        email=user.get('email'),
        created_at=user.get('created_at')

    )
