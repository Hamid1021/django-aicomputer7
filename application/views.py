# views.py
from django.shortcuts import render
from blog.models import Blog
from club.models import Club
from event.models import Event
from django.db import models


def home(request):
    newest_posts = Blog.objects.order_by('-date_create')[:8]
    newest_events = Event.objects.order_by('-date_create')[:8]
    clubs = Club.objects.filter(is_active=True).annotate(
        user_count=models.Count('user')
    ).order_by('-user_count')

    context = {
        "newest_events": newest_events,
        "newest_posts": newest_posts,
        "clubs": clubs
    }
    return render(request, "index.html", context)
