from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login, authenticate
from .forms import CustomUserCreationForm, CustomPasswordResetForm, EmailChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, email_confirmation_token, change_email_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from users.models import CustomUser
from home.views import main, search, error
from profile.views import index
from notifications.signals import notify
from django.utils import timezone
from  profile.models import Profile


User = CustomUser


# Create your views here.

def signup(request):
    form = CustomUserCreationForm()
    context={
        'form': form,
        'title':'ClickTime'
    }
    if request.method=="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            current_site = get_current_site(request)

            mail_subject = 'Confirm your ClickTime account.'
            message = render_to_string('users/confirm_acc.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':email_confirmation_token.make_token(user),

            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to = [to_email])
            email.send()

            password = form.cleaned_data.get('password1')
            user = authenticate(request, username = to_email, password = password)
            if user is None:
                context['error'] = 'Invalid credentials'
                return render(request, 'users/signup.html', context=context)
            login(request, user)
            return render(request,'users/confirmation_link.html',{'title':'ClickTime'})
        
        print('not-valid')
        context['form'] = form
        return render(request, 'users/signup.html', context=context)
    return render(request, 'users/signup.html',context=context)



def signin(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        if '@' in email:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None
        else:
            try:
                user = Profile.objects.get(username=email).user
            except Profile.DoesNotExist:
                user = None
        if user and user.check_password(password) and user.is_active:
                login(request, user)
                notify.send(sender = user , recipient = user, verb='logged in', description=f'There was a login to your account {email}.' )
                return redirect(main)

        if user and user.check_password(password) and not user.is_active:
                    return render(request,'users/disabled_account.html',{'title':'ClickTime','user':user})

        elif user is None :
            context={
                'error':"The username or email you entered doesn't belong to an account.",
                'title':'Log In |  ClickTime'
            }
            return render(request, "users/login.html",context=context)

        else:
            context={
                'error':"Invalid credentials",
                'title':'Log In | ClickTime'
            }
            return render(request, "users/login.html",context=context)
    return render(request, "users/login.html",{'title':'Log In | ClickTime'})


@login_required
def signout(request):
    logout(request)
    return redirect(signin)


@login_required
def resend_email(request):
    user = request.user
    context = {
        'title':'Send email confirmation link | ClickTime',
    }
    if request.method == 'POST':
        entered_email = request.POST['email']
        
        if request.user.email != entered_email:
            context['message'] = 'Looks like you entered the wrong email address!'
            return render(request, 'users/resend_email.html', context=context)
        else:
            
            current_site = get_current_site(request)
            mail_subject = 'Confirm your ClickTime account.'
            message = render_to_string('users/confirm_acc.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':email_confirmation_token.make_token(user),

            })
            to_email = entered_email
            email = EmailMessage(mail_subject, message, to = [to_email])
            email.send()
            context['message_true'] = 'A Confirmation Email has been sent to you.'  
            return render(request, 'users/resend_email.html', context=context)
    return render(request, 'users/resend_email.html', context=context)


def confirm_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_confirmation_token.check_token(user, token):
        user.profile.email_confirmed = True
        user.save()
        if not request.user.is_authenticated:
            login(request, user)
        return redirect(main)

    else:
        return redirect(error, message = 'Confirmation link is invalid!')


def send_activation_email(request):
    context = {
        'title':'Reactivate my account | ClickTime'
    }
    if request.method == 'POST':
        entered_email = request.POST['email']
        
        try:
            user = User.objects.get(email = entered_email)
        except User.DoesNotExist:
            return redirect(error, message='User not found!')
            
        current_site = get_current_site(request)
        mail_subject = 'Reactivate your ClickTime account.'
        message = render_to_string('users/reactivate_acc.html',{
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),

        })
        to_email = entered_email
        email = EmailMessage(mail_subject, message, to = [to_email])
        email.send()
        context['message_true'] = 'Reactivation link has been sent to you.'  
        return render(request, 'users/activation_email.html', context=context)

    return render(request, 'users/activation_email.html', context=context)



def reactivate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return redirect(main)

    else:
        return redirect(error, message = 'Reactivation link is invalid!')


def forget_password(request):
    context = {
        'title':'ClickTime',
    }
    if request.method == 'POST':

        entered_email = request.POST['email']
        try:
            user = User.objects.get(email = entered_email)
        except User.DoesNotExist:
            context['message'] = "The email you entered doesn't belong to an account!"                
            return render(request, 'users/forget_password.html', context=context)
    
        token_generator = PasswordResetTokenGenerator()
        current_site = get_current_site(request)
        mail_subject = 'Reset your ClickTime account password.'
        message = render_to_string('users/password_acc.html',{
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':token_generator.make_token(user),

        })
        to_email = entered_email
        email = EmailMessage(mail_subject, message, to = [to_email])
        email.send()
        context['message_true'] = 'An email with password reset instructions has been sent to you.'  
        return render(request, 'users/forget_password.html', context=context)
    return render(request, 'users/forget_password.html', context=context)



def reset_password(request, uidb64, token):
    token_generator = PasswordResetTokenGenerator()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        login(request,user)
        return redirect('reset_password_confirm')
    else:
        return redirect(error, message = 'Password reset link is invalid!')


def reset_password_confirm(request):
    form = CustomPasswordResetForm(request.user)
    context = {
        'title':'Password reset | ClickTime',
        'form':form,
    }
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.user,request.POST)
        if form.is_valid() :
            form.save()
            if not request.user.is_authenticated:
                return redirect(login)
            else:
                return redirect(main)
        context['form'] = form
        return render(request, 'users/reset_password.html', context=context)
    return render(request, 'users/reset_password.html', context=context)

    
@login_required
def change_email(request):
    form = EmailChangeForm(instance=request.user)
    context={
        'title':'ClickTime',
        'form':form
    }
    if request.method == 'POST':
        form = EmailChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)

            mail_subject = 'ClickTime change your email address.'
            message = render_to_string('profile/change_email_acc.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':change_email_token.make_token(user),

            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to = [to_email])
            email.send()

            context['message']= 'Email change link has been sent to you'
            return render(request, 'profile/change_email.html', context=context)

        context['form'] = form
        return render(request, 'profile/change_email.html', context=context)

    return render(request, 'profile/change_email.html', context=context)



def change_email_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and change_email_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()

        login(request, user)
        return redirect(main)

    else:
        return redirect(error, message = 'Reactivation link is invalid!')
