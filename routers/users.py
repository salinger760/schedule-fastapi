from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from lib.auth_utils import AuthJwtCsrf
from fastapi_csrf_protect import CsrfProtect
import schemas.user as user_schema
import schemas.auth as autu_schema
import cruds.user as user_crud


router = APIRouter(prefix="/users", tags=["Users"])
auth = AuthJwtCsrf()


@router.get("/{user_id}", response_model=user_schema.User)
async def read_user(
    req: Request, res: Response, user_id: int, db: AsyncSession = Depends(get_db)
):
    print("-------------user_id")
    db_user = await user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/email/", response_model=user_schema.User)
async def read_user_email(
    req: Request,
    res: Response,
    user: user_schema.UserEmail,
    db: AsyncSession = Depends(get_db),
):
    user_data = jsonable_encoder(user)
    db_user = await user_crud.get_user_by_email(db, email=user_data["email"])
    print("-------------email")
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[user_schema.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    users = await user_crud.get_users(db, skip=skip, limit=limit)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@router.post("/", response_model=user_schema.User)
async def create_user(
    req: Request,
    res: Response,
    user: user_schema.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user_data = jsonable_encoder(user)
    db_user = await user_crud.get_user_by_email(db, email=user_data["email"])

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await user_crud.create_user(db=db, user=user)


@router.get("/current/", response_model=autu_schema.TokenData)
def get_user_refresh_jwt(req: Request, res: Response):
    new_token, subject = auth.verify_update_jwt(req)
    res.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )
    return {"email": subject}


@router.put("/{user_id}", response_model=user_schema.UserCreateResponse)
async def update_user(
    req: Request,
    res: Response,
    user_id: int,
    user_body: user_schema.UserUpdate,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    new_token = auth.verify_csrf_update_jwt(req, csrf_protect, req.headers)
    print("-----------------------1")
    user = await user_crud.get_user(db, user_id=user_id)
    print(user)
    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )
    
    print("-----------------------2")
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    print("-----------------------3")
    return await user_crud.update_user(db, user_body, original=user)