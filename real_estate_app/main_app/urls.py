from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict', views.predict, name='predict'),
    path('signup/', views.SignupPage.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('historique/', views.historique, name='historique'),

]
