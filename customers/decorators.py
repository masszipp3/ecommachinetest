from django.shortcuts import redirect,render
import re
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def is_customer(user):
    return user.is_authenticated and user.is_customer

def customerrequired(view_func):
    decorated_view = user_passes_test(is_customer, login_url=reverse_lazy('customers:signin'))
    return decorated_view(view_func)   