from django.urls import path
from .views import contact_view, request_view

app_name = "contact"

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('request/', request_view, name='request'),
]
