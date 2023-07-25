from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from aivle0205.forms import UpdateProfileForm
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import AuthSms,User
from random import randint
import json
import hashlib
import hmac
import base64
import requests
import time
from django.contrib import messages
from django.http import HttpResponse
from .forms import PhoneVerificationForm
from django.views import View
from django.contrib.auth import logout
@csrf_protect
def signup(request):
    verified_phone = request.session.get('phone')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            del request.session['phone']
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=user.username, password=raw_password)
            messages.success(request, '회원 가입 되었습니다!')
            return redirect(reverse_lazy('login'))
    else:
        form = SignUpForm()
    
    form_errors = form.errors

    return render(request, 'registration/signup.html', {'form': form, 'form_errors': form_errors, 'verified_phone': verified_phone })

@csrf_protect
def phone_verification(request):
    return render(request, 'registration/phone_verification.html')

@login_required
@csrf_protect
def update(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)  
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('main')
    else:
        form = UpdateProfileForm(instance=request.user)  
        
    return render(request, 'registration/update.html', {'form': form})

@login_required
def delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)  
        return redirect('index')  
    else:
        return redirect('accounts:update') 


class AuthSmsSendView(View):
    @staticmethod
    def send_sms(phone_number, auth_number):
        url = 'https://sens.apigw.ntruss.com'
        uri = '/sms/v2/services/'
        serviceid = 'ncp:sms:kr:310050875034:sms_system'
        uri2 = '/messages'
        URI = uri + serviceid + uri2
        API_URL = url + URI

        ACCESS_KEY = 'NqeRJSTz4OWe854MZfrz'
        timestamp = str(int(time.time() * 1000))
        method="POST"
        message = method+" " + URI + "\n" + timestamp + "\n" + ACCESS_KEY
        message = bytes(message, 'UTF-8')

        SIGNATURE = AuthSmsSendView.make_signature(message)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': 'NqeRJSTz4OWe854MZfrz',
            'x-ncp-apigw-signature-v2': SIGNATURE
        }
        body = {
            'type': 'SMS',
            'contentType': 'COMM',
            'countryCode': '82',
            'from': '01072560188',
            'content': f'인증번호 [{auth_number}]를 입력해주세요.',
            'messages': [{"to": phone_number}]
        }
        requests.post(API_URL, headers=headers, data=json.dumps(body))

    @staticmethod
    def make_signature(string):
        secret_key = "eKv9kLWrAumWoUm9nGkfiNHRJXsSFs3eJ61iZESt"
        secret_key = bytes(secret_key, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, string, digestmod=hashlib.sha256).digest())
        return signingKey

    def post(self, request):
        try:
            data = json.loads(request.body)
            phone_number = data['phone_number']
            auth_number = str(randint(1000, 10000))

            AuthSms.objects.update_or_create(
                phone_number=phone_number,
                defaults={
                    'phone_number': phone_number,
                    'auth_number': auth_number
                }
            )

            self.send_sms(
                phone_number=phone_number,
                auth_number=auth_number
            )
            request.session['phone_number'] = phone_number
            request.session['auth_number'] = auth_number
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)

class SMSVerificationConfirmView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            phone_number = data['phone_number']
            auth_number = data['auth_number']
            # phone=request.session.get('phone_number')
            auth=request.session.get('auth_number')
            # auth_sms = AuthSms.objects.get(phone_number=phone_number)
            # 그냥 세션으로 가져와서 처리 db는 오류가 나서 계속 안됨
            if auth_number == auth :
                if not User.objects.filter(phone=phone_number).exists():
                    request.session['phone'] = phone_number
                    del request.session['phone_number']
                    del request.session['auth_number']
                    return JsonResponse({'message': 'SUCCESS'}, status=200)

                if User.objects.filter(phone=phone_number).exists():
                    return JsonResponse({'message': 'REGISTERED_NUMBER'}, status=401)
            else:
                return JsonResponse({'message': 'INVALID_NUMBER'}, status=403)
                
        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)
        
        
        
        
def logout_view(req):
    logout(req)

    return redirect('main')    