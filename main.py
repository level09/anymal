from fastapi import FastAPI

from anymal.db import create_db_and_tables
from anymal.schemas.user import UserRead, UserCreate, UserUpdate
from anymal.users import auth_backend, fastapi_users, current_active_user
# from anymal.routers import user  # Uncomment when you want to use the user router

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


async def init_db():
    # Your DB initialization logic here
    await create_db_and_tables()

app.add_event_handler("startup", init_db)
