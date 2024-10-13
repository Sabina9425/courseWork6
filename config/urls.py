from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('mailing_app.urls', 'mailing_app'), namespace='mailing_app')),
]
