from django.urls import include, path
from . import views
from django.views.generic import TemplateView, RedirectView

app_name = 'User'
urlpatterns = [
	path('users/', views.gUsersView, name='users'),
    path('info_user/<str:email>/', views.infoUserView, name='info'),
    #path('admin/<str:email>/<str:nome>/<str:password>/', views.adminView, name='admin'),
    #path('user/<string:email>/<str:username>/<str:name>/<str:password>/', views.UserView, name='user'),
    #path('change_user/<int:id>/<string:email>/<str:username>/<str:name>/<str:password>/<float:coins>/', views.cUserView, name='cuser'),
    #path('delete_user/<int:id>/', views.dUserView, name='duser'),
]
