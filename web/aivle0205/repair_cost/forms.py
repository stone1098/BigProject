from django import forms
from .models import CarImageInput, CarImageOutput


class CarImageInputForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = CarImageInput
        fields = '__all__'
        exclude = ('user','img_id', 'img')
        widgets = {
          'img': forms.FileInput(attrs={'id':'file','class':'bg03-02-preview'}),
          'location' : forms.Textarea(attrs={'id':'location','class':"bg03-01"}), # TextInpout or Textarea
          'car_company' : forms.Textarea(attrs={'id':'car_company','class':"bg03-01"}),
          'car_type' : forms.Textarea(attrs={'id':'car_type','class':"bg03-01"}),
          'car_year' : forms.Textarea(attrs={'id':'car_year','class':"bg03-01"}),
        }


        
        

class CarImageOutputForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = CarImageOutput
        fields = '__all__'


