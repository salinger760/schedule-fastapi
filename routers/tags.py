from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas.tag as tag_schema
import cruds.tag as tag_crud

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", response_model=list[tag_schema.Tag])
async def get_tags(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    tags = await tag_crud.get_tags(db, skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model=tag_schema.Tag)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await tag_crud.get_tag(db, tag_id=tag_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="tag not found")
    return db_user


@router.post(
    "/",
    response_model=tag_schema.TagCreateResponse,
)
async def create_tag(
    tag_body: tag_schema.TagCreate,
    db: AsyncSession = Depends(get_db),
):
    return await tag_crud.create_tag(db, tag_body)


@router.put(
    "/{tag_id}",
    response_model=tag_schema.TagCreateResponse,
)
async def update_tag(
    tag_id: int,
    tag_body: tag_schema.TagCreate,
    db: AsyncSession = Depends(get_db),
):
    tag = await tag_crud.get_tag(db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")

    return await tag_crud.update_tag(db, tag_body, original=tag)


@router.delete("/{tag_id}", response_model=None)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await tag_crud.get_tag(db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")

    return await tag_crud.delete_tag(db, original=tag)
