import datetime

from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import *

from django.urls import reverse

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
def product_login(req):
    """Checks logged in status"""
    if req.user.is_authenticated:
        return HttpResponseRedirect('/product/login_redirect/')
    return render(req, 'product/login.html')


@login_required
def product_login_redirect(req):
    return render(req, 'product/login_redirect.html')