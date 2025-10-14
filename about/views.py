from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import AboutPage, TeamMember, FAQ


def about_view(request):
    about_main = AboutPage.objects.filter(
        is_active=True, is_deleted=False).first()
    team = TeamMember.objects.filter(is_active=True, is_deleted=False)
    faqs = FAQ.objects.filter(is_active=True, is_deleted=False)
    history = AboutPage.objects.filter(
        page_type='history', is_active=True, is_deleted=False).first()
    mission = AboutPage.objects.filter(
        page_type='mission', is_active=True, is_deleted=False).first()

    context = {
        'about_main': about_main,
        'team': team,
        'faqs': faqs,
        'history': history,
        'mission': mission,
    }
    return render(request, 'about.html', context)
