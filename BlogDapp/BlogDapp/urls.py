"""BlogDapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render, redirect, reverse
from django.views.generic import RedirectView
from django.contrib import auth
from django.contrib.auth.models import Permission
from django.conf import settings
from django.urls.exceptions import NoReverseMatch
from django.http import HttpResponse
import json


def get_redirect_url(request):
    if request.GET.get('next'):
        return request.GET.get('next')
    elif request.POST.get('next'):
        return request.POST.get('next')
    elif settings.LOGIN_REDIRECT_URL:
        try:
            url = reverse(settings.LOGIN_REDIRECT_URL)
        except NoReverseMatch:
            url = settings.LOGIN_REDIRECT_URL
        return url


def login(request):
    if not request.user.is_authenticated:
        return render(request, 'web3auth/login.html')
    else:
        return redirect('/blogs')


def auto_login(request):
    if not request.user.is_authenticated:
        return render(request, 'web3auth/autologin.html')
    else:
        return redirect('/blogs')


def logout(request):
    auth.logout(request)
    return redirect('/blogs')


def go_plus(request):
    if not request.user.is_authenticated:
        return render(request, 'web3auth/autologin.html')

    if request.user.has_perm('Blog.view_blog'):
        return redirect('/blogs')
    else:
        return render(request, "web3auth/goplus.html")


def go_plus_auth(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'web3auth/autologin.html')

        if request.user.has_perm('Blog.view_blog'):
            return redirect('/blogs')
        else:
            permission = Permission.objects.get(name='Can view blog')
            request.user.user_permissions.add(permission)
            resp = {'redirect_url': get_redirect_url(request), 'status': 'OK'}

            return HttpResponse(json.dumps(resp), content_type='application/json')
    else:
        return render(request, "web3auth/goplus.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', RedirectView.as_view(url='/login')),
    re_path(r'^login/', login, name='login'),
    re_path(r'^auto_login/', auto_login, name='autologin'),
    re_path(r'^logout/', logout, name='logout'),
    re_path(r'^goplus/$', go_plus, name='go_plus'),
    re_path(r'^authenticate/$', go_plus_auth, name='go_plus_auth'),
    re_path(r'', include('web3auth.urls')),
    path('blogs/', include('Blog.urls')),
]
