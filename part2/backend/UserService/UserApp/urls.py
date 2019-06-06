from django.urls import include, path, register_converter
from . import converters, views
from django.views.generic import TemplateView, RedirectView

register_converter(converters.BoolConverter, 'bool')
register_converter(converters.DateConverter, 'date')
register_converter(converters.TimeConverter, 'time')
register_converter(converters.FloatConverter, 'float')

app_name = 'UserApp'
urlpatterns = [

    path('info_user/<str:email>/', views.infoUserView, name='info'),

    
    # path('admin/<str:email>/<str:nome>/<str:password>/', views.adminView, name='admin'),

    path('user/<str:email>/<str:username>/<str:name>/<str:password>/', views.userView, name='user'),
    path('change_user/<int:id>/<str:email>/<str:username>/<str:name>/<str:password>/<float:coins>/', views.cUserView, name='cuser'),
    path('delete_user/<int:id>/', views.dUserView, name='duser')
]
