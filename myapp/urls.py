from django.urls import path
from . import views

urlpatterns = [

    path("analytics", views.analytics, name="analytics"),
   
    path("records/add/", views.record_create, name="record_add"),
    path("records/<int:pk>/", views.record_detail, name="record_detail"),
    path("records/<int:pk>/edit/", views.record_update, name="record_edit"),
    path("records/<int:pk>/delete/", views.record_delete, name="record_delete"),
    
    path("records/", views.record_list, name="records"),

    #root
    path("", views.home, name="home"),


]
