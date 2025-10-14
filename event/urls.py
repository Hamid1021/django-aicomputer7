
from django.urls import path

from event.views import event_register, events_list, event_detail

app_name = "events"

urlpatterns = [
    # لیست تمام رویدادها
    path('', events_list, name='events'),
    path('category/<int:pk>/', events_list, name='events_by_category'),
    path('<slug:slug>/<int:pk>/', event_detail, name='event'),
    path("event/register/<int:pk>/", event_register, name="event_register"),
]
