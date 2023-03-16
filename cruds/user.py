from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
import schemas.user as user_schema
import models.user as user_model
from lib.auth_utils import AuthJwtCsrf

# from fastapi.encoders import jsonable_encoder
auth = AuthJwtCsrf()

"""
def user_serializer(users) -> dict:
    result = []
    items = []
    tmp_id = None
    for user in users:
        tmp_id = user.Item.id
        print("-----------------------1")
        print(user.Item.id)

        if tmp_id == user.Item.id:
            item_values = {
                "id": str(user.Item.id),
                "title": user.Item.title,
                "description": bool(user.Item.description),
                "owner_id": user.Item.owner_id,
            }

            items.append(item_values)
            print("-----------------------2")
            print(items)
        else:

            values = {
                "id": str(user.User.id),
                "email": user.User.email,
                "is_active": bool(user.User.is_active),
                "items": items,
            }
            result.append(values)

            items = []
            item_values = {
                "id": str(user.Item.id),
                "title": user.Item.title,
                "description": bool(user.Item.description),
                "owner_id": user.Item.owner_id,
            }
            items.append(item_values)

            print("-----------------------3")
            print(result)

    print("-----------------------4")
    print(items)
    if items:
        values = {
            "id": str(user.User.id),
            "email": user.User.email,
            "is_active": bool(user.User.is_active),
            "items": items,
        }
        result.append(values)

        print("-----------------------5")
        print(result)

        print("===")
        print(result)

    return result
"""

"""
async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Optional[user_model.User]:

    # result: Result = await db.execute(select(user_model.User).offset(skip).limit(limit))
    result: Ressault = await db.execute(
        select(user_model.User, item_model.Item)
        .select_from(user_model.User)
        .join(
            item_model.Item,
            user_model.User.id == item_model.Item.owner_id,
        )
        .order_by(user_model.User.id)
    )
    # print(result.all())
    # print("---------------------------test")
    # return result.all()

    users: Optional[List[user_model.User]] = result.all()

    return user_serializer(users)

    # return user[0] if user is not None else None
"""


async def get_user(db: AsyncSession, user_id: int):
    result: Result = await db.execute(
        select(user_model.User)
        .select_from(user_model.User)
        .where(user_model.User.id == user_id)
    )
    print('-get_user-')
    print(result)
    user: Optional[Tuple[user_schema.User]] = result.first()
    return user[0] if user is not None else None
    #return user[0].toDict() if user is not None else None


async def get_user_by_email(db: AsyncSession, email: str):
    result: Result = await db.execute(
        select(
            user_model.User.id,
            user_model.User.name,
            user_model.User.email,
            user_model.User.hashed_password,
            user_model.User.is_active,
        )
        .select_from(user_model.User)
        .where(user_model.User.email == email)
    )
    user = result.first()

    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(
            user_model.User.id,
            user_model.User.name,
            user_model.User.email,
            user_model.User.is_active,
            user_model.User.created_at,
            user_model.User.updated_at,
        )
        .offset(skip)
        .limit(limit)
    )

    return result.all()


async def create_user(
    db: AsyncSession, user: user_schema.UserCreate
) -> user_model.User:

    user = user_model.User(
        name=user.name,
        email=user.email,
        hashed_password=auth.generate_hashed_password(user.hashed_password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    db: AsyncSession,
    user_create: user_schema.UserUpdate,
    original: user_model.User,
) -> user_model.User:
    print('-update_user-')
    print(type(original))
    print('-----------------------')
    print(type(user_create))
    original.name = user_create.name
    original.email = user_create.email
    original.is_active = user_create.is_active
    print('update_user2')
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_user(db: AsyncSession, original: user_model.User) -> None:
    await db.delete(original)
    await db.commit()

