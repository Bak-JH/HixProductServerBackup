from order.tasks import do_payment
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseServerError
from .forms import CancelForm
from django.contrib.auth.decorators import login_required
from .models import  PricingPolicy
from product.models import Product
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from .utils import *
# from django.views.decorators.csrf import csrf_exempt
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
            target_serial = find_free_serial(product)[0]
            userinfo = {'username': request.user.username, 'email': request.user.email}
            result = do_payment(billing_id, policy, target_serial, userinfo)
            print(result)
            if result is not None:

            # result = billing_bootpay(
            #             bootpay,
            #             billing_id, 
            #             policy.product.name, 
            #             policy.price,
            #             request.POST['order_id'],
            #             userinfo
            #         )
            # if result is not None:

            #     save_billingInfo(billing_id, result['card_name'], result['card_no'])
                
            #     save_receipt(result['receipt_id'], result['receipt_url'],
            #                 result['purchased_at'], target_serial)

            #     send_receipt(result['receipt_url'], 
            #                 request.user.email, target_serial.serial_number)

                return JsonResponse({'receipt_url': result})
            else:
                return HttpResponseServerError()
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

