from django import forms
from django.contrib.auth.models import User
from .models import Profile


class Loginform(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username_login',
                                                                            'class': 'form-control',
                                                                            'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password_login',
                                                                 'class': 'form-control', 'placeholder': 'Password'}))


class Signupform(forms.Form):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'email', 'faculty', 'enroll', 'password', 'confirm_pass')

    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username',
                                                                            'class': 'form-control',
                                                                            'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'first_name',
                                                                              'class': 'form-control',
                                                                              'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'last_name',
                                                                             'class': 'form-control',
                                                                             'placeholder': 'Last name'}))
    email = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'email',
                                                                         'class': 'form-control',
                                                                         'placeholder': 'somone@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password',
                                                                 'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password',
                                                                         'class': 'form-control',
                                                                         'placeholder': 'Confirm Password'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        try:
            User.objects.get(username=username)
            print("raier")
            raise forms.ValidationError("username taken.")

        except User.DoesNotExist:
            pass

        if password != confirm_password:
            raise forms.ValidationError("The passwords don't match.")
