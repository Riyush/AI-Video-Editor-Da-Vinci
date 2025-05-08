import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY

Price_ID = settings.PRICE_ID

if settings.IN_DEVELOPMENT:
    success_url = 'http://localhost:8000/success'
    cancel_url = 'http://localhost:1420/cancel'
else:
    # In Production, setup the urls using the domain I buy
    pass

@api_view(['POST'])
def create_checkout_session(request):
    try:
        data = json.loads(request.body)  # This parses the JSON string into a Python dict
        email = data.get('email', None)
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        # Log to make sure the data is received correctly
        print(f"Received email: {email}")

        # Create new customer
        customer = stripe.Customer.create(email=email)
        #Set 30 minute expiration of checkout
        expires_at = expires_at = int((datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).timestamp())

        session = stripe.checkout.Session.create(
            customer = customer.id,
            payment_method_types=['card',],
            line_items=[{
                'price': Price_ID,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=success_url,
            cancel_url=cancel_url,
            subscription_data={
                'trial_period_days': 14
            },
            expires_at=expires_at
        )
        print(session.url)
        return JsonResponse({'session_url': session.url, 'session_id':session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def check_payment_status(request):

    data = json.loads(request.body)
    session_id = data.get("session_id")

    #print(f"session ID: {session_id}")

    if not session_id:
        return JsonResponse({'error': 'Missing session_id'}, status=400)
    try:
        #stripe.checkout.Session.expire(session_id)
        session = stripe.checkout.Session.retrieve(session_id)
        # The session object has 2 attributes that let us track if a user
        # has paid, has yet to paid but the session is still active, or the page has expired
        # those attributes are payment_status and status
        print(f"this requests payment status: {session.payment_status} and status: {session.status}")
        return JsonResponse({'customer_id':session.customer, 'payment_status': session.payment_status, 'status': session.status})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['POST'])
def expire_checkout_session(request):

    data = json.loads(request.body)
    session_id = data.get("session_id")
    if not session_id:
        return JsonResponse({'error': 'Missing session_id'}, status=400)
    try:
        stripe.checkout.Session.expire(session_id)
        return JsonResponse({'message': 'Session expired successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
