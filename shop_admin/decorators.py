from django.shortcuts import redirect,render
import re
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

def is_shopadmin(user):
    return user.is_authenticated and user.is_shopadmin

def shopadminrequired(view_func):
    decorated_view = user_passes_test(is_shopadmin, login_url=reverse_lazy('shop_admin:signin'))
    return decorated_view(view_func)   