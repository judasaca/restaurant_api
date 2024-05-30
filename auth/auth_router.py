from fastapi import APIRouter

from auth.models import UserSignUp

AuthRouter = APIRouter(prefix="/auth", tags=["Auth routes"])


@AuthRouter.post("/signup", response_model=UserSignUp)
def create_user(user_data: UserSignUp):
    print(user_data)
    return user_data
