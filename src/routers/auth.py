import stripe
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from src import app
from src.config import settings

router = APIRouter(
    prefix = "/auth",
    tags = ['Auth']
)

# Stripe Credentials
stripe_keys = {
    "secret_key"     : settings.stripe_secret_key,
    "publishable_key": settings.stripe_publishable_key,
    "endpoint_secret": settings.stripe_secret_key
}

stripe.api_key = stripe_keys["secret_key"]

@router.get("/stripe_login")
def stripe_login(request: Request):
    if not settings.stripe_client_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing a Required Credential")

    stripe_login_url = f'https://connect.stripe.com/oauth/authorize?response_type=code&client_id={settings.stripe_client_id}&scope=read_write&redirect_uri={settings.stripe_oauth_redirect}'
    # stripe_login_url = f'https://connect.stripe.com/oauth/authorize?response_type=code&client_id={settings.stripe_client_id}&scope=read_write'
    redirect = RedirectResponse(url=stripe_login_url)

    return redirect

@router.get("/login")
def authorize_stripe(request: Request):
    authorization_code = request.query_params.get('authorization_code')

    try:
        response = stripe.OAuth.token(
            grant_type='authorization_code',
            code=authorization_code,
        )

        account_id = response['stripe_user_id']
        return {'account_id':account_id}
    except Exception as e:
        print (e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Missing Authorization Code")

@router.get("/logout")
def deauthorize_stripe():

    stripe.OAuth.deauthorize(
        client_id='ca_FkyHCg7X8mlvCUdMDao4mMxagUfhIwXb',
        stripe_user_id='acct_5qIK6loErW6kNw'
    )

    return {'hip' : 'hop'}
