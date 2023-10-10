from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from anymal.config import settings
from anymal.db import create_db_and_tables, User
from anymal.schemas.user import UserRead, UserCreate, UserUpdate
from anymal.users import auth_backend, fastapi_users, current_active_user, google_oauth_client

# from anymal.routers import user  # Uncomment when you want to use the user router

app = FastAPI()

# Add CORS middleware with more restrictive origins for production
ALLOWED_ORIGINS = ["*"]  # For dev, allow all origins; for prod, list your frontend domains.
if settings.environment == 'production':  # Assuming you have a 'debug' field in your Settings class
    ALLOWED_ORIGINS = ["https://anymal.io"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # List of origins (you might want to restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # List of allowed methods
    allow_headers=["*"],  # List of allowed headers
)

@app.get('/')
def index():
    return {'Welcome to Anymal Framework 💀'}

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

app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, str(settings.secret_key)),
    prefix="/auth/google",
    tags=["auth"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()


async def init_db():
    # Your DB initialization logic here
    await create_db_and_tables()


app.add_event_handler("startup", init_db)
