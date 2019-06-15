"""api_layer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from reverse_proxy.views import Gets, Login, Bet, Event, EventEnd, Register, Team


urlpatterns = [
	#POSTS
    url(r'^(?P<path>.*)login/$', Login.as_view()),
    url(r'^(?P<path>.*)register/$', Register.as_view()),
    url(r'^(?P<path>.*)bet/$', Bet.as_view()),
    url(r'^(?P<path>.*)event/$', Event.as_view()),
    url(r'^(?P<path>.*)end_event/$', EventEnd.as_view()),
    url(r'^(?P<path>.*)team/$', Team.as_view()),

    #GETS
    url(r'^(?P<path>.*)$', Gets.as_view()),
]