from order.tasks import do_payment
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from .forms import CancelForm
from django.contrib.auth.decorators import login_required
from .models import  PricingPolicy
from product.models import Product
from .utils import *
import datetime
from slicerServer.views import show_error

from django.contrib.admin.views.decorators import staff_member_required

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
        billing_id = request.POST['billing_id']        
        target_serial = create_new_serial(product)
        userinfo = {'username': request.user.username, 'email': request.user.email}
        result = do_payment(billing_id, product.name, policy.price, target_serial.serial_number, userinfo)   
        

        if result is not None:
            target_serial.is_activated = True
            target_serial.save()
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

