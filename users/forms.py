from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm, PasswordField
from allauth.account.forms import ChangePasswordForm
from django import forms
from .models import *
# from . import app_settings

class SimpleSignupForm(SignupForm):
    name = forms.CharField(max_length=12, label='name', widget=forms.TextInput(attrs={'placeholder': 'name'}))
    avatar = forms.ImageField(label='avatar', required=False, widget=forms.FileInput(attrs={'placeholder': 'avatar', 'value':"avatars/avatar.png"}))
    # password1 = PasswordField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': 'password1'}))
    def __init__(self, *args, **kwargs):
        super(SimpleSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['avatar']
    
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        avatar = cleaned_data.get("avatar")
        if avatar is None:
            self.add_error("avatar", ("You must upload an image"))
        password = self.cleaned_data.get("password1")
        if password is None:
            self.add_error("password1", ("You must enter a password"))
        if (
            "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    ("You must type the same password each time."),
                )
        return self.cleaned_data

    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.avatar = self.cleaned_data['avatar']
        user.save()
        return user
    # email.widget.attrs.update({'class': 'form-control'})
    avatar.widget.attrs.update({'class': 'form-control file-upload', 'type': 'file', 'id': "imageUpload", 'accept' :".png, .jpg, .jpeg"})
    name.widget.attrs.update({'class': 'form-control'})
    # password1.widget.attrs.update({'class': 'form-control'})

class SimpleLoginForm(LoginForm):
    password = PasswordField(label="Password", autocomplete="current-password")
    remember = forms.BooleanField(label="Remember Me", required=False)
    error_messages = {
        "account_inactive": ("This account is currently inactive."),
        "email_password_mismatch": (
            "The e-mail address and/or password you specified are not correct."
        ),
        "username_password_mismatch": (
            "The username and/or password you specified are not correct."
        ),
    }
    # login = forms.EmailField(max_length=254, label='email', widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(SimpleLoginForm, self).__init__(*args, **kwargs)
        self.fields["login"] = forms.EmailField(max_length=254, label='email', widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'form-control'}))

    password.widget.attrs.update({'class': 'form-control'})
    remember.widget.attrs.update({'class': 'form-check-input'})




class ProfileForm(forms.ModelForm):
    # Get user
    # user = User.objects.get(user_logged_in)
    # data = SocialAccount.objects.filter(user=user, provider='google')
    # if data==None:
    # password1 = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
    # password2 = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password again'}))


    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)
    password1.widget.attrs.update({'class': 'form-control', 'placeholder': 'password'})
    password2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password again'})
    class Meta:
        model = User
        fields = ['name', 'avatar', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'd-none', 'type': 'file', 'id': "photo", 'accept' :".png, .jpg, .jpeg" }),
        }
    # validation
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        avatar = cleaned_data.get("avatar")
        if avatar is None:
            self.add_error("avatar", ("You must upload an image"))
        password = self.cleaned_data.get("password1")
        if password is None:
            self.add_error("password1", ("You must enter a password"))
        if (
            "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error('password2', ("You must type the same password each time."))
        return self.cleaned_data
    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        
        password = self.cleaned_data.get("password1")
        if (
            "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    ("You must type the same password each time."),
                )
            if self.cleaned_data["password1"] != "":
                    print('herrreee')
                    print(self.cleaned_data["password1"])
                    user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    # validate password
    # def clean_password(self):
    #     cleaned_data = super(ProfileForm, self).clean()
    #     password = self.cleaned_data.get("password1")
    #     if password is None:
    #         self.add_error("password1", ("You must enter a password"))
    #     if (
    #         "password1" in self.cleaned_data
    #         and "password2" in self.cleaned_data
    #     ):
    #         if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
    #             self.add_error(
    #                 "password2",
    #                 ("You must type the same password each time."),
    #             )
    #     return self.cleaned_data
    