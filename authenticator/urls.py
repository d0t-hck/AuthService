from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up),
    path('sign-in', views.sign_in),
    path('roles', views.get_roles),
    path('roles/add', views.add_role),
    path('roles/<int:id>/', views.get_role),
    #path('users/', views.get_users),
    path('users/', views.user_list),
    #path('users/<int:id>/', views.get_users),
    path('users/<int:id>/', views.user_detail),
    path('users/<str:email>/', views.get_users),
]