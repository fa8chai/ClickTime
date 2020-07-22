from django.urls import path
from . import views
from django.conf import settings
from .views import extendUnread


urlpatterns = [
   
    path('', views.index, name="index"),
    path('ajax/1/validate_username/',views.validate_username,name='validate_username'),
    path('delete_account/', views.confirm_del, name='confirm_del'),
    path('account_deleted/', views.delete_user, name="delete_user"),
    path('deactivate_account/', views.confirm_deactivate, name='confirm_deactivate'),
    path('account_deactivated/', views.deactivate_user, name='deactivate_user'),
    path('settings/', views.account_settings, name='account_settings'),
    path('followers/', views.followers, name='followers'),
    path('following/', views.following, name='following'),
    path('blocked-users',views.blocked, name='blocked'),
    path('likes/', views.likes, name='likes'),
    
]