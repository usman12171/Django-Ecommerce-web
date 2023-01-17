from django.forms import ModelForm
from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,UserChangeForm
from django.utils.translation import gettext ,gettext_lazy as _

class userregister(UserCreationForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control','id':'emailfield'}))
    class Meta:
     model = User
     fields = ['username','email','password1','password2']
     widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

    def clean_email(self):
      email = self.cleaned_data['email']
      try:
        user = User.objects.get(email = email)
      except Exception as e:
            return email
      raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

class loginform(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_('password'),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class update_profile(UserChangeForm):
    class Meta: 
        model = User
        fields = {'username','first_name','last_name','email',}


class update_customer(forms.ModelForm):
    class Meta:
        model = Customer
        fields={'contact','address','country','city','zipcode','avatar'}


    def __init__(self, *args, **kwargs):
        super(update_customer, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False

