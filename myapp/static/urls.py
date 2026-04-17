from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('items/', views.items, name='items'),
    path('items/add/', views.add_item, name='add_item'),
    path('analytics/', views.analytics, name='analytics'),
]
