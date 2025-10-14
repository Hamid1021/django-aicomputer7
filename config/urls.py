"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('blogs/', include('blog.urls', namespace="blogs")),
    path('clubs/', include('club.urls', namespace="clubs")),
    path('events/', include('event.urls', namespace="events")),
    path('', include('contact.urls', namespace="contact")),
    path('', include('about.urls', namespace="about")),
    path('', include('account.urls', namespace="account")),
    path('', include('application.urls', namespace="application")),
    path('', include('map_xml.urls', namespace="sitemap")),
    # path('site/admin/', include('Panel_Admin.urls', namespace="Panel_Admin")),
    # path('site/admin/', include('Panel_Admin.setting_urls', namespace="settings_Panel_Admin")),
]

from django.conf import settings
from django.conf.urls.static import static


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
