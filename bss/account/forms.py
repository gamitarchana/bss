from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.contrib.auth.forms import PasswordResetForm
from bss.user.models import UserProfile
#User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if not user:
                raise forms.ValidationError('Username and password are incorrect')
            #if not user.check_password(password):
            #    raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('User is not active')

            return super(LoginForm, self).clean(*args, **kwargs)

class UserSignUpForm(forms.ModelForm):
    email = forms.EmailField(label = 'Email Address')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
    def clean(self):
        print("clean")
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        print("clean_password")
        print(password)
        print(password2)
        if password != password2:
            print("not equal")
            raise forms.ValidationError('Passwords must match')


    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = UserProfile.objects.filter(username=username)
        if username_qs.exists():
            print("username_qs.exists")
            raise forms.ValidationError("This username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = UserProfile.objects.filter(email=email)
        if email_qs.exists():
            print("email_qs.exists")
            raise forms.ValidationError("This email already exists")

        return email

    '''def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        print("clean_password")
        print(password)
        print(password2)
        if password != password2:
            print("not equal")
            raise forms.ValidationError('Passwords must match')

        return password'''


class UserPasswordResetForm(PasswordResetForm):
    #email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    class Meta:
        model = UserProfile
    '''    fields = ("email")
    def clean_email(self):
        email = self.cleaned_data['email']
        if function_checkemaildomain(email) == False:
            raise forms.ValidationError("Untrusted email domain")
        elif function_checkemailstructure(email)==False:
            raise forms.ValidationError("This is not an email adress.")

        return email'''
