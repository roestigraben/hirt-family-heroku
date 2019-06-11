from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('pages.urls')),
]

admin.site.site_header = "Stammbaum Admin"
admin.site.site_title = "Stammbaum Portal"
admin.site.index_title = "Hirt Family Stammbaum Administration"
