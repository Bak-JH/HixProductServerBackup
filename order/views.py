from django.shortcuts import render
from django.http import HttpResponseRedirect
from lib.BootpayApi import BootpayApi
import json 

# Create your views here.
def subscribe(request):
    order_id = request.GET.get('id')
    if order_id:
        bootpay = BootpayApi('59a4d32b396fa607c2e75e00', 't3UENPWvsUort5WG0BFVk2+yBzmlt3UDvhDH2Uwp0oA=')
        access_token = bootpay.get_access_token()
        result = bootpay.subscribe_billing(order_id, 'test', 3000, '12345', [], {'username': 'test'})
        receipt = result['data']['receipt_url']
        return HttpResponseRedirect(receipt)
    else:
        return render(request, 'subscribe.html')
