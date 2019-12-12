from django import forms
from .models import *

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
    password_check = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")
    class Meta:
        model = User
        fields = ['userId', 'password', 'password_check', 'role']
        #fields = '__all__'
        
class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
    class Meta:
        model = User
        fields = ['userId', 'password']
        #fields = '__all__'
        
class UploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'     
