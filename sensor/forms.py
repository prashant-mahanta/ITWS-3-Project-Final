from django.contrib.auth.models import User
from django import forms
from .models import Plant
class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	email=forms.EmailField(label='Email')
	class Meta:
		model=User
		fields=['username','email','password']
class LoginForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model=User
		fields=['username','password']
class AddPlant(forms.ModelForm):
	plant_type=forms.CharField(label='Plant type')
	class Meta:
		model=Plant
		fields=['plant_type']
