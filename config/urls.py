from django.contrib import admin
from django.urls import path, include

#connects the website pages together
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
