from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    
    path('musics', views.musics, name='musics'),
    path('musics/<int:music_id>', views.music_detail, name='music_detail'),
    path('musics/favorite/<int:music_id>', views.favorite_music, name='favorite_music'),

    path('register', views.register, name='register'),

    path('calendar', views.calendar, name='calendar'),
    
    # path('users', views.users, name='users'),
    
    path('profile', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('edit-password', views.edit_password, name='edit_password'),
    # path('success', views.success, name='success'),
    # path('cancel', views.cancel, name='cancel'),

]