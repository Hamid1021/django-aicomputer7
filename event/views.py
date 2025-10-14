from account.models import USER
from club.models import Club  # چون در مدل EventUser نیاز هست
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Event, EventUser
from .models import Event
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event, EventsCategory
from club.models import Club


def events_list(request, pk=None):
    """لیست تمام رویدادها یا فیلتر شده بر اساس دسته‌بندی"""
    all_categories = EventsCategory.objects.filter(is_active=True)

    if pk:
        category = get_object_or_404(EventsCategory, pk=pk)
        events = Event.objects.filter(
            is_active=True, is_deleted=False, event_cat=category).order_by('-date_create')
    else:
        category = None
        events = Event.objects.filter(
            is_active=True, is_deleted=False).order_by('-date_create')
            
    club_id = request.GET.get('club')
    if club_id:
        club = get_object_or_404(Club, pk=club_id)
        events = events.filter(club=club)

    # Pagination
    paginator = Paginator(events, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category': category,
        'all_categories': all_categories,
    }
    return render(request, "events/events.html", context)


def event_detail(request, slug, pk):
    event = get_object_or_404(Event, slug=slug, pk=pk,
                              is_active=True, is_deleted=False)

    # بررسی شرکت کاربر در رویداد
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventUser.objects.filter(
            user=request.user, event=event).exists()

    # رویدادهای مشابه
    related_events = Event.objects.filter(
        event_cat__in=event.event_cat.all(),
        is_active=True,
        is_deleted=False
    ).exclude(id=event.id).distinct()[:4]

    context = {
        "event": event,
        "related_events": related_events,
        "is_registered": is_registered,
    }
    return render(request, "events/event_detail.html", context)


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    if EventUser.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({"status": "exists"})
    club = request.user.club
    EventUser.objects.create(user=request.user, club=club, event=event)
    return JsonResponse({"status": "ok"})
