from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.hashers import check_password
from .models import Profile
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from home.views import main
import json
# Create your views here.

@login_required
def extendUnread(request):
    request.user.notifications.mark_all_as_read()
    qset = request.user.notifications.all()[:20]
    return render(request,'notifications/list.html',{'notifications':qset,'title':'Notifications | ClickTime'})


@login_required
def index(request):
    user_profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance=user_profile)
    context={
        'title':'Profile | ClickTime',
        'form':form,
        'user':user_profile,
    }
    if not user_profile.email_confirmed:
        context['email_not_confirmed'] = 'You have not confirmed your email address'

    if request.method == 'POST':
        form=ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            if request.FILES:
                user_profile.picture = request.FILES['picture']
    
            user_profile.save()
            return redirect(main)
        else:
            context['message'] =  'Something went wrong!'
            return render(request, "profile/index.html",context=context)

    return render(request, "profile/index.html",context=context)

@login_required
def validate_username(request):
        if request.method == 'GET':
            res = {}
            username = request.GET.get('username')
            res = {
            'taken' : Profile.objects.filter(username__iexact=username).exists(),
            }
            return HttpResponse(json.dumps(res))


@login_required
def account_settings(request):
    user_profile = request.user.profile
    context = {
        'title':'Settings | ClickTime',
        'user_profile':user_profile,
    }
    if not user_profile.email_confirmed:
        context['email_not_confirmed'] = 'You have not confirmed your email address'

    return render(request, 'profile/settings.html', context = context)


@login_required
def confirm_del(request):
    user = request.user
    context ={
        'title':'Delete my account | ClickTime',
        'user':user
    }

    if request.method == 'POST':
        password = request.POST['password']
        current_password = user.password

        if check_password(password, current_password):
            return redirect('delete_user')
        else:
            context['message'] = 'wrong password!'
            return render(request, 'profile/confirm_del.html',context=context)
    
    return render(request, 'profile/confirm_del.html',context=context)


@login_required
def confirm_deactivate(request):
    user = request.user
    context ={
        'title':'Deactivate my account | ClickTime',
        'user':user,
        'confirm_deactivate':True
    }

    if request.method == 'POST':
        password = request.POST['password']
        current_password = user.password

        if check_password(password, current_password):
            return redirect('deactivate_user')
        else:
            context['message'] = 'wrong password!'
            return render(request, 'profile/confirm_del.html',context=context)
    
    return render(request, 'profile/confirm_del.html',context=context)
    



@login_required
def delete_user(request):
    user = request.user
    user.delete()
    
    context = {
        'title':'ClickTime',
        'message':'User account has been successfully deleted.'
    }
    return render(request, 'profile/delete_deactivate.html',context=context)


@login_required
def deactivate_user(request):
    user = request.user
    user.is_active = False
    user.save()
    context = {
        'title':'ClickTime',
        'message':'User account has been successfully deactivated!'
    }
    return render(request, 'profile/delete_deactivate.html',context=context)


@login_required
def followers(request):
    context={
        'title':'ClickTime',
        'users':request.user.profile.followers.all()
        
    }
    return render(request, 'profile/followers.html',context=context)

@login_required
def following(request):
    context={
        'title':'ClickTime',
        'users':request.user.profile.following.all(),
        'username':request.user.profile.username
    }
    return render(request, 'profile/following.html',context=context)

@login_required
def blocked(request):
    context={
        'title':'ClickTime',
        'users':request.user.profile.blocking.all(),
        'username':request.user.profile.username
    }
    return render(request, 'profile/blocked.html',context=context)


@login_required
def likes(request):
    context={
        'title':'ClickTime',
        'likes':request.user.profile.likes.all(),
        'user':request.user.profile
    }
    return render(request, 'profile/likes.html',context=context)

