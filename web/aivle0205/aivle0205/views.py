# views.py
from django.shortcuts import render

from django.shortcuts import render, redirect
from aivle0205.forms import UpdateProfileForm
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

def index(req):
    return render(req, 'index.html')
def main(req):
    return render(req, 'main.html')

def contact(req):
    return render(req, 'contact.html')

def about(req):
    return render(req, 'about.html')

def test_view(request):
    return render(request, 'test.html')

def account(req):
    return render(req, 'account.html')
