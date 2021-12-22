from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up),
    path('sign-in', views.sign_in),
    path('roles/', views.get_roles),
    path('roles/add', views.add_role),
    path('roles/<int:id>/', views.get_roles),
    path('users/', views.get_users),
    path('users/<int:id>/', views.get_users),
]