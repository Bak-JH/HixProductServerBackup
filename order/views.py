from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from lib.BootpayApi import BootpayApi
import json 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
@login_required(login_url="/product/login")
def subscribe(request):
    billing_id = request.GET.get('id')
    if billing_id:
        print(billing_id)
        bootpay = BootpayApi('59a4d32b396fa607c2e75e00', 't3UENPWvsUort5WG0BFVk2+yBzmlt3UDvhDH2Uwp0oA=')
        access_token = bootpay.get_access_token()
        result = bootpay.subscribe_billing(
                    billing_id, 
                    '테스트', 
                    1000, 
                    'id_dent1', 
                    [], 
                    {'username': 'test'}
                )
        reserve = bootpay.subscribe_billing_reserve(
                    billing_id,
                    '테스트 예약',
                    3000,
                    'id_dent1',
                    time.time() + 30, # 30초 뒤 실행
                    '[[ feedback_url ]]'
                )
        receipt = result['data']['receipt_url']
        print(reserve)
        return HttpResponseRedirect(receipt)
    else:
        return render(request, 'subscribe.html')

@login_required(login_url="/product/login")
def cancel_subscribe(request, billing_id):
    print(billing_id)
    bootpay = BootpayApi('59a4d32b396fa607c2e75e00', 't3UENPWvsUort5WG0BFVk2+yBzmlt3UDvhDH2Uwp0oA=')
    response = bootpay.get_access_token()
    if response['status'] is 200:
        print(bootpay.destroy_subscribe_billing_key(billing_id))
        return HttpResponse(bootpay.destroy_subscribe_billing_key(billing_id))
