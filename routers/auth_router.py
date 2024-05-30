from fastapi import APIRouter, Response

from models.auth_models import UserSignUp

AuthRouter = APIRouter(prefix="/auth", tags=["Auth routes"])


@AuthRouter.post("/signup", response_model=UserSignUp)
def create_user(user_data: UserSignUp) -> None:
    print(user_data)
