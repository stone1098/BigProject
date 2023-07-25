from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User,AuthSms
from django.contrib import admin
class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'phone', 'birthdate', 'password1', 'password2', 'first_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_last_step = False

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4 or len(username) > 16:
            raise forms.ValidationError('ID는 4자리에서 16자리 사이로 입력해주세요.')
        return username

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('이미 등록된 휴대폰 번호입니다.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 존재하는 이메일입니다.')
        return email
    
    
    
class PhoneVerificationForm(forms.Form):
    phone_number = forms.CharField(label='휴대전화 번호', max_length=11)
    auth_number = forms.IntegerField(label='인증번호')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        return phone_number

    def clean_auth_number(self):
        auth_number = self.cleaned_data['auth_number']
        return auth_number