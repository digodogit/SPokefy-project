from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('spokefyapp.urls')),
    path('users/', include('spokefypkmn.urls')),
]
