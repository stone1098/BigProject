from django import forms
from .models import CarTextInput, CarTextOutput


class CarTextInputForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = CarTextInput
        fields = '__all__'
        exclude = ('user','text_id')
        widgets = {
          'accident_report': forms.Textarea(attrs={'id':'reportbox','class': 'reportbox', 'placeholder' : '사고 경위서 작성해주세요..'}),
        }
        labels = {
            'accident_report': ""
        }

class CarTextOutputForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = CarTextOutput
        fields = '__all__'