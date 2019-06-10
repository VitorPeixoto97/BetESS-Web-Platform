# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from . import models
from django.contrib.auth.decorators import login_required, permission_required
import json
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import pika

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

def endBets(event, result):
        users = []
        for bet in models.Bet.objects.filter(event=event):
            users.append(bet.user + '-' + (bet.profit if bet.result == result else 0))

        models.Bet.objects.filter(event=event).update(result=result)

        return users