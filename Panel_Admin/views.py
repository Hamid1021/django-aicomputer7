from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from Panel_Admin.models import Panel_Admin_Settings
from account.models import Ticket
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader


def panel_admin(request):
    return render(request, "test.html", {})


def panel_admin1(request):
    return render(request, "test.html", {})


def panel_admin2(request):
    return render(request, "test.html", {})


def tickets(request):
    global results_per_page
    results_per_page = 10
    all_tickets = Ticket.objects.all()[:results_per_page]
    context = {
        "object_list": all_tickets,
    }
    return render(request, "Tickets.html", context)


def load_more_ticket(request):
    page = request.POST.get('page')
    all_tickets = Ticket.objects.all()
    paginator = Paginator(all_tickets, results_per_page)
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(2)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    posts_html = loader.render_to_string(
        'one_ticket.html',
        {'object_list': tickets}
    )
    output_data = {
        'posts_html': posts_html,
        'has_next': tickets.has_next(),
    }
    return JsonResponse(output_data)


def ticket(request, pk):
    return render(request, "test.html", {})


##############################     Partial     #################################
def header_ref_admin_panel(request):
    context = {

    }
    return render(request, "Base/header_ref.html", context)


def footer_ref_admin_panel(request):
    n_mode = Panel_Admin_Settings.objects.all().first().night_mode
    if n_mode:
        n_mode_status = 1
    else:
        n_mode_status = 0
    context = {
        "n_mode_status": n_mode_status,
    }
    return render(request, "Base/footer_ref.html", context)


def footer_admin_panel(request):
    context = {

    }
    return render(request, "Base/footer.html", context)


def left_aside_admin_panel(request):
    f_color = get_Sidenav_color_settings()
    logo_colre = ""
    if f_color == "bg-gradient-dark":
        t_color = "text-white"
    else:
        t_color = "text-dark"
        logo_colre = "-dark"
    context = {
        "fg_color": f_color,
        "t_color": t_color,
        "logo_colre": logo_colre,
        "classes": f"{get_color_settings()} {t_color} active",
    }
    return render(request, "Base/left_aside.html", context)


def settings_admin_panel(request, ):
    fix_status = Panel_Admin_Settings.objects.all().first().fixed_navbar
    n_mode = Panel_Admin_Settings.objects.all().first().night_mode
    if n_mode:
        n_mode_status = 1
    else:
        n_mode_status = 0
    if fix_status:
        checked = 'checked'
    else:
        checked = ""
    context = {
        "nav_fix_status": checked,
        "n_mode_status": n_mode_status,
    }
    return render(request, "Base/settings.html", context)


def top_path_and_navbar_admin_panel(request):
    status = Panel_Admin_Settings.objects.all().first().fixed_navbar
    tree_last_message = Ticket.objects.get_last_three_unread_message()
    f_color = get_Sidenav_color_settings()
    if f_color == "bg-gradient-dark":
        t_color = "text-white"
    else:
        t_color = "text-dark"
    if status:
        nav_status = True
    else:
        nav_status = False
    context = {
        "nav_status": nav_status,
        "tree_last_message": tree_last_message,
        "classes": f"{get_color_settings()} {t_color} active",
        "t_color": f"{t_color}",
    }
    return render(request, "Base/top_path_and_nav.html", context)


##############################     Partial     #################################

def daily_information_admin_panel(request):
    context = {

    }
    return render(request, "Base/daily_information.html", context)


def visit_admin_panel(request):
    context = {

    }
    return render(request, "Base/visit.html", context)


def set_color_settings(request):
    item = Panel_Admin_Settings.objects.all().first()
    color = request.GET.get("color")
    item.bg_color_Sidebar = color
    item.save()
    return HttpResponse("Done!")


def get_color_settings():
    item = Panel_Admin_Settings.objects.all().first()
    temp = item.bg_color_Sidebar
    li = {
        "pr": "primary",
        "da": "dark",
        "in": "info",
        "su": "success",
        "wa": "warning",
        "dn": "danger",
    }
    return f"bg-gradient-{li[temp]}"


def set_Sidenav_color_settings(request):
    item = Panel_Admin_Settings.objects.all().first()
    color = request.GET.get("color")
    item.Sidenav_color = color
    item.save()
    return HttpResponse("Done!")


def get_Sidenav_color_settings():
    item = Panel_Admin_Settings.objects.all().first()
    temp = item.Sidenav_color
    li = {
        "wh": "bg-white", "tr": "bg-transparent", "da": "bg-gradient-dark",
    }
    return f"{li[temp]}"


def set_fixed_navbar_settings(request):
    item = Panel_Admin_Settings.objects.all().first()
    statue = request.GET.get("statue")
    item.fixed_navbar = statue
    item.save()
    return HttpResponse("Done!")


def set_night_mode_settings(request):
    item = Panel_Admin_Settings.objects.all().first()
    statue = request.GET.get("statue")
    item.night_mode = statue
    item.save()
    return HttpResponse("Done!")
