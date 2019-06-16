from django.urls import include, path
from . import views
from django.views.generic import TemplateView, RedirectView

app_name = 'Betting'
urlpatterns = [
    path('bets/', views.gBetsView, name='gbets'),
    path('bet/<int:id>/', views.gBetView, name='Get Bet'),
    path('add_bet/', views.addBetView, name='Add Bet'),
    path('del_bet/<int:id>/', views.delBetView, name='Delete Bet'),
    path('bets/<str:user>/', views.getUserBetsView, name='User Bets'),
    path('notifs/', views.gNotificationsView, name='notifs'),
    path('notifs/<int:user>/', views.gNotificationUserView, name='notif_user'),
    path('del_notif/<int:id>/', views.dNotificationView, name='dnotif'),
]