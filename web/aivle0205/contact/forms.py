from django import forms

class EmailForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)