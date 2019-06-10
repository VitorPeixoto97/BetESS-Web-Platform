# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from . import models
import pika
import json

# Create your views here.

class IndexView(generic.ListView):
	template_name = 'index.html'
	context_object_name = 'user_list'
	#def get_queryset(self):
		#return models.Clube.objects.order_by('-nome')[:5]

class PostsView(ListAPIView):
    authentication_class = (JSONWebTokenAuthentication,) # Don't forget to add a 'comma' after first element to make it a tuple
    permission_classes = (IsAuthenticated,)

def index(request):
    context = 'Hello World'
    return render(request, 'server/index.html', context)

def infoBetView(request, id):
  bet = models.Bet.objects.get(id=id)

  return JsonResponse(model_to_dict(bet))

def gBetView(request, id):
    bet = get_object_or_404(models.Bet, id=id)
    return JsonResponse(model_to_dict(bet))

def gBetsView(request):
    bets = models.Bet.objects.all()
    aux = []
    for bet in bets:
        aux.append(model_to_dict(bet))
    return JsonResponse(aux, safe=False)

@csrf_exempt 
def addBetView(request):
    if request.method=='POST':
        received = json.loads(request.body.decode('utf-8'))

        if(received['bet']=="V"):
            res=0
        elif(received['bet']=="E"):
            res=1
        elif(received['bet']=="D"):
            res=2

        prof=received['odd']*received['amount']

        models.Bet.objects.create(result=res, amount=received['amount'], odd=received['odd'], profit=prof, event=received['id'], user=received['user'])

        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='bad form')

@login_required
@permission_required('change_bet', raise_exception=True)
def cBetView(request, result, amount, odd, profit):
    models.Bet.objects.filter(id=id).update(result=result, amount=amount, odd=odd, profit=profit)
    return HttpResponse('ok')


def dBetView(request, id):
    bet = get_object_or_404(models.Bet, id=id)
    bet.delete()
    return HttpResponse('ok')

def gNotificationView(request, id):
    notif = get_object_or_404(models.Notification, id=id)
    return JsonResponse(model_to_dict(notif))

def gNotificationUserView(request, user):
    notifs = models.Notification.objects.filter(user=user)
    aux = []
    for notif in notifs:
        aux.append(model_to_dict(notif))
    return JsonResponse(aux, safe=False)

def gNotificationsView(request):
    notifs = models.Notification.objects.all()
    aux = []
    for notif in notifs:
        aux.append(model_to_dict(notif))
    return JsonResponse(aux, safe=False)

#def notifView(request, message):
def notifView(user, message):
    existe = False
    for notif in models.Notification.objects.all():
        if notif.id == id:
            existe = True
    if not existe:
        models.Notification.objects.create(user=user, message=message)
        #return HttpResponse('ok')
    #else:
        #return HttpResponseBadRequest(content='notif already exists')

def dNotificationView(request, id):
    notif = get_object_or_404(models.Notification, id=id)
    notif.delete()
    return HttpResponse('ok')

def word(result):
    word = 'undefined'
    if result == 0:
        word = 'ganhou'
    if result == 1:
        word = 'empatou'
    if result == 2:
        word = 'perdeu'

def endBets(event, result, equipaC, equipaV):
        models.Bet.objects.filter(event=event).update(result=result)

        users = []
        for bet in models.Bet.objects.filter(event=event):
            if bet.result == result:
                message = equipaC + ' ' + word(result) + ' contra ' + equipaV + '! Ganhou ' + bet.profit + ' coins da sua aposta!'
                users.append(bet.user + '-' + bet.profit)
            else: 
                message = equipaC + ' ' + word(result) + ' contra ' + equipaV + '! Perdeu a sua aposta...'

            models.Notification.objects.create(message=message, bet=bet.id, user=bet.user)

        return users