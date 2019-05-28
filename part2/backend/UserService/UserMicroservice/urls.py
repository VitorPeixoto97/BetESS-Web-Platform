from django.urls import include, path, register_converter
from . import converters, views
from django.views.generic import TemplateView, RedirectView

register_converter(converters.BoolConverter, 'bool')
register_converter(converters.DateConverter, 'date')
register_converter(converters.TimeConverter, 'time')

app_name = 'UserMicroservice'
urlpatterns = [

    path('info_user/<str:email>/', views.infoUserView, name='info'),

    
    # path('admin/<str:email>/<str:nome>/<str:password>/', views.adminView, name='admin'),

    path('tecnico/<int:clube>/<str:email>/<str:nome>/<str:password>/', views.tecnicoView, name='tecnico'),
    path('change_tecnico/<int:id>/<str:grelhaC>/<str:grelhaB>/', views.cTecnicoView, name='ctecnico'),

]
