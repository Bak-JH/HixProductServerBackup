from django.core import exceptions
from .serializers import *
from order.models import BillingInfo, PricingPolicy
from slicerServer.views import show_error

from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product, ProductSerial
from .forms import *
from django.conf import settings
from rest_framework.response import Response

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import pre_social_login
from allauth.exceptions import ImmediateHttpResponse
from django.dispatch import receiver
from allauth.account.utils import perform_login


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.admin.views.decorators import staff_member_required

from django_email_verification import sendConfirm
from .utils import verify_recaptcha
from .serializers import *

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
        form = RegisterSerialForm(user=req.user)
        context = {
            'form': form,
            'user': req.user,
        }
        return render(req, 'product/register_serial.html', context)

    return HttpResponseRedirect(reverse('registration_done'))

def get_user_with_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def product_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/product/login_redirect/')

    else:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                if verify_recaptcha(request.POST.get('g-recaptcha-response')):
                    if get_user_with_email(form.cleaned_data['email']) is not None:
                        error = 'Email already exists. Try again with another email'
                        context = {
                            'form': form,
                            'error': error
                        }
                        return render(request, 'product/signup.html', context)
                    new_user = User.objects.create_user(**form.cleaned_data)
                    new_user.is_active = False
                    sendConfirm(new_user)
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
            response.delete_cookie('username', domain='.hix.co.kr')
            return response   
        else:
            response = HttpResponseRedirect('/product/login/')
            response.delete_cookie('username', domain='.hix.co.kr')
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

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data['email']
    try:
        user = User.objects.get(email=email_address)
        raise ImmediateHttpResponse(perform_login(request, user, email_verification='optional'))
    except User.DoesNotExist:
        pass

@staff_member_required    
@login_required(login_url="/product/login")
def view_profile(request):
    query = ProductSerial.objects.filter(owner=request.user)
    serial_keys = []
    for serial in query:
        serial_keys.append(serial.serial_number)

    return render(request, 'product/profile.html', {'serial_keys': serial_keys})

@staff_member_required
@login_required(login_url="/product/login")
def edit_username(request):
    error = ""
    if request.method == 'POST':
        new_name = request.POST['username']
        try:
            user = User.objects.get(username=new_name)
            error = "Username already exists."
        except User.DoesNotExist: 
            old_user = User.objects.get(username=request.user)
            old_user.username = new_name
            old_user.save()

            return render(request, 'product/edit_username.html',
                            {'done': True, 'new_name': new_name})
        except Exception as e:
            error = e

    form = ChangeUsernameForm(initial={'username': request.user})
    return render(request, 'product/edit_username.html',{'error': error, 'form': form})

@staff_member_required
@login_required(login_url="/product/login")
def get_serial_list(request, serial_key):
    return render(request, 'product/profile.html', {'serial_key': serial_key})

@staff_member_required
@login_required(login_url="/product/login")
def transmit_serial(request, serial_key):
    serial = ProductSerial.objects.get(serial_number=serial_key)
    if serial.owner == request.user:
        if request.method == "POST":
            result = request.POST['clicked']
            if result == 'true':
                if serial.reset_count > 0:
                    serial.owner = None
                    serial.reset_count -= 1
                    serial.save()
                    return HttpResponse('ok')
                else:
                    return HttpResponse(status=500, reason="No reset count remains.")
        return render(request, 'product/transmit_serial.html',
                        { 'serial_key': serial_key, 'product': serial.product,
                          'reset_count': serial.reset_count })
    else:
        return show_error(request, 500)

@api_view(['GET'])
def get_plans(request): 
    try:
        if request.GET.get('filter') is not None:
            query = PricingPolicy.objects.filter(method=request.GET.get('filter'))
        else:
            query = PricingPolicy.objects.all()
        result = PolicySerializer(query, many=True)
        print(result.data)
        return Response(result.data)
    except Exception as e:
        print(e)
        return Response()

@api_view(['GET'])
def get_plan(request, plan_id):
    try:
        query = PricingPolicy.objects.get(pricing_id=plan_id)
        result = PolicySerializer(query)
        return Response(result.data)
    except:
        return Response(status=500, reason="Plan is not exist")

@api_view(['GET'])
@staff_member_required
def get_cards(request):
    try:
        query = BillingInfo.objects.filter(owner=request.user)
        result = BillingInfoSerializer(query, many=True)
        return Response(result.data)
    except Exception as e:
        print(e)
        return Response()