from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from src.services.user import UserService
from src.schemas.user import User, UserCreate, UserUpdate, UserBase
from src.utils.auth import basic_auth

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserService = Depends()):
    db_user = await service.get_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="This username already registered!")
    return await service.create(user)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int,
                      user: UserUpdate,
                      service: UserService = Depends(),
                      current_username: str = Depends(basic_auth)):
    db_user = await service.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    if db_user.username != current_username:
        raise HTTPException(status_code=403, detail="You can't update other users data!")

    db_user = await service.get_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="This username already registered!")

    return await service.update(db_user=db_user, user_update=user)


@router.patch("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def patch_username(user_id: int,
                         user: UserBase,
                         service: UserService = Depends(),
                         _: str = Depends(basic_auth)):
    db_user = await service.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    return await service.update_username(db_user=db_user, user=user)


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_all(service: UserService = Depends(),
                  _: str = Depends(basic_auth)):
    db_users = await service.get_all()
    if len(db_users) == 0:
        raise HTTPException(status_code=404, detail="Users not found.")
    return db_users


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int,
                   service: UserService = Depends(),
                   _: str = Depends(basic_auth)):
    db_user = await service.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      service: UserService = Depends(),
                      _: str = Depends(basic_auth)):
    db_user = await service.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await service.delete(db_user)
