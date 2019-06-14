from django.shortcuts import render
from revproxy.views import ProxyView

#POSTS
class Login(ProxyView):
	upstream = 'http://127.0.0.1:8002/auth/obtain/'

class Bet(ProxyView):
	upstream = 'http://127.0.0.1:8000/betting/add_bet/'

class Event(ProxyView):
	upstream = 'http://127.0.0.1:8001/matches/add_event/'

class EventEnd(ProxyView):
	upstream = 'http://127.0.0.1:8001/matches/end_event/'

class Register(ProxyView):
	upstream = 'http://127.0.0.1:8002/user/register/'

#GETS
class Gets(ProxyView):
	upstream = 'http://127.0.0.1:8000/'
	rewrite = (
		(r'^/betting(.*)$', r'http://127.0.0.1:8000/betting\1'),
		(r'^/matches(.*)$', r'http://127.0.0.1:8001/matches\1'),
		(r'^/user(.*)$', r'http://127.0.0.1:8002/user\1'),
		(r'^/login(.*)$', r'http://127.0.0.1:8002/auth/obtain/'),
		(r'^/refresh(.*)$', r'http://127.0.0.1:8002/auth/refresh\1'),
	)