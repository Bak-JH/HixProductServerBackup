from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, HttpResponseServerError
from .forms import CancelForm
from lib.BootpayApi import BootpayApi
import json 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import time
from .models import BillingInfo, PaymentHistory, PricingPolicy
from product.models import Product, ProductSerial
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from django.views.decorators.csrf import csrf_exempt

def load_bootpay():
    bootpay = BootpayApi('59a4d32b396fa607c2e75e00', 't3UENPWvsUort5WG0BFVk2+yBzmlt3UDvhDH2Uwp0oA=')
    bootpay.response = bootpay.get_access_token()
    return bootpay

def billing_bootpay(bootpay, billing_id, product_name, price, order_id, userinfo):
    result = bootpay.subscribe_billing(
                        billing_id, product_name, 
                        price,      order_id, 
                        [],         userinfo
                    )
    return result['data'] if result['status'] is 200 else None

def save_billingInfo(billing_id, card_name, card_number):
    card_number = card_number[-4:]
    return BillingInfo(billing_key=billing_id, 
                       card_name=card_name, 
                       card_number=card_number)

def find_free_serial(product):
    return ProductSerial.objects.filter(product=product, owner=None)

def save_receipt(receipt_id, receipt_url, purchased_at, serial):
    purchased_at = purchased_at if purchased_at is not None else None
    serial = ProductSerial.objects.get(serial_number=serial.serial_number)
    return PaymentHistory(receipt_id, receipt_url, purchased_at, serial)

def send_receipt(url, email):
    print(url)
    print(email)

    msg_html = render_to_string('order/receipt.html', {'receipt_url': url})

    result = send_mail(
        'Receipt from HiX',
        '',
        'HiX<support@hix.co.kr>',
        [email],
        html_message=msg_html
    )

    return result

@login_required(login_url="/product/login")
def subscribe(request):
    try:
        product = Product.objects.get(name=request.GET.get('product'))
        policy = PricingPolicy.objects.get(product=product)
    except:
        raise Http404('Product Not Exist')

    if request.method == 'POST':
        billing_id = request.POST['billing_id']
        bootpay = load_bootpay()
        if bootpay.response['status'] is 200 :
            result = billing_bootpay(
                        bootpay,
                        billing_id, 
                        policy.product.name, 
                        policy.price,
                        request.POST['order_id'],
                        {'username': request.user.username, 'email': request.user.email}
                    )

            save_billingInfo(billing_id, result['card_name'], result['card_no'])
            save_receipt(result['receipt_id'], result['receipt_url'],
                        result['purchased_at'], find_free_serial(product)[0])
            send_receipt(result['receipt_url'], request.user.email)

            return JsonResponse({'receipt_url': result['receipt_url']})
        else:
            return HttpResponseServerError()
    else:
        return render(request, 'order/subscribe.html')

@login_required(login_url="/product/login")
def cancel_payment(request, billing_id):
    if request.method == "POST":
        bootpay = load_bootpay()
        if bootpay.response['status'] is 200:
            result = bootpay.cancel(billing_id, '', request.POST['cancel_user'], request.POST['cancel_reason'])
            return HttpResponse()
    else:
        return render(request, 'order/cancel_payment.html', {'form': CancelForm})

