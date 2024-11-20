from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

# I wrote this code
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'profile-update'}), label='first name')
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'profile-update'}), label='last name')
    dob = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',attrs={'class': 'profile-update', 'type': 'date'}), label='date of birth')
    pfp = forms.ImageField(label='profile image', required=False)
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'dob', 'pfp']

class PostsForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control',}), label='')
    image = forms.ImageField(required=False, label='upload', widget=forms.FileInput(attrs={'class': 'form-control-file','id': 'image',}))

    class Meta:
        model = Posts
        fields = ['text', 'image']

class ChatroomForm(forms.ModelForm):
    chatroom = forms.CharField(required=True,)
    class Meta:
        model = Chatroom
        fields = ['chatroom']
# end of code I wrote