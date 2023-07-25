from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.views import View

from .forms import EmailForm

def send_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            
            subject = f"새로운 이메일이 도착했습니다: {name}"
            email_body = f"보낸 사람: {name}\n이메일: {email}\n전화번호: {phone}\n\n{message}"
            to_email = ['asdfgyuio123@naver.com']

            EmailMessage(subject=subject, body=email_body, to=to_email).send()
            return render(request, 'contact.html', {'success_message': '이메일이 성공적으로 전송되었습니다!'})
        else:
            return render(request, 'contact.html', {'form': form, 'error_message': '입력한 정보가 올바르지 않습니다.'})
    else:
        form = EmailForm()
        return render(request, 'contact.html', {'form': form})