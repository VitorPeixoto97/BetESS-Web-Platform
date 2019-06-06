from django.urls import include, path, register_converter
from . import converters, views
from django.views.generic import TemplateView, RedirectView

register_converter(converters.BoolConverter, 'bool')
register_converter(converters.DateConverter, 'date')
register_converter(converters.TimeConverter, 'time')

app_name = 'BettingApp'
urlpatterns = [

    path('bets/', TemplateView.as_view(template_name='bets.html')),
    path('notifs/', TemplateView.as_view(template_name='notifs.html')),

    path('bet/<str:result>/<int:amount>/<float:odd>/<float:profit>/', views.betView, name='bet'),
    #path('change_bet/<int:id>/<str:result>/<int:amount>/<float:odd>/<float:profit>/', views.cBetView, name='cbet'),
    path('get_bets/', views.gBetsView, name='gbets'),
    path('get_bets/<str:id>/', views.gBetView, name='gbet'),

    path('notif/', views.notifView, name='notif'),
    path('del_notif/<int:id>/', views.dNotificationView, name='dnotif'),
    path('get_notif/<int:id>/', views.gNotificationsView, name='gnotif'),
]