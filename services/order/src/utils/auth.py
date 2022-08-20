from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from src.services.user import UserService
from src.utils.hash import verify_password

security = HTTPBasic()


async def basic_auth(credentials: HTTPBasicCredentials = Depends(security),
                     user_service: UserService = Depends()):
    is_pw_correct = False
    user = await user_service.get_by_username(credentials.username)
    if user is not None:
        is_pw_correct = verify_password(credentials.password, user.password)

    if not (user and is_pw_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
