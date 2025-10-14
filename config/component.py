from club.models import Club
from django.shortcuts import render


def herader_ref(request):
    return render(request, "base/header_ref.html", context={})


def top_header(request):
    message = "به سایت انجمن علمی کامپیوتر خوش آمدید! آخرین اخبار و رویدادها را دنبال کنید."
    return render(request, "base/top_header.html", context={"message": message})


def header(request):
    return render(request, "base/header.html", {})


def clubs(request, is_footer=False):
    # گرفتن تمام کلاب‌های فعال و غیرحذف‌شده
    clubs = Club.objects.filter(
        is_active=True, is_deleted=False).order_by('date_create')

    context = {
        "is_footer": bool(is_footer),
        "clubs": clubs,
    }
    return render(request, "base/clubs.html", context)


def footer(request):
    return render(request, "base/footer.html", {})


def footer_ref(request):
    return render(request, "base/footer_ref.html", {})
