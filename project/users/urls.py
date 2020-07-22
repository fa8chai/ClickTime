from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path('signup/', views.signup, name='signup'),
    path('logout/',views.signout,name='signout'),
    path('login/',views.signin,name='signin'),
    path('user/resend_email/', views.resend_email, name='resend_email'),
    path('confirm_email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('send/activation_email/',views.send_activation_email, name='send_activation_email'),
    path('reactivate/<uidb64>/<token>/', views.reactivate_account, name='reactivate_account'),
    path('forgot_password/',views.forget_password, name='forget_password'),
    path('reset/password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('reset/password/confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    path('settings/email/change/', views.change_email, name='change_email'),
    path('change/email/<uidb64>/<token>/', views.change_email_activate, name='change_email_activate'),

    
]