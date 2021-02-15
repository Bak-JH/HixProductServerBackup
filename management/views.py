from django.shortcuts import render
from django.conf import settings
from .forms import AddResinForm, AddProductSerialForm
from resin.models import Material
from product.models import Product, ProductSerial, ProductSerial_batch
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required, permission_required
import uuid
from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status


# Create your views here.

@login_required(login_url="/product/login")
@permission_required('management.edit_resin', login_url="/product/login", raise_exception=True)
def add_serial(request):
    if request.method == "POST":
        form = AddProductSerialForm(request.POST)
        if form.is_valid():
            #product_serial = ProductSerial.objects.create(**form.cleaned_data)
            serials = []
            for i in range(0, int(request.POST['number'])):
                UUID = uuid.uuid4()
                today = date.today()
                created_date = today.strftime("%Y-%m-%d")
                product = Product.objects.get(name=request.POST['product'])
                expire_date = request.POST['expire_date'] if request.POST['expire_date'] != "" else None
                batch = ProductSerial_batch.objects.get(id=request.POST['batch']) if request.POST['batch'] != "" else None
                serial = ProductSerial.objects.create(serial_number=UUID, product=product, expire_date=expire_date, created_date=created_date, batch=batch)
                serial.save()
                serials.append(UUID)

            context = {
                'form': form,
                'serials': serials
            }
            return render(request, 'management/add_serial.html', context)
    else:
        form = AddProductSerialForm()
    return render(request, 'management/add_serial.html', {'form': form})

# @login_required
# @permission_required('management.edit_resin', login_url="services.hix.co.kr/accounts/login", raise_exception=True)
# def add_resinInfo(request):
#     # check user doens't already own the product
#     if request.method == "POST":
#         try:
#             resin_info = Material.objects.get(M_id=request.POST['M_id'])
#             form = AddResinForm(request.POST, resin=resin_info)
#         except Material.DoesNotExist:
#             form = AddResinForm(request.POST, resin=request)
#         except:
#             return HttpResponseNotFound()

#         if form.is_valid():
#             register_product_serial = Material.objects.create(**form.cleaned_data)
#             register_product_serial.save()
#             return render(request, 'management/add_resin.html', {'form': form})
#     else:
#         form = AddResinForm(resin=request)
#     return render(request, 'management/add_resin.html', {'form': form})
