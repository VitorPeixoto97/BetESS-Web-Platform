from django.urls import include, path
from . import views
from django.views.generic import TemplateView, RedirectView

app_name = 'Matches'
urlpatterns = [
    path('add_team/', views.addTeamView, name='Add Team'),
    path('teams/', views.gTeamsView, name='All Teams'),
    path('events/', views.getAllEventsView, name='All Events'),
    path('events/<int:usertype>/', views.getEventsView, name='Events'),
    path('active_events/', views.getActiveEventsView, name='Active Events'),
    path('event/<int:id>/', views.getEventView, name='Event'),
    path('add_event/', views.addEventView, name='addEvent'),
    path('end_event/', views.endEventView, name='endEvent'),
    path('competitions/', views.gCompetitionsView, name='All Competitions'),
    path('add_competition/', views.addCompetitionView, name='Add Competition'),
]