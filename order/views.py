from order.tasks import do_payment
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from .forms import CancelForm
from django.contrib.auth.decorators import login_required
from .models import  PricingPolicy, RegularPayment
from product.models import Product
from .utils import *
import datetime
import uuid
from slicerServer.views import show_error
from rest_framework.decorators import api_view

from django.contrib.admin.views.decorators import staff_member_required

def do_payment_first(billing_id, policy, user):
    bootpay = load_bootpay()
    if bootpay.response['status'] is 200:
        result = billing_bootpay(
                    bootpay, 
                    billing_id, 
                    policy.product.name, 
                    policy.price,
                    str(uuid.uuid4()),
                    {'username': user.username, 'email': user.email}
                )

        if result is not None:
            billinginfo = save_billingInfo(True, billing_id, result['card_name'], result['card_no'], user)# disabled isSave
            target_serial = create_new_serial(policy.product)
            save_receipt(result['receipt_id'], result['receipt_url'], result['purchased_at'], target_serial.serial_number, billinginfo)
            send_receipt(result['receipt_url'],
                        user.email, target_serial.serial_number)
            
            crontab_date = (str(datetime.datetime.now().minute),
                            str(datetime.datetime.now().hour),
                            '*',
                            str(datetime.datetime.today().day),
                            '*')

            regular = RegularPayment.objects.create(serial=target_serial, billing_info=billinginfo, policy=policy, owner=user)

            reserve_billing(crontab_date, str(regular.id))
            return result['receipt_url']
    return None

# from django.views.decorators.csrf import csrf_exempt
@staff_member_required
@login_required(login_url="/product/login")
def subscribe(request):
    try:
        policy = PricingPolicy.objects.get(pricing_id=request.GET.get('id'))
        product = policy.product
    except:
        return show_error(request, 404, 'Pricing Policy Not Exist')

    bootpay = load_bootpay()
    if bootpay.response['status'] is not 200:
        return show_error(request, bootpay.response['status'])

    if request.method == 'POST':
        try:
            billing_id = request.POST['billing_id'] 
        except:
            try: 
                billing_id = request.data['billing_id']
            except:
                return HttpResponse(status=500)
            
        try:
            user = User.objects.get(username=request.user.username)
        except:
            HttpResponse(status=500)

        try:
            isSave = request.POST['is_save']
        except:
            isSave = False
        result = do_payment_first(billing_id, policy, user) # disabled isSave option. To Enable, edit True to isSave
        

        if result is not None:
            return JsonResponse({'receipt_url': result})
        return HttpResponse(status=500)
            
    else:
        return render(request, 'order/subscribe.html', {'product':product.name})

@staff_member_required
@login_required(login_url="/product/login")
def cancel_payment(request, receipt_id):
    if request.method == "POST":
        bootpay = load_bootpay()
        if bootpay.response['status'] is 200:
            result = bootpay.cancel(receipt_id, '', request.POST['cancel_user'], request.POST['cancel_reason'])
            
            if result['status'] is 200:
                try:
                    receipt_url = cancel_reserve(receipt_id)
                    return render(request, 'order/thank_you.html', 
                                  {'refund': True, 'url': receipt_url})
                except Exception as e:
                    return show_error(request, 500, e)
            else:
                return show_error(request, result['status'], result['message'])
        else:
            return show_error(request, bootpay.response['status'])
    else:
        return render(request, 'order/cancel_payment.html', {'form': CancelForm})

