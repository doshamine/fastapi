from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy import Integer, Float, String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import config
import datetime

engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {'id': self.id}


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'author': self.author,
            'created_at': self.created_at
        }


ORM_OBJ = Advertisement
ORM_CLS = type[Advertisement]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()