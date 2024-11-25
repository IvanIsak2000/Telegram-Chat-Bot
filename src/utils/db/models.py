from sqlalchemy import (
    MetaData,
    Integer,
    BigInteger,
    String,
    Boolean,
    DateTime,
)

from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from utils.config import DSN
from utils.logger.logger import BotLogger

meta = MetaData()
Base = declarative_base(metadata=meta)

try:
    engine = create_async_engine(
        DSN,
        pool_size=10,
        max_overflow=20,
        connect_args={"timeout": 120}
    )

    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
except ValueError:
    pass


class UserModel(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    full_name: Mapped[str] = mapped_column(String)
    join_time: Mapped[str] = mapped_column(DateTime(timezone=True))
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    welcome_notif_id: Mapped[int] = mapped_column(Integer, default=0)
    feature_notif_id: Mapped[int] = mapped_column(Integer, default=0)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(meta.create_all)
    except Exception as e:
        if "already exists" in str(e):
            await BotLogger().info('✅ DB is created')
        else:
            await BotLogger().critical(f'DB error: {e}')
    