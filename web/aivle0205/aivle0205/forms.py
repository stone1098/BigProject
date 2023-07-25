from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
class UpdateProfileForm(UserCreationForm):
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'birthdate','password1','password2', 'address', 'first_name', 'last_name']

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if username and (username != self.instance.username or not self.instance.username):
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('이미 사용 중인 사용자 이름입니다.')

        return username
      
    def clean_email(self):
      cleaned_data = super().clean()
      email = cleaned_data.get('email')

      if email and (email != self.instance.email or not self.instance.email):
          if User.objects.filter(email=email).exists():
              raise forms.ValidationError('이미 사용 중인 이메일입니다.')

      return email 