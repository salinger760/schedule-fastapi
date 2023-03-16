from fastapi import APIRouter, HTTPException, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas.schedule as schedule_schema
import cruds.schedule as schedule_crud
from fastapi_csrf_protect import CsrfProtect
from lib.auth_utils import AuthJwtCsrf

router = APIRouter(prefix="/schedules", tags=["Schedule"])
auth = AuthJwtCsrf()


@router.get("/", response_model=list[schedule_schema.Schedule])
async def get_schedules(
    req: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    auth.verify_jwt(req)
    schedules = await schedule_crud.get_schedules(db, skip=skip, limit=limit)
    return schedules


@router.get("/{schedule_id}", response_model=schedule_schema.Schedule)
async def get_schedule(
    req: Request, res: Response, schedule_id: int, db: AsyncSession = Depends(get_db)
):
    new_token, _ = auth.verify_update_jwt(req)

    db_user = await schedule_crud.get_schedule(db, schedule_id=schedule_id)

    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if db_user is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_user


@router.get("/user/{user_id}", response_model=list[schedule_schema.Schedule])
async def get_user_schedule(
    req: Request, res: Response, user_id: int, db: AsyncSession = Depends(get_db)
):
    new_token, _ = auth.verify_update_jwt(req)

    db_user = await schedule_crud.get_schedule_user(db, user_id=user_id)

    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if db_user is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_user


@router.post("/", response_model=schedule_schema.ScheduleCreateResponse)
async def create_schedule(
    req: Request,
    res: Response,
    schedule_body: schedule_schema.ScheduleCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    new_token = auth.verify_csrf_update_jwt(req, csrf_protect, req.headers)

    result = await schedule_crud.create_schedule(db, schedule_body)

    res.status_code = status.HTTP_201_CREATED
    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if result:
        return result
    raise HTTPException(status_code=404, detail="Create Schedule failed")


@router.put("/{schedule_id}", response_model=schedule_schema.ScheduleCreateResponse)
async def update_user(
    req: Request,
    res: Response,
    schedule_id: int,
    schedule_body: schedule_schema.ScheduleCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    new_token = auth.verify_csrf_update_jwt(req, csrf_protect, req.headers)

    schedule = await schedule_crud.get_schedule(db, schedule_id=schedule_id)

    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return await schedule_crud.update_schedule(db, schedule_body, original=schedule)


@router.delete("/{schedule_id}", response_model=None)
async def delete_user(schedule_id: int, db: AsyncSession = Depends(get_db)):
    schedule = await schedule_crud.get_schedule(db, schedule_id=schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="schedule not found")

    return await schedule_crud.delete_schedule(db, original=schedule)
