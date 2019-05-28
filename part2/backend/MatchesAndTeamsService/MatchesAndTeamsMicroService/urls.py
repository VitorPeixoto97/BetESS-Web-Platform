from django.urls import include, path, register_converter
from . import converters, views
from django.views.generic import TemplateView, RedirectView

register_converter(converters.BoolConverter, 'bool')
register_converter(converters.DateConverter, 'date')
register_converter(converters.TimeConverter, 'time')

app_name = 'MatchesAndTeamsMicroservice'
urlpatterns = [

    path('teams/', TemplateView.as_view(template_name='teams.html')),
    path('events/', TemplateView.as_view(template_name='events.html')),

    path('team/<str:nome>/<str:simbolo>/', views.teamView, name='team'),
    path('change_team/<int:id>/<str:simbolo>/', views.cTeamView, name='cteam'),
    path('get_teams/', views.gTeamsView, name='gteams'),
    path('get_teams/<str:id>/', views.gClubeView, name='gteam'),

    path('event/', views.eventoView, name='event'),
    path('change_event/', views.cEventView, name='cevent'),
    path('del_event/<int:id>/', views.dEventView, name='devent'),
    path('get_events/', views.gEventsView, name='gevento'),
    path('get_event/<int:id>/', views.gEventView, name='gevent'),
]