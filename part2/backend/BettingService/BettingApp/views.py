from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from . import models, forms
from django.contrib.auth.decorators import login_required, permission_required
import json
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


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

@login_required
@permission_required('view_bet', raise_exception=True)
def gBetView(request, id):
    bet = get_object_or_404(models.Bet, id=id)
    return JsonResponse(model_to_dict(bet))


@login_required
@permission_required('view_bet', raise_exception=True)
def gBetsView(request):
    bets = models.Bet.objects.all()
    aux = []
    for bet in bets:
        aux.append(model_to_dict(bet))
    return JsonResponse(aux)

@login_required
@permission_required('add_bet', raise_exception=True)
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

'''
@login_required
@permission_required('change_bet', raise_exception=True)
def cBetView(request, result, amount, odd, profit):
    models.Bet.objects.filter(id=id).update(result=result, amount=amount, odd=odd, profit=profit)
    return HttpResponse('ok')
'''

@login_required
@permission_required('delete_bet', raise_exception=True)
def dBetView(request, id):
    bet = get_object_or_404(models.Bet, id=id)
    bet.delete()
    return HttpResponse('ok')


@login_required
@permission_required('view_notif', raise_exception=True)
def gNotificationView(request, id):
    notif = get_object_or_404(models.Notification, id=id)
    return JsonResponse(model_to_dict(notif))


@login_required
@permission_required('view_notif', raise_exception=True)
def gNotificationsView(request):
    notifs = models.Notification.objects.all()
    aux = []
    for notif in notifs:
        aux.append(model_to_dict(notif))
    return JsonResponse(aux)


@login_required
@permission_required('add_notif', raise_exception=True)
def notifView(request, message):
    existe = False
    for notif in models.Notification.objects.all():
        if notif.id == id:
            existe = True
    if not existe:
        models.Notification.objects.create(message=message)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='notif already exists')

@login_required
@permission_required('delete_notif', raise_exception=True)
def dNotificationView(request, id):
    notif = get_object_or_404(models.Notification, id=id)
    notif.delete()
    return HttpResponse('ok')