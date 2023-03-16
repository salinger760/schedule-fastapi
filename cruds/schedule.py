from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

# from sqlalchemy.orm import joinedload
from typing import Optional, Tuple
from datetime import timedelta, timezone
import schemas.schedule as schedule_schema
import models.schedule as schedule_model
import models.tagging as tagging_model
import cruds.tag as tag_crud


JST = timezone(timedelta(hours=+9), "JST")


async def get_schedule(
    db: AsyncSession, schedule_id: int
) -> Optional[schedule_model.Schedule]:
    result: Result = await db.execute(
        select(schedule_model.Schedule).where(schedule_model.Schedule.id == schedule_id)
    )

    schedule: Optional[Tuple[schedule_model.Schedule]] = result.first()
    return schedule[0] if schedule is not None else None


async def get_schedules(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(
            schedule_model.Schedule.id,
            schedule_model.Schedule.user_id,
            schedule_model.Schedule.period_start,
            schedule_model.Schedule.period_end,
            schedule_model.Schedule.title,
            schedule_model.Schedule.memo,
            schedule_model.Schedule.created_at,
            schedule_model.Schedule.updated_at,
        )
        .offset(skip)
        .limit(limit)
    )
    return result.all()


async def get_schedule_user(
    db: AsyncSession, user_id: int
) -> Optional[schedule_model.Schedule]:

    result: Result = await db.execute(
        select(
            schedule_model.Schedule.id,
            schedule_model.Schedule.user_id,
            schedule_model.Schedule.period_start,
            schedule_model.Schedule.period_end,
            schedule_model.Schedule.title,
            schedule_model.Schedule.memo,
            schedule_model.Schedule.created_at,
            schedule_model.Schedule.updated_at,
        ).where(schedule_model.Schedule.user_id == user_id)
    )

    # result: Result = await db.execute(
    #    select(schedule_model.Schedule).where(
    #        schedule_model.Schedule.user_id == user_id
    #    )
    # )

    return result.all()

    # schedule: Optional[Tuple[schedule_model.Schedule]] = result.first()
    # return schedule[0] if schedule is not None else None


# async def get_schedule_user(
#    db: AsyncSession, schedule_id: int
# ) -> Optional[schedule_model.Schedule]:
#    result: Result = await db.execute(
#        select(schedule_model.Schedule)
#        .where(schedule_model.Schedule.id == schedule_id)
#        .options(joinedload(schedule_model.Schedule.user))
#    )
#
#    schedule: Optional[Tuple[schedule_model.Schedule]] = result.first()
#    return schedule[0] if schedule is not None else None


async def create_schedule(
    db: AsyncSession, schedule_create: schedule_schema.ScheduleCreate
) -> schedule_model.Schedule:

    db_schedule = schedule_model.Schedule()
    db_schedule.user_id = schedule_create.user_id
    db_schedule.period_start = schedule_create.period_start
    db_schedule.period_end = schedule_create.period_end
    db_schedule.title = schedule_create.title
    db_schedule.memo = schedule_create.memo

    for tag_id in schedule_create.tag:
        tag_info = await tag_crud.get_tag(db, tag_id)

        if tag_info is not None:
            db_schedule.tag.append(tag_info)

    db.add(db_schedule)

    await db.commit()
    await db.refresh(db_schedule)

    return db_schedule


async def update_schedule(
    db: AsyncSession,
    schedule_create: schedule_schema.ScheduleCreate,
    original: schedule_model.Schedule,
) -> schedule_model.Schedule:

    original.user_id = schedule_create.user_id
    original.period_start = schedule_create.period_start
    original.period_end = schedule_create.period_end
    original.title = schedule_create.title
    original.memo = schedule_create.memo

    for tag_id in schedule_create.tag:
        tag_info = await tag_crud.get_tag(db, tag_id)

        if tag_info is not None:
            original.tag.append(tag_info)

    # 現在のタグを削除
    result = await db.execute(
        select(tagging_model.Tagging).where(
            tagging_model.Tagging.schedule_id == original.id
        )
    )

    delete_data_list = result.all()

    if delete_data_list is not None:
        for delete_data in delete_data_list:
            await db.delete(delete_data[0])

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_schedule(db: AsyncSession, original: schedule_model.Schedule) -> None:
    await db.delete(original)
    await db.commit()
