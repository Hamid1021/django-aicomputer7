# club/urls.py
from django.urls import path
from club.views import club_detail

app_name = "clubs"

urlpatterns = [
    path('<int:pk>/', club_detail, name='club_detail'),
]
