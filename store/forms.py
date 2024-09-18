from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import Profile

class RegisterUser(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'name':'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'name':'last_name'}))
    usable_password = None # to hide the Password-authan
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(RegisterUser, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UpdateUserForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'name':'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'name':'last_name'}))
    password = None # to hide the Password-authan
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email']
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            

class UpdatePassword(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    def __init__(self, *args, **kwargs):
        super(UpdatePassword, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), required=False)
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}), required=False)
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
    governorate = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Governorate or State'}), required=False)
    
    class Meta: 
        model = Profile
        fields = ('phone', 'address', 'city', 'governorate',)
