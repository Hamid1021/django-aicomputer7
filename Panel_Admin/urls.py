from django.urls import path

from Panel_Admin.views import *

app_name = "Panel_Admin"

urlpatterns = [
    path("tickets/", tickets, name="tickets"),
    path("tickets/load_more_ticket", load_more_ticket, name="load_more_ticket"),
    path("ticket/<int:pk>/", ticket, name="ticket"),
]
