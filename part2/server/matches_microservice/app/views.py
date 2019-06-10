from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.forms.models import model_to_dict
from . import models

def cTeamView(request, id, name, simbolo):
    models.Team.objects.filter(id=id).update(name=name, simbolo=simbolo)
    return HttpResponse('ok')

def gTeamView(request, id):
    team = get_object_or_404(models.Team, id=id)
    return JsonResponse(model_to_dict(team))

def gTeamsView(request):
    teams = models.Team.objects.all()
    aux = []
    for team in teams:
        aux.append(model_to_dict(team))
    return JsonResponse(aux, safe=False)

def cCompetitionView(request, id, name, country):
    models.Competition.objects.filter(id=id).update(name=name, country=country)
    return HttpResponse('ok')

def gCompetitionView(request, id):
    competition = get_object_or_404(models.Competition, id=id)
    return JsonResponse(model_to_dict(competition))

def gCompetitionsView(request):
    competitions = models.Competition.objects.all()
    aux = []
    for competition in competitions:
        aux.append(model_to_dict(competition))
    return JsonResponse(aux)

def cEventView(request, id, name, country):
    models.Event.objects.filter(id=id).update(name=name, country=country)
    return HttpResponse('ok')

def gEventView(request, id):
    event = get_object_or_404(models.Event, id=id)
    return JsonResponse(model_to_dict(event))

def gEventsView(request):
    events = models.Event.objects.all()
    aux = []
    for event in events:
        new_event = {}
        new_event['type'] = event.type
        new_event['competition'] = event.competition.name
        new_event['equipaC'] = event.equipaC.name
        new_event['equipaF'] = event.equipaF.name
        new_event['oddV'] = event.oddV
        new_event['oddE'] = event.oddE
        new_event['oddD'] = event.oddD
        new_event['status'] = event.status
        new_event['result'] = event.result
        aux.append(new_event)
    return JsonResponse(aux, safe=False)
