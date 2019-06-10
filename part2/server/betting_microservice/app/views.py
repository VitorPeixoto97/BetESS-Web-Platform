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

def betView(request, result, amount, odd, profit):
    existe = False
    for bet in models.Bet.objects.all():
        if bet.id == id:
            existe = True
    if not existe:
        models.Bet.objects.create(result=result, amount=amount, odd=odd, profit=profit)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='bet already exists')

@csrf_exempt 
def addBetView(request):
    if request.method=='POST':
        received = json.loads(request.body.decode('utf-8'))

        this.selected.amount = 1
        this.selected.bet = "V", "E", "D"
        this.selected.odd = 2.34
        this.selected.id = 6
        this.selected.equipa = "Benfica"
        this.selected.user = vitor-peixoto@outlook.pt

        tp = get_object_or_404(models.TipoEvento, id=received['tipo'])
        jg = get_object_or_404(models.Jogo, id=received['jogo'])
        #inst = received['instante']
        inst = '00:05:12'
        eq = get_object_or_404(models.Formacao, id=received['equipa'])
        at1 = get_object_or_404(models.Atleta, id=received['atleta1'])
        at2 = received['atleta2']
        zC = received['zonaC']
        zB = received['zonaB']
        novo = received['novoinst']

        if novo is not None:
            models.Evento.objects.create(tipo=tp, jogo=jg, instante=inst, novoinstante=novo)
        elif eq is not None and at1 is not None and at2 is not None:
            models.Evento.objects.create(tipo=tp, jogo=jg, equipa=eq, atleta1=at1, atleta2=at2, instante=inst)
            models.Convocado.objects.filter(atleta=at1, jogo=jg).update(emCampo=False)
            models.Convocado.objects.filter(atleta=at2, jogo=jg).update(emCampo=True)
        elif eq is not None and at1 is not None and zC is not None and zB is not None:
            models.Evento.objects.create(tipo=tp, jogo=jg, equipa=eq, atleta1=at1, zonaCampo=zC, zonaBaliza=zB, instante=inst)
        elif eq is not None and at1 is not None and zC is not None:
            models.Evento.objects.create(tipo=tp, jogo=jg, equipa=eq, atleta1=at1, zonaCampo=zC, instante=inst)
        elif eq is not None:
            models.Evento.objects.create(tipo=tp, jogo=jg, equipa=eq, instante=inst)

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