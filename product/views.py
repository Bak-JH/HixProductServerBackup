import datetime
import urllib
import json

from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned 
from django.urls import reverse
from product.models import Product, ProductSerial
from product.forms import RegisterSerialForm, LoginForm, SignupForm
from django.db import models
from django.conf import settings

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .utils import verify_recaptcha

# @require_GET
# # @login_required
# def check_login(req):
#     """Checks logged in status"""
#     if not req.user.is_authenticated:
#         return HttpResponseForbidden()

#     num_visits = req.session.get('num_visits', 0)
#     num_visits += 1
#     req.session['num_visits'] = num_visits
#     respStr = f"you are logged in, visited this page: {num_visits} in this session"

#     return HttpResponse(respStr)


@require_GET
@login_required(login_url="/product/login")
def owns(req, product_name):
    """Checks is user owns product"""
    try:
        product = Product.objects.get(name=product_name)
        product_serial = ProductSerial.objects.get(product=product, owner=req.user)
    except:
        return HttpResponseRedirect(reverse('register_product'))
    return HttpResponse("owns product")


@login_required(login_url="/product/login")
def register(req):
    """Register product if product exists and user doesn't own product"""
    if req.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RegisterSerialForm(req.POST, user=req.user)
        # Check if the form is valid:/
        if form.is_valid():
            #register serial
            serial = form.cleaned_data['serial_number']
            register_product_serial = ProductSerial.objects.get(serial_number=serial)
            register_product_serial.owner = req.user
            register_product_serial.save()
            product_name = register_product_serial.product.name
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('owns_product', kwargs={'product_name': product_name}))
        else:
            context = {
                'form': form,
                'user': req.user
            }
            return render(req, 'product/register_serial.html', context)

    # If this is a GET (or any other method) create the default form.
    else:
        #logout
        if req.GET.get('clicked'):
            return product_logout(req)
            
        else: 
            form = RegisterSerialForm(user=req.user)
            context = {
                'form': form,
                'user': req.user,
            }
            return render(req, 'product/register_serial.html', context)
    
    return HttpResponseRedirect(reverse('registration_done'))

def product_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/product/login_redirect/')

    else:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                if verify_recaptcha(request.POST.get('g-recaptcha-response')):
                    new_user = User.objects.create_user(**form.cleaned_data)
                    return HttpResponseRedirect(reverse('product_login'))
                else:
                    error = 'Invalid reCAPTCHA. Please try again.'
                    context = {
                        'form': form,
                        'error': error
                    }
                return render(request, 'product/signup.html', context)
            return render(request, 'product/signup.html', {'form': form})                        
        #get
        else:
            form = SignupForm()
            context = {
                'form': form, 
                'key': settings.RECAPTCHA_SITE_KEY
            }
            return render(request, 'product/signup.html', context)
    
def product_login(request):
    """Checks logged in status"""
    if request.user.is_authenticated: 
        next_url = request.GET.get('next')
        if next_url:
            response = HttpResponseRedirect(next_url)
            response.set_cookie('username', request.user.username, domain=".hix.co.kr")
            return response   
        else:
            response = HttpResponseRedirect('/product/login_redirect/')
            response.set_cookie('username', request.user.username, domain=".hix.co.kr")
            return response
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            id = request.POST['username']
            pw = request.POST['password']
            user = authenticate(username=id, password=pw)
            if user is not None:
                login(request, user=user)
                next_url = request.GET.get('next')
                if next_url:
                    response = HttpResponseRedirect(next_url)
                    response.set_cookie('username', user.username, domain=".hix.co.kr")
                    return response
                else:
                    response = HttpResponseRedirect(reverse('product_login_redirect'))
                    response.set_cookie('username', user.username, domain=".hix.co.kr")
                    return response
            else:
                try: 
                    user = User.objects.get(username=request.POST['username'])
                    if not user.is_active:
                        error = 'Email is not verified. Please check your email'
                    else: 
                        error = 'Password is incorrect'
                except:
                    error = 'We cannot find an account with that ID'

                context = {
                    'form': form,
                    'error': error
                }
                return render(request, 'product/login.html', context)

        #get
        else:
            form = LoginForm()
        
        return render(request, 'product/login.html', {'form': form})

@login_required(login_url="/product/login")
def product_logout(request):
    if request.GET.get('clicked'):
        logout(request)
        next_url = request.GET.get('next')
        if next_url:
            response = HttpResponseRedirect(next_url)
            response.delete_cookie('username')
            return response   
        else:
            response = HttpResponseRedirect('/product/login/')
            response.delete_cookie('username')
            return response
    else:
        return render(request, 'product/logout.html')



@login_required(login_url="/product/login")
def product_login_redirect(req):
    return render(req, 'product/login_redirect.html')

@login_required(login_url="/product/login")
def registration_done(req):
    return render(req, 'product/registration_done.html')


def on_signup(request, user, **kwargs):
    social_user = SocialAccount.objects.get(user=user)
    provider = social_user.get_provider()
    if provider.id.lower() == 'naver':
        user.last_name = social_user.extra_data['name']
        user.email = social_user.extra_data['email']
        user.save()

user_signed_up.connect(on_signup)
