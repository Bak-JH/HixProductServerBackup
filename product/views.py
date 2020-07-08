import datetime

from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_GET
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned 
from django.urls import reverse
from product.models import Product, ProductSerial
from product.forms import RegisterSerialForm
from django.db import models


@require_GET
# @login_required
def check_login(req):
    """Checks logged in status"""
    if not req.user.is_authenticated:
        return HttpResponseForbidden()

    num_visits = req.session.get('num_visits', 0)
    num_visits += 1
    req.session['num_visits'] = num_visits
    respStr = f"you are logged in, visited this page: {num_visits} in this session"

    return HttpResponse(respStr)


@require_GET
@login_required
def owns(req, product_name):
    """Checks is user owns product"""
    try:        
        product = Product.objects.get(name=product_name)
        product_serial = ProductSerial.objects.get(name=product_name, owner=self.user)
    except:
            return HttpResponseRedirect(reverse('register_product',  kwargs={'product': product_name}))
    return HttpResponse("owns product")


@login_required
def register(req, product_name):
    """Register product if product exists and user doesn't own product"""
    product = get_object_or_404(Product, name=product_name)
    try:
        #check user doens't already own the product
        product_serial = ProductSerial.objects.get(product=product, owner=req.user)
    except ProductSerial.DoesNotExist:
        # If this is a POST request then process the Form data
        if req.method == 'POST':
            # Create a form instance and populate it with data from the request (binding):
            form = RegisterSerialForm(req.POST, product=product)
            # Check if the form is valid:/
            if form.is_valid():
                #register serial
                serial = form.cleaned_data['serial_number']
                register_product_serial = ProductSerial.objects.get(serial_number=serial)
                register_product_serial.owner = req.user
                register_product_serial.save()
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('registration_done'))

        # If this is a GET (or any other method) create the default form.
        else:
            form = RegisterSerialForm(product=product)
            context = {
                'form': form,
                'product': product,
                'user' : req.user,
            }
            return render(req, 'product/register_serial.html', context)
    except:
        return HttpResponseNotFound()
    #register is not needed
    return HttpResponseRedirect(reverse('registration_done'))


@require_GET
def product_login(req):
    """Checks logged in status"""
    if req.user.is_authenticated:
        return HttpResponseRedirect('/product/login_redirect/')
    return render(req, 'product/login.html')


@login_required
def product_login_redirect(req):
    return render(req, 'product/login_redirect.html')