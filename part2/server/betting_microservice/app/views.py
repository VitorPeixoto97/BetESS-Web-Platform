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
import json
from . import messaging
from decimal import Decimal

# Create your views here.

class IndexView(generic.ListView):
	template_name = 'index.html'
	context_object_name = 'user_list'

class PostsView(ListAPIView):
    authentication_class = (JSONWebTokenAuthentication,) 
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

def getUserBetsView(request, user):
    aux = getUserBets(user)

    return JsonResponse(aux, safe=False)

def getUserBets(userid):
    bets = models.Bet.objects.filter(user=userid)
    aux=[]
    for bet in bets:
        aux.append(model_to_dict(bet))
    return aux

def delBetView(request, id):
    bet = get_object_or_404(models.Bet, id=id)
    user = bet.user
    amount = bet.amount

    bet.delete()

    messaging.send_message('bet_cancel;'+ str(user) + ';' + str(amount))

    return HttpResponse('ok')

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

        usr = received['user']
        bets = getUserBets(usr['id'])

        odd = float(received['odd']) 
        amount = int(received['amount'])
        prof = odd*amount

        jaapostou=False
        for bet in bets:
            if(bet['event']==received['id']):
                jaapostou=True
        if(jaapostou):
            return HttpResponseBadRequest('Já apostou nesse evento!')
        else:
            id = max(models.Bet.objects.all().values_list('id', flat=True)) + 1
            models.Bet.objects.create(id=id, result=res, amount=amount, odd=odd, profit=prof, event=received['id'], user=usr['id'])

            messaging.send_message('bet_made;' + str(usr['id']) + ';' + str(amount))

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

    if(bet.result == -1):
        messaging.send_message('bet_cancel;' + bet.user + ';' + bet.amount)

    return HttpResponse('ok')

def gNotificationView(request, id):
    notif = get_object_or_404(models.Notification, id=id)
    return JsonResponse(model_to_dict(notif))

def gNotificationUserView(request, user):
    notifs = models.Notification.objects.filter(user=user)
    aux = []
    if(notifs.count()==0):
        return JsonResponse(aux, safe=False)
    for notif in notifs:
        aux.append(model_to_dict(notif))
    return JsonResponse(aux, safe=False)

def gNotificationsView(request):
    notifs = models.Notification.objects.all()
    aux = []
    for notif in notifs:
        aux.append(model_to_dict(notif))
    return JsonResponse(aux, safe=False)

def notifView(user, message):
    existe = False
    for notif in models.Notification.objects.all():
        if notif.id == id:
            existe = True
    if not existe:
        id = max(models.Notification.objects.all().values_list('id', flat=True)) + 1
        models.Notification.objects.create(id=id, user=user, message=message)

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
    return word

def endBets(event, result, equipaC, equipaF):
        models.Bet.objects.filter(event=event)

        users = []
        for bet in models.Bet.objects.filter(event=event):
            if bet.result == result:
                message = equipaC + ' ' + word(result) + ' contra ' + equipaF + '! Ganhou ' + str(bet.profit) + '€!'
                users.append(str(bet.user) + '-' + str(bet.profit))
            else: 
                print('loser: ' + str(bet.id))
                message = equipaC + ' ' + word(result) + ' contra ' + equipaF + '! Perdeu a sua aposta...'
                bet.profit=Decimal('0.00')
                bet.save()

            id = max(models.Notification.objects.all().values_list('id', flat=True)) + 1
            models.Notification.objects.create(id=id, message=message, bet=bet, user=bet.user)


        return users
