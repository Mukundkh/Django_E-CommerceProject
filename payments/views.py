from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree
#sample braintree creds:
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="z2rjcyzz8qnz9x6f",
        public_key="zjy2xy9gz3qkjymc",
        private_key="038f3edc6fbe8f9d7a6ea178a17598c9" 
    )
)
#User authentication
def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)

        if user.session_token == token:
            return True
        else:
            return False
    except UserModel.DoesNotExist:
        return False

#Generate payment token
@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Inavlid Session. Please login again'})

#process payment
@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Inavlid Session. Please login again'})
    
    nonce_from_the_client = request.POST["paymentMethodNonce"]

    amount_from_the_client = request.POST["amount"]


    result = gateway.transaction.sale({

        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({
            'success': result.is_success,
            'transaction':{
                'id':result.transaction.id,
                'amount':result.transaction.amount
            }

        })
    else :
        return JsonResponse({'error':True, 'success':False})

