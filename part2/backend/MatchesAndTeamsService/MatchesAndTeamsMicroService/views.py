from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.forms.models import model_to_dict
from . import models, forms

@login_required
@permission_required('change_team', raise_exception=True)
def cTeamView(request, id, name, simbolo):
    models.Team.objects.filter(id=id).update(name=name, simbolo=simbolo)
    return HttpResponse('ok')


@login_required
@permission_required('view_team', raise_exception=True)
def gTeamView(request, id):
    team = get_object_or_404(models.Team, id=id)
    return JsonResponse(model_to_dict(team))


@login_required
@permission_required('view_team', raise_exception=True)
def gTeamsView(request):
    teams = models.Team.objects.all()
    aux = []
    for team in teams:
        aux.append(model_to_dict(team))
    return JsonResponse(aux)

@login_required
@permission_required('change_competition', raise_exception=True)
def cCompetitionView(request, id, name, country):
    models.Competition.objects.filter(id=id).update(name=name, country=country)
    return HttpResponse('ok')


@login_required
@permission_required('view_competition', raise_exception=True)
def gCompetitionView(request, id):
    competition = get_object_or_404(models.Competition, id=id)
    return JsonResponse(model_to_dict(competition))


@login_required
@permission_required('view_competition', raise_exception=True)
def gCompetitionsView(request):
    competitions = models.Competition.objects.all()
    aux = []
    for competition in competitions:
        aux.append(model_to_dict(competition))
    return JsonResponse(aux)

@login_required
@permission_required('change_event', raise_exception=True)
def cEventView(request, id, name, country):
    models.Event.objects.filter(id=id).update(name=name, country=country)
    return HttpResponse('ok')


@login_required
@permission_required('view_event', raise_exception=True)
def gEventView(request, id):
    event = get_object_or_404(models.Event, id=id)
    return JsonResponse(model_to_dict(event))


@login_required
@permission_required('view_event', raise_exception=True)
def gEventsView(request):
    events = models.Event.objects.all()
    aux = []
    for event in events:
        aux.append(model_to_dict(event))
    return JsonResponse(aux)

