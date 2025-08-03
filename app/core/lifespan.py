import asyncio
from sqlalchemy.exc import OperationalError
from app.db.base import Base
from app.db.session import engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app):
    retries = 0
    max_retries = 10  # 10 * 3s = 30 seconds max wait

    while retries < max_retries:
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected, tables created if not exists.")
            break
        except OperationalError:
            retries += 1
            print(f"Database not ready, retrying in 3 seconds... (Attempt {retries}/{max_retries})")
            await asyncio.sleep(3)
    else:
        # Optional: exit if DB never becomes ready
        raise RuntimeError("Database connection failed after multiple attempts.")

    yield
