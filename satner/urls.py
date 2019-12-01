"""satner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from .views import AboutPageView, ServicesPageView, ContactView, HomePageView, acme_challenge
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('projects/', include('projects.urls')),
    path('blog/', include('blog.urls')),
    path('newsletter/', include('marketing.urls')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('.well-known/acme-challenge/.', acme_challenge, name='acme_challenge'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)