from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm, PasswordField
from django import forms
from .models import *

class SimpleSignupForm(SignupForm):
    name = forms.CharField(max_length=12, label='name', widget=forms.TextInput(attrs={'placeholder': 'name'}))
    avatar = forms.ImageField(label='avatar', widget=forms.FileInput(attrs={'placeholder': 'avatar'}))
    password1 = PasswordField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': 'password1'}))
    def __init__(self, *args, **kwargs):
        super(SimpleSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.avatar = self.cleaned_data['avatar']
        user.save()
        return user
    # email.widget.attrs.update({'class': 'form-control'})
    avatar.widget.attrs.update({'class': 'file-upload', 'type': 'file', 'id': "imageUpload", 'accept' :".png, .jpg, .jpeg"})
    name.widget.attrs.update({'class': 'form-control'})
    password1.widget.attrs.update({'class': 'form-control'})

class SimpleLoginForm(LoginForm):
    password = PasswordField(label="Password", autocomplete="current-password")
    remember = forms.BooleanField(label="Remember Me", required=False)
    # login = forms.EmailField(max_length=254, label='email', widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(SimpleLoginForm, self).__init__(*args, **kwargs)
        self.fields["login"] = forms.EmailField(max_length=254, label='email', widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'form-control'}))

    # def login(self, *args, **kwargs):
        # return super(SimpleLoginForm, self).login(*args, **kwargs)
        # Add your own processing here.

        # You must return the original result.
        # return result
    # login.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
    remember.widget.attrs.update({'class': 'form-check-input'})
    