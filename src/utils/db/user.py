from . import *

from utils.logger.logger import BotLogger


class User(BaseModel):
    user_id: int
    username: Optional[str]
    full_name: str
    join_time: datetime.datetime
    is_banned: bool
    account_created: bool
    welcome_notif_id: int
    feature_notif_id: int
    balance: int = 0
    ref_id: Optional[int]


class UserOrm:
    def __init__(self):
        self.async_session = async_session

    async def is_banned_user(self, user_id: int) -> bool:
        try:
            async with self.async_session() as session:
                query = select(UserModel.is_banned).where(
                    UserModel.user_id == user_id)
                result = await session.execute(query)
                banned = result.scalars().first()
                if banned:
                    return True
                return False
        except TypeError:
            return False

    async def add_user(self, user_id: int, full_name: str = None, username: str = None, ref_id: int = None) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    await BotLogger().info(
                        message=f'Adding user: username={username}, user_id={user_id}')
                    local_time = datetime.datetime.now()
                    session.add(
                        UserModel(
                            user_id=user_id,
                            username=username,
                            full_name=full_name,
                            join_time=local_time,
                            account_created=False,
                            ref_id=ref_id
                        ),
                    )
                    await session.commit()

                    await BotLogger().info(
                        message=f'User added: username={username}, user_id={user_id}'
                    )
                    return True
                except sqlalchemy.exc.IntegrityError:
                    await BotLogger().info(
                        message=f'User is know: username={username}, user_id={user_id}')
                    pass
                except Exception as e:
                    raise e

    async def remove(self, user_id: int) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(UserModel).where(
                    UserModel.user_id == user_id
                )
                await session.execute(query)
                return True

    async def create_account(self, user_id: int) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                q = update(UserModel).where(
                    UserModel.user_id == user_id
                ).values(
                    account_created=True
                )
                await session.execute(q)
                return True

    async def ban_user(self, user_id: int) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                q = update(UserModel).where(
                    UserModel.user_id == user_id
                ).values(
                    is_banned=True
                )
                await session.execute(q)
                return True

    async def unban_user(self, user_id: int) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                q = update(UserModel).where(
                    UserModel.user_id == user_id
                ).values(
                    is_banned=False
                )
                await session.execute(q)
                return True

    async def get_user(self, user_id: int) -> User:
        async with self.async_session() as session:
            async with session.begin():
                q = select(UserModel).where(UserModel.user_id == user_id)
                for i in await session.execute(q):
                    return User(
                        user_id=i.UserModel.user_id,
                        username=i.UserModel.username,
                        full_name=i.UserModel.full_name,
                        join_time=i.UserModel.join_time,
                        is_banned=i.UserModel.is_banned,
                        account_created=i.UserModel.account_created,
                        welcome_notif_id=i.UserModel.welcome_notif_id,
                        feature_notif_id=i.UserModel.feature_notif_id,
                        balance=i.UserModel.balance,
                        ref_id=i.UserModel.ref_id
                    )

    async def is_have_account(self, user_id: int) -> bool:
        async with self.async_session() as session:
            async with session.begin():
                q = select(UserModel).where(UserModel.user_id == user_id)
                result = await session.execute(q)
                user = result.scalars().first()
                if user is None or not user.account_created:
                    return False
                return True
