from django.contrib import admin
from django.urls import path
from articles import views

urlpatterns = [
    path('',views.home,name = "home"),
    path('register',views.register,name="register"),
    path('logout',views.logoutUser,name="logout"),
    path('login',views.loginUser,name="login"),
    path('/<str:category>',views.catdisplay,name='catdisplay'),
    path('/<str:category>/<int:aid>',views.articledisplay,name='articledisplay'),
    path('submit',views.submit,name='submit')
]