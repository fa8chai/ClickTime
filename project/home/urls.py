from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.main, name="main"),
    path('post/', views.create_post, name="create_post"),
    path('<username>/p/<post_id>/', views.view_post, name="view_post"),
    path('search/',views.search, name='search' ),
    path('u/<username>/',views.get_user, name='get_user'),
    path('search/people/<key>',views.users_search,name="users_search"),
    path('post/delete/<post_id>',views.delete_post,name='delete_post'),
    path('error/<message>/',views.error,name='error'),
    path('ajax/2/load_comments/',views.load_comments,name='load_comments'),
    path('ajax/3/follow/', views.follow, name='follow'),
    path('ajax/4/unfollow/', views.unfollow, name='unfollow'),
    path('ajax/5/like/', views.like, name='like'),
    path('ajax/6/ch_like/', views.ch_like, name='ch_like'),
    path('<username>/p/<post_id>/likes/',views.users_liked, name='users_liked'),
    path('ajax/7/fol/',views.fol ,name='fol'),
    path('ajax/8/block/', views.block, name='block'),
    path('ajax/9/unblock/', views.unblock, name='unblock'),
    path('ajax/10/comment/',views.comment,name='comment'),


]