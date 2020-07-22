from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from .forms import PostForm
from .models import Post, Image, Like
from profile.models import Profile, UserFollowing, UserBlocking
import uuid
from django.db.models import Max
import json
from notifications.signals import notify

# Create your views here.



@login_required
def main(request):
    print('Hello')
    user_profile = Profile.objects.get(user = request.user)
    posts = user_profile.posts.all().order_by('-created_on')
    context={
        'title': 'Home | ClickTime ',
        'user':user_profile,
        'posts':posts,
    }
    if not user_profile.email_confirmed:
        context['email_not_confirmed'] = 'You have not confirmed your email address!'
    if posts:
        return render(request, 'home/main.html',context=context)
    else:
        context['message'] = "You haven't created any posts yet."
        return render(request,'home/main.html',context=context)

def error(request,message):
    context={
        'title':'Error | ClickTime',
        'message':message
    }
    return render(request, 'home/error.html', context=context)


def get_user(request, username):
    try:
        user = Profile.objects.get(username = username)
    except Profile.DoesNotExist:
        return redirect(error, message='User Not Found!')
    
    context={
            'title': 'ClickTime',
            'user':user,
        }
    if request.user.is_anonymous :
        posts = user.posts.all().order_by('-created_on')
        if posts:
            context['posts'] = posts
            return render(request, 'home/main.html',context=context)
        else:
            context['message'] = f"Oops! {user.username} hasn't posted ."
            return render(request,'home/main.html',context=context)
    elif not request.user.is_anonymous and not request.user.profile.username == username:
        try:
            d = user.blocking.get(blocking_user_id=request.user.profile)
        except UserBlocking.DoesNotExist:
            d = None
        if d:
            return redirect(error,message='User Not Found!')
        else:
            posts = user.posts.all().order_by('-created_on')
            try:
                rel = request.user.profile.following.get(following_user_id = user.id)
            except UserFollowing.DoesNotExist:
                rel = None
            if rel:
                context['following'] = 'following'
            else:
                context['not_following'] = 'not_following'

            try:
                rel2 = request.user.profile.blocking.get(blocking_user_id = user.id)
            except UserBlocking.DoesNotExist:
                rel2 = None
            if rel2 :
                context['blocked'] = 'blocked'
            else:
                context['not_blocked'] = 'not_blocked'
        
            if posts:
                context['posts'] = posts
                return render(request, 'home/main.html',context=context)
            else:
                context['message'] = f"Oops! {user.username} hasn't posted ."
                return render(request,'home/main.html',context=context)
    else:
        return redirect(main)
        



@login_required()
def create_post(request):
    postForm = PostForm()
    user_profile = request.user.profile
    context = {
        'title':'New Post | ClickTime',
        'postForm':postForm,
    }
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        if postForm.is_valid():
            if not user_profile.email_confirmed and user_profile.posts.count() == 3:
                notify.send(sender = user_profile.user, recipient = user_profile.user, verb='tried to upload a new post',description = 'Please confirm your email address to post again.' )
                context['email_not_confirmed'] = 'You need to confirm your account to post more than three posts!'
                return render(request, "home/post.html", context=context)
                
            else:
                print('valid')
                post = postForm.save(commit=False)
                post.user = request.user.profile
                post.text = postForm.cleaned_data['text']
                post.save()

                try:
                    for image in request.FILES.getlist('images'):
                        inctance = Image(post = post, image = image)
                        inctance.save()
                except (TypeError, ValueError, OverflowError):
                    context['error'] = 'something went wrong!'
                    return render(request, "home/post.html", context=context)
        
                return redirect(main)
        else:   
            print('not-valid') 
            context['postForm'] = postForm
            return render(request, "home/post.html", context=context)
    return render(request, "home/post.html", context=context)


@login_required()
def view_post(request, username, post_id):
    try:
        val = uuid.UUID(post_id, version=4)
        post = Post.objects.get(pk = post_id)
    except (ValueError, Post.DoesNotExist):
        return redirect(error, message='No Post Found!')

    try:
        post_user = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        return redirect(error, message='No User Found!')

    try:
        d = request.user.profile.blocking.get(blocking_user_id=post_user)
    except UserBlocking.DoesNotExist:
        d = None
    if d:
        return redirect(error, message='You Have Blocked This User')
        
    else:          
        context = {
            'title': 'ClickTime',
            'post':post,
            'likes':post.likes.count(),
            'comments':post.comments.all(),
            'user':request.user.profile
        }
        if request.user.profile.username == username:
            context['myPost'] = True
        else:
            context['myPost'] = False
        return render(request, 'home/post_details.html',context=context)
    

@login_required
def delete_post(request, post_id):
    try:
        val = uuid.UUID(post_id, version=4)
        post = Post.objects.get(pk = post_id)
    except (ValueError, Post.DoesNotExist):
        return redirect(error, message='No Post Found!') 
    post.delete()
    return redirect(main)  





def search(request):
    blocked_users = set()
    for e in request.user.profile.blocking.filter(user_id = request.user.profile).select_related('blocking_user_id'):
        blocked_users.add(e.blocking_user_id)

    blocked_users_id = set()
    for e in request.user.profile.blocking.filter(user_id = request.user.profile).select_related('blocking_user_id'):
        blocked_users_id.add(e.blocking_user_id.user)

    if request.GET.get('search'): 
        try:
            key = request.GET.get('search')
            users = Profile.objects.filter(username__icontains=key).exclude(user__in=blocked_users_id)
        except Profile.DoesNotExist:
            users = None
        
        try:
            posts = Post.objects.filter(text__icontains=key).exclude(user__in=blocked_users)
        except Post.DoesNotExist:
            posts = None

        context = {
            'title':'Search | ClickTime',
            'users':users,
            'posts':posts,
            'key':key
        }
        return render(request,'home/search_res.html',context=context)
    else:
        posts= Post.objects.all().order_by('-created_on').exclude(user__in=blocked_users)

        context={
            'title':'Search | ClickTime',
            'posts':posts,
        }
        return render(request,'home/search.html',context = context)



def users_search(request,key):
    blocked_users = set()
    for e in request.user.profile.blocking.filter(user_id = request.user.profile).select_related('blocking_user_id'):
        blocked_users.add(e.blocking_user_id)
    try:
        users = Profile.filter(username__icontains=key).exclude(blocked_users)
    except Profile.DoesNotExist:
        users = None
    
    context={
        'title':'Search | ClickTime',
        'users':users,
    }
    return render(request,'home/users_search.html',context=context)


def load_comments(request):
    if request.method == 'GET' :
        post_id = request.GET.get('post_id')
        num = int(request.GET.get('num'))
        print(num)
        try:
            val = uuid.UUID(post_id, version=4)
            post = Post.objects.get(pk = post_id)
        except (ValueError, Post.DoesNotExist):
            return redirect(error, message='No Post Found!') 
        comments = post.comments.all().order_by('-created_on')[num:num+5]
        data = serializers.serialize('json', list(comments))
        res = {
            'data':data
        }
        return HttpResponse(json.dumps(res))
    else:
        return redirect(error, message='ERROR')

@login_required
def follow(request):
    user = request.user.profile
    current_user = request.GET.get('username')
    try:
        current_user = Profile.objects.get(username = current_user)
    except Profile.DoesNotExist:
        return redirect(error, message='User not found!')
    try:
        d = user.following.get(following_user_id=current_user)
    except UserFollowing.DoesNotExist:
        d = None
    if d:
        return redirect(error,message='You Are Following This User')

    user.follow(current_user)
    notify.send(sender = user.user , recipient = current_user.user, verb='is following you', description='' )
    res = {
        'data':'follow'
    }
    return HttpResponse(json.dumps(res))

@login_required
def block(request):
    user = request.user.profile
    current_user = request.GET.get('username')
    try:
        current_user = Profile.objects.get(username = current_user)
    except Profile.DoesNotExist:
        return redirect(error, message='User not found!')
    try:
        d = user.blocking.get(blocking_user_id=current_user)
    except UserBlocking.DoesNotExist:
        d = None
    if d:
        return redirect(error, message='You Have Blocked This User')
        
    user.block(current_user)
    res = {
        'data':'block'
    }
    return HttpResponse(json.dumps(res))


@login_required
def unfollow(request):
    user = request.user.profile
    current_user = request.GET.get('username')
    try:
        current_user = Profile.objects.get(username = current_user)
    except Profile.DoesNotExist:
        return redirect(error, message='User not found!')
    
    try:
        user.unfollow(current_user)
    except UserFollowing.DoesNotExist:
        return redirect(error, message='Unexpected error!')
        
    res = {
        'data':'unfollow'
    }
    return HttpResponse(json.dumps(res))


@login_required
def unblock(request):
    user = request.user.profile
    current_user = request.GET.get('username')
    try:
        current_user = Profile.objects.get(username = current_user)
    except Profile.DoesNotExist:
        return redirect(error, message='User not found!')
    
    try:
        user.unblock(current_user)
    except UserBlocking.DoesNotExist:
        return redirect(error, message='Unexpected error!')
        
    res = {
        'data':'unblock'
    }
    return HttpResponse(json.dumps(res))



@login_required
def like(request):
    post_id = request.GET.get('post_id')
    try:
        val = uuid.UUID(post_id, version=4)
        post = Post.objects.get(pk = post_id)
    except (ValueError, Post.DoesNotExist):
        return redirect(error, message='No Post Found!') 
    user = request.user
    notify.send(sender = user , recipient = post.user.user, verb='liked your post', action_object=post)
    res = {
        'data':'succsess'
    }
    return HttpResponse(json.dumps(res))
            


@login_required
def ch_like(request):
    post_id = request.GET.get('post_id')
    try:
        val = uuid.UUID(post_id, version=4)
        post = Post.objects.get(pk = post_id)
    except (ValueError, Post.DoesNotExist):
        return redirect(error, message='No Post Found!') 

    try:
        liked = post.likes.get(user=request.user.profile,post=post)
    except Like.DoesNotExist:
        liked = None

    if liked is not None:
        res = {
        'data':'Liked'
        }
        return HttpResponse(json.dumps(res))
    else:
        res = {
        'data':'Like'
        }
        return HttpResponse(json.dumps(res))


@login_required
def users_liked(request, username, post_id):
    try:
        val = uuid.UUID(post_id, version=4)
        post = Post.objects.get(id = post_id)
    except (ValueError, Post.DoesNotExist):
        return redirect(error, message='No Post Found!')

    users = post.likes.all()
    context={
        'title':'Likes | ClickTime',
        'users':users
    }
    return render(request, 'home/users_liked.html',context=context)


@login_required
def fol(request):
    user_profile = request.user.profile
    res={
        'followers':user_profile.followers.count(),
        'following':user_profile.following.count()
    }
    return HttpResponse(json.dumps(res))


@login_required
def comment(request):
    post_id = request.GET.get('post_id')
    try:
        val = uuid.UUID(post_id, version=4)
        post = Post.objects.get(pk = post_id)
    except (ValueError, Post.DoesNotExist):
        return redirect(error, message='No Post Found!') 
    user = request.user
    if not user == post.user.user:
        notify.send(sender = user , recipient = post.user.user, verb='commented on your post', action_object=post)
        res = {
            'data':'succsess'
        }
        return HttpResponse(json.dumps(res))
    else:
        res = {
            'data':'succsess'
        }
        return HttpResponse(json.dumps(res))
            

