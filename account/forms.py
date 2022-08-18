from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import password_validation

class UserRegisterForm(UserCreationForm):
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['first_name','last_name', 'email','user_type','name','age','phone','image','specialization','address_line1','city', 'state', 'country','pincode']

from datetime import date
class UserForm(forms.ModelForm):            
        password = forms.CharField(widget=forms.PasswordInput())

        def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': '{}'.format(field).replace("_", ' ').capitalize(),

                })

            self.fields['email'].widget.attrs['placeholder'] = 'abc@xyz.com'
            self.fields['email'].required = True
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['password'].required = True

            if self.instance.pk:
                self.fields['email'].required = False
                self.fields['email'].widget.attrs['readonly'] = True
                self.fields['password'].widget.attrs['readonly'] = True
                self.fields['password'].required = False

        def save(self, *args, **kwargs):
            self.date_joined = date.today()
            super(UserForm, self).save(*args, **kwargs)
            return self

        class Meta:
            model = User
            fields = ('first_name','last_name','email','user_type','age','phone','image','address_line1','city','state','country','pincode')
            exclude = ('date_joined','about_company')

class BlogForm(forms.ModelForm):
    publish_on = forms.CharField(label='published_on', 
                    widget=forms.TextInput(attrs={'placeholder': '2022-05-05 14:03:11'}))
    class Meta:
        model = Blog
        fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'Starttime_of_appointment': forms.TextInput(
                attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }

class AppointmentSlotForm(forms.ModelForm):
    class Meta:
        model = AppointmentSlot
        fields = '__all__'
        widgets = {
            'date':forms.TextInput(
                attrs={'placeholder': 'YYYY-MM-DD'}),
            'start_time': forms.TextInput(
                attrs={'placeholder': ' HH:MM:SS'}),
            'end_time': forms.TextInput(
                attrs={'placeholder': 'HH:MM:SS'}),
            
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
       

