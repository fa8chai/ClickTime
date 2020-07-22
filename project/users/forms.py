from django.contrib.auth.forms import UserCreationForm, UserChangeForm, forms, PasswordChangeForm
from .models import *


class CustomPasswordResetForm(PasswordChangeForm):
    
    old_password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    old_password.widget.attrs.update({'placeholder':('Old password'),'class':('form-control')})
    new_password1.widget.attrs.update({'placeholder':('Password'),'class':('form-control')})        
    new_password2.widget.attrs.update({'placeholder':('Repeat password'),'class':('form-control')})
    
 




class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': True,'placeholder':('First Name'),'class':('form-control')})
        self.fields['last_name'].widget.attrs.update({'placeholder':('Last Name'),'class':('form-control')})
        self.fields['email'].widget.attrs.update({'placeholder':('Email'),'class':('form-control')})
        self.fields['password1'].widget.attrs.update({'placeholder':('Password'),'class':('form-control')})        
        self.fields['password2'].widget.attrs.update({'placeholder':('Repeat password'),'class':('form-control')})

   
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           
        self.fields['email'].widget.attrs.update({'class':('form-control'),})

    def clean_email(self):
        email = self.cleaned_data['email']

        if self.instance.pk is not None and self.instance.email == email:
            raise forms.ValidationError('This is your current email address!')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Email address {email} already exists!')
        
        return email            

    def save(self, *args, **kwargs):
        user = self.instance
        user.email = self.cleaned_data['email']
        user.is_active = False
        user.profile.email_confirmed = False
        user.save()
        return user

