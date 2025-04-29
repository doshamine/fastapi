from models import Advertisement, ORM_CLS, ORM_OBJ
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def add_item(session: AsyncSession, item: ORM_OBJ):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(409, "Item already exists")

async def get_item_by_id(session: AsyncSession, orm_cls: ORM_CLS, item_id: int):
    item = await session.get(orm_cls, item_id)

    if item is None:
        raise HTTPException(404, "Item not found")

    return item

async def delete_item(session: AsyncSession, item: ORM_OBJ):
    await session.delete(item)
    await session.commit()