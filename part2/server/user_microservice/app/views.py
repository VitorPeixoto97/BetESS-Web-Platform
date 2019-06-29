from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from . import models
from django.contrib.auth.decorators import login_required, permission_required
import json
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model

class IndexView(generic.ListView):
	template_name = 'index.html'
	context_object_name = 'user_list'
	#def get_queryset(self):
		#return models.Clube.objects.order_by('-nome')[:5]

class PostsView(ListAPIView):
    authentication_class = (JSONWebTokenAuthentication,) # Don't forget to add a 'comma' after first element to make it a tuple
    permission_classes = (IsAuthenticated,)

@csrf_exempt
def registerView(request):
    if request.method=='POST':
        received = json.loads(request.body.decode('utf-8'))

        email = received['username']
        password = received['password']
        name = received['name']
        coins = int(received['coins']) + 5
        if(received['premium']==False):
            premium=0
        else:
            premium=1

        users = models.User.objects.filter(email=email)
        admins = models.Admin.objects.filter(email=email)

        if(users.count()>0 or admins.count()>0):
            return HttpResponseBadRequest(content='Endereço email introduzido já se encontra registado.')
        elif(coins<10):
            return HttpResponseBadRequest(content='Tem de depositar no mínimo 5 coins para fazer o registo.')
        else:
            id = 1
            ids = models.User.objects.all().values_list('id', flat=True)
            if len(ids) != 0:
                id = max(ids) + 1                
            user = get_user_model().objects.create_user(email, email, password)
            models.User.objects.create(id=id, email=email, name=name, type=premium, coins=coins)
            return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='bad form')


def index(request):
    context = 'Hello World'
    return render(request, 'server/index.html', context)

def gUsersView(request):
    users = models.User.objects.all()
    aux = []
    for user in users:
        aux.append(model_to_dict(user))
    return JsonResponse(aux, safe=False)

def infoUserView(request, email):
  user = get_object_or_404(models.User, email=email)
  return JsonResponse(model_to_dict(user))

def userView(request, username, email, password, name, coins):
    existe = False
    for user in models.User.objects.all():
        if user.email == email:
            existe = True
    for admin in models.Admin.objects.all():
        if admin.email == email:
            existe = True
    if not existe:
        id = 1
        ids = models.Team.objects.all().values_list('id', flat=True)
        if len(ids) != 0:
            id = max(ids) + 1
        models.User.objects.create(id=id, username=username, email=email, password=password, name=name, coins=coins+10)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='user already exists')

def cUserView(request, id, email, username, password, name, coins):
    models.User.objects.filter(id=id).update(email, username, password, name, coins)
    return HttpResponse('ok')

def removeCoinsView(request, userid, amount):
    usr = get_object_or_404(models.User, id=userid)

    if(usr.coins<amount):
        return HttpResponseBadRequest('Não tem saldo suficiente!')
    else: 
        models.User.objects.filter(id=userid).update(coins=usr.coins-amount)
    return HttpResponse('ok')

def addCoinsView(request, userid, amount):
    usr = get_object_or_404(models.User, id=userid)
    models.User.objects.filter(id=userid).update(coins=usr.coins+amount)
    return HttpResponse('ok')


def dUserView(request, id):
    user = get_object_or_404(models.User, id=id)
    user.delete()
    return HttpResponse('ok')

def updateCoins(id, coins):
    user = models.User.objects.get(id=id)
    models.User.objects.filter(id=id).update(coins=user.coins + coins)
    return HttpResponse('ok')

def infoAdminView(request, email):
  user = models.Admin.objects.get(email=email)
  return JsonResponse(model_to_dict(user))