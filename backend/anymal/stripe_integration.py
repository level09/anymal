import stripe
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .db import get_async_session, User
from .schemas.user import UserRead
from .users import current_active_user

router = APIRouter()

stripe.api_key = settings.stripe_secret_key.get_secret_value()


@router.post("/create-checkout-session", )
async def create_checkout_session(lookup_key: str, current_user: UserRead = Depends(current_active_user),
                                  session: AsyncSession = Depends(get_async_session)):
    try:
        prices = stripe.Price.list(lookup_keys=[lookup_key], expand=['data.product'])

        # Fetch the user from the database
        user = (await session.execute(select(User).filter(User.id == current_user.id))).scalar_one_or_none()

        # If the user doesn't have a stripe_customer_id, create a new customer in Stripe
        if user and not user.stripe_customer_id:
            stripe_customer = stripe.Customer.create(email=current_user.email)
            user.stripe_customer_id = stripe_customer.id
            await session.commit()

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': prices.data[0].id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=settings.domain + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.domain + '/cancelled',
            customer=user.stripe_customer_id if user else None
        )

        return {"checkout_url": checkout_session.url}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")


@router.post("/create-portal-session")
async def customer_portal(current_user: UserRead = Depends(current_active_user),
                          session: AsyncSession = Depends(get_async_session)):
    try:
        # Fetch the user from the database
        user = (await session.execute(select(User).filter(User.id == current_user.id))).scalar_one_or_none()

        # If the user doesn't have a stripe_customer_id, raise an error
        if not user or not user.stripe_customer_id:
            raise HTTPException(status_code=400, detail="User does not have an associated Stripe customer ID.")

        return_url = settings.domain
        portalSession = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id,
            return_url=return_url,
        )
        return {"portal_url": portalSession.url}  # Return the portal URL as a JSON response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")



@router.post("/webhook")
async def webhook_received(request: Request):
    webhook_secret = settings.webhook_secret
    request_data = await request.json()

    if webhook_secret:
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
    elif event_type == 'customer.subscription.trial_will_end':
        print('Subscription trial will end')
    elif event_type == 'customer.subscription.created':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.updated':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.deleted':
        print('Subscription canceled: %s', event.id)

    return {'status': 'success'}
