
from django.http import HttpResponse
from django.shortcuts import redirect

from .decorators import *
from django.contrib import messages

from django.shortcuts import render 

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                print('working',allowed_roles)
                return view_func(request,*args,**kwargs)
            else:
                messages.warning(request, f'User is not authorised to access this page !!!')
                return render(request,"account/home.html")
                # return redirect('home')
        return wrapper_func
    return decorator

def admins_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'Doctor' :
                return redirect('usernames')
            elif group == 'Patient' :
                return redirect('usernames')
            elif group == 'Admin' :
                return view_func(request, *args, **kwargs)

    return wrapper_func
