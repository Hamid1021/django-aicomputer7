from django.urls import path

from Panel_Admin.views import *

app_name = "settings_Panel_Admin"

urlpatterns = [
    path('home1/', panel_admin, name="home"),
    path('home2/', panel_admin1, name="home1"),
    path('home3/', panel_admin2, name="home2"),
    path('set_color_settings', set_color_settings, name="set_color_settings"),
    path('set_Sidenav_color_settings', set_Sidenav_color_settings, name="set_Sidenav_color_settings"),
    path('set_fixed_navbar_settings', set_fixed_navbar_settings, name="set_fixed_navbar_settings"),
    path('set_night_mode_settings', set_night_mode_settings, name="set_night_mode_settings"),
]
