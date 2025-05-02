from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from models import Session
from typing import Annotated

async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]