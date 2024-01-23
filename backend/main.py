from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, WebSocketException
from fastapi.middleware.cors import CORSMiddleware

from anymal import stripe_integration
from anymal.config import settings
from anymal.db import create_db_and_tables, User
from anymal.schemas.user import UserRead, UserCreate, UserUpdate
from anymal.users import auth_backend, UserManager, get_user_manager
from anymal.users import fastapi_users, google_oauth_client, AccessTokenDatabase, AccessToken, get_database_strategy, get_access_token_db
from anymal.websocket_manager import connect, disconnect, broadcast

# from anymal.routers import user  # Uncomment when you want to use the user router
# import pdb
# pdb.set_trace()
app = FastAPI(docs_url=settings.docs_url, redoc_url=settings.redoc_url, debug=settings.debug)


# Add CORS middleware with more restrictive origins for production
ALLOWED_ORIGINS = ["http://localhost:3000",  # Vue app
                   "http://localhost:8000"  # FastAPI app
                   ]
if settings.environment == 'production':  # Assuming you have a 'debug' field in your Settings class
    ALLOWED_ORIGINS = ["https://anymal.io"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # List of origins (you might want to restrict this in production)
    allow_credentials=True,  # Allow cookies
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
    fastapi_users.get_oauth_router(google_oauth_client,

                                   auth_backend,
                                   str(settings.secret_key),
                                   redirect_url=f'{settings.frontend_base_url}/auth/google/callback'
                                   ),
    prefix="/auth/google",

    tags=["auth"],
)

# Stripe
app.include_router(stripe_integration.router, prefix="/stripe", tags=["stripe"])


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()


@app.post("/send_message")
async def send_message_endpoint(message: str):
    await broadcast(message)
    return {"message": "Message sent"}


async def get_user_from_cookie(
        websocket: WebSocket,
        user_manager: UserManager = Depends(get_user_manager),
        access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db)
):
    # Extract the JWT token directly from the WebSocket's cookies
    cookie = websocket.cookies.get(settings.auth_cookie_name)

    if not cookie:
        raise WebSocketException("Authentication cookie not found")

    # Decode and verify the JWT token using the auth_backend
    # Get the strategy using the access_token_db
    strategy = get_database_strategy(access_token_db)

    user = await strategy.read_token(cookie, user_manager)
    if not user or not user.is_active:
        raise WebSocketException("Invalid user")
    return user


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_user_from_cookie)):
    await connect(websocket, user)
    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_text()

            # Send a message back to the client
            await broadcast(f"Message text was: {data}")

    except WebSocketDisconnect:
        disconnect(websocket)
        await broadcast("Client left the chat")
