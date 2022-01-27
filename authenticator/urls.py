from django.urls import path
from . import views

urlpatterns = [
    path('roles', views.roles),
    path('roles/<int:id>', views.role_detail),
    path('users', views.users),
    path('users/', views.users),
    path('authorize', views.authorize),
    path('users/logout', views.logout),
    path('users/<str:email>', views.user_detail),
    path('token', views.refresh_token)
]