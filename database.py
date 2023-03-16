from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# heroku
# ASYNC_DB_URL = "postgresql+asyncpg://sariqbxpnwnmcn:d2cb82052c3d3147ff3428a0fb2fd3f3adcb854bb0032a2a1c2233d6c35ded8b@ec2-54-208-104-27.compute-1.amazonaws.com:5432/dalglsjl1ajfht"

# postgresql
ASYNC_DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# mysql
# ASYNC_DB_URL = (
#     f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8"
# )
# ASYNC_DB_URL = "mysql+aiomysql://root:root@db:3306/apidb?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
