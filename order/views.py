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

# from django.views.decorators.csrf import csrf_exempt
@login_required(login_url="/product/login")
def subscribe(request):
    try:
        product = Product.objects.get(name=request.GET.get('product'))
        policy = PricingPolicy.objects.get(product=product)
    except:
        return show_error(request, 404, 'Product Not Exist')

    bootpay = load_bootpay()
    if bootpay.response['status'] is not 200:
        return show_error(request, bootpay.response['status'])

    if request.method == 'POST':
        billing_id = request.POST['billing_id']        
        target_serial = find_free_serial(product)[0]
        userinfo = {'username': request.user.username, 'email': request.user.email}
        result = do_payment(billing_id, policy, target_serial, userinfo)   
        

        if result is not None:
            crontab_date = ('*','*','*',str(datetime.datetime.today().day),'*')
            reserve_result = reserve_billing(billing_id, policy, target_serial,
                                                userinfo, crontab_date)
            if reserve_result is not None:
                return JsonResponse({'receipt_url': result})
        return show_error(request, 500, )

            
    else:
        return render(request, 'order/subscribe.html')

@login_required(login_url="/product/login")
def cancel_payment(request, receipt_id):
    if request.method == "POST":
        bootpay = load_bootpay()
        if bootpay.response['status'] is 200:
            result = bootpay.cancel(receipt_id, '', request.POST['cancel_user'], request.POST['cancel_reason'])
            
            if result['status'] is 200:
                cancel_reserve(receipt_id)
            else:
                return show_error(request, result['status'], result['message'])
            return render(request, 'order/thank_you.html', {'refund': True})
        else:
            return show_error(request, bootpay.response['status'])
    else:
        return render(request, 'order/cancel_payment.html', {'form': CancelForm})

