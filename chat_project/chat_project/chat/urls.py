from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('member_list/', views.member_list, name='member_list'),
    path('chat/<str:username>/', views.private_chat, name='private_chat'),
    path('chat/history/<str:username>/', views.chat_history, name='chat_history'),
]
