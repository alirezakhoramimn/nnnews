from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# crispy form will help us a lot to fashion our forms
# so we install it then we go to settings for installed app.


class UserRegisterFrom(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
# heasm -->> Manalihastam

# A model form
# it allows us to create a from that works with a specific database model
class UserUpdateForm(forms.ModelForm):
    # in this class we will just update the email and the username
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", 'email']
        # we don't have the image form in here because it is build in models
        # we import it at top


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
