from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('admine', views.admine, name="admine"),
    path('add',views.ADD, name='add'),
    path('edit', views.Edit, name='edit'),
    path('update/<str:id>', views.Update, name='update'),
    path('delete/<str:id>', views.Delete, name='delete'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_logout',views.admin_logout, name='admin_logout'),
    path('search', views.search, name="search")
]
