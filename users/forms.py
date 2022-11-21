from django import forms
from allauth.account.forms import SignupForm
from .models import User

class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        name = forms.CharField(max_length=30, label='First Name')

    # Put in custom signup logic
    def custom_signup(self, request, user):
        # Set the user's type from the form reponse
        user.name = self.cleaned_data['name']

        # Save the user's type to their database record
        user.save()