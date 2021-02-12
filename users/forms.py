from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.helper import FormHelper


User = get_user_model()

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(max_length=254, help_text="یک ایمیل درست وارد کنید.", required=False)
    # first_name = forms.CharField(max_length=100,required=True)
    # last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User

        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'mobile', 'avatar']