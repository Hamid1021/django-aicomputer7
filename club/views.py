from django.shortcuts import render, get_object_or_404
from club.models import Club
from blog.models import Blog
from event.models import Event
from django.core.paginator import Paginator

def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk, is_active=True)

    posts = Blog.objects.filter(club=club).order_by('-date_create')
    events = Event.objects.filter(club=club).order_by('-date_create')

    post_paginator = Paginator(posts, 8)
    event_paginator = Paginator(events, 8)

    post_page = request.GET.get('post_page')
    event_page = request.GET.get('event_page')

    context = {
        'club': club,
        'club_name': club.club_name,
        'post_page_obj': post_paginator.get_page(post_page),
        'event_page_obj': event_paginator.get_page(event_page),
    }
    return render(request, "club/club_detail.html", context)
