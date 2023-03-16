from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import Optional, Tuple
from datetime import datetime, timedelta, timezone
import schemas.tag as tag_schema
import models.tag as tag_model


JST = timezone(timedelta(hours=+9), "JST")


async def get_tag(
    db: AsyncSession, tag_id: int
) -> Optional[tag_model.Tag]:
    result: Result = await db.execute(
        select(tag_model.Tag).where(
            tag_model.Tag.id == tag_id
        )
    )
    # for item in result:
    #    print(item.Item.id)
    # print(result.first())

    tag: Optional[
        Tuple[tag_model.Tag]
    ] = result.first()
    return tag[0] if tag is not None else None


async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(
            tag_model.Tag.id,
            tag_model.Tag.name,
            tag_model.Tag.color,
            tag_model.Tag.created_at,
            tag_model.Tag.updated_at,
        )
        .offset(skip)
        .limit(limit)
    )
    return result.all()


async def create_tag(
    db: AsyncSession, job: tag_schema.Tag
) -> tag_model.Tag:

    db_tag = tag_model.Tag(**job.dict())

    db.add(db_tag)

    await db.commit()
    await db.refresh(db_tag)

    return db_tag


async def update_tag(
    db: AsyncSession,
    job_create: tag_schema.Tag,
    original: tag_model.Tag,
) -> tag_model.Tag:

    original.date_tag = job_create.date_tag
    original.title = job_create.title
    original.copies = job_create.copies
    original.speed = job_create.speed
    original.finished_top_to_bottom = job_create.finished_top_to_bottom
    original.finished_edge = job_create.finished_edge
    original.cover_cutting_top = job_create.cover_cutting_top
    original.cover_edge = job_create.cover_edge
    original.cover_thickness = job_create.cover_thickness
    original.signature_cutting_top = job_create.signature_cutting_top
    original.signature_edge = job_create.signature_edge
    original.signature_thickness = job_create.signature_thickness
    original.updated_at = datetime.now(JST)
    original.created_at = job_create.created_at

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_tag(
    db: AsyncSession, original: tag_model.Tag
) -> None:
    await db.delete(original)
    await db.commit()
