from django.urls import include, path
from . import views
from django.views.generic import TemplateView, RedirectView

app_name = 'User'
urlpatterns = [
	path('users/', views.gUsersView, name='Users'),
    path('info/<str:email>/', views.infoUserView, name='User Info'),
    path('remove_coins/<int:userid>/<int:amount>/', views.removeCoinsView, name="Remove Coins"),
    path('add_coins/<int:userid>/<int:amount>/', views.addCoinsView, name="Add Coins"),
    path('admin_info/<str:email>/', views.infoAdminView, name='Admin Info'),
    path('register/', views.registerView, name='Register'),
]
