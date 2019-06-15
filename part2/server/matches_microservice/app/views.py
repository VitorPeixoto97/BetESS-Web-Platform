from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import messaging
import json
from decimal import Decimal, ROUND_HALF_UP
import datetime

@csrf_exempt 
def addTeamView(request):
    if request.method=='POST':
        received = json.loads(request.body.decode('utf-8'))

        name = received['name']
        simbolo = received['simbolo']
        id = max(models.Team.objects.all().values_list('id', flat=True)) + 1

        models.Team.objects.create(id=id, name=name, simbolo=simbolo)

        return HttpResponse('ok')
    
    else:
        return HttpResponseBadRequest(content='bad form')

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
        new_team = {}
        new_team['id'] = team.id
        new_team['name'] = team.name
        new_team['simbolo'] = team.simbolo
        aux.append(new_team)
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
        new_competition = {}
        new_competition['id'] = competition.id
        new_competition['name'] = competition.name
        new_competition['country'] = competition.country
        aux.append(new_competition)
    return JsonResponse(aux, safe=False)
    #     new_competition['teams'] = []
    #     for team in competition.teams.all():
    #         new_team = {}
    #         new_team['id'] = team.id
    #         new_team['name'] = team.name
    #         new_team['simbolo'] = team.simbolo
    #         new_competition['teams'].append(new_team)
    #     aux.append(new_competition)
    # return JsonResponse(aux, safe=False)

@csrf_exempt
def addEventView(request):
    if request.method=='POST':
        received = json.loads(request.body.decode('utf-8'))

        print(received['premium'])

        if(received['premium']):
            tipo = 1
        else: 
            tipo = 0

        competition = models.Competition.objects.get(id=received['competicao']['id'])
        equipaC = models.Team.objects.get(id=received['equipaC']['id'])
        equipaF = models.Team.objects.get(id=received['equipaF']['id'])
        oddV = Decimal(received['oddV']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        oddE = Decimal(received['oddE']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        oddD = Decimal(received['oddD']).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        date = datetime.datetime.strptime(received['data'] + ' ' + received['hora'] , '%Y-%m-%d %H:%M')

        models.Event.objects.create(type=tipo, competition=competition, equipaC=equipaC, equipaF=equipaF,
        oddV=oddV, oddE=oddE, oddD=oddD, status=True, date=date.date(), time=date.time())

        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='bad form')

def cEventView(request, id, type, competition, equipaC, equipaF, oddV, oddE, oddD, status, result):
    models.Event.objects.filter(id=id).update(type=type, competition=competition, equipaC=equipaC, equipaF=equipaF, 
                                                oddV=oddV, oddE=oddE, oddD=oddD, status=status, result=result)

# def dEventView(request, id):
#     models.Event.objects.filter(id=id).delete

@csrf_exempt 
def endEventView(request):
    if request.method=='POST':
        received = json.loads(request.body.decode('utf-8'))

        id = received['id']
        result = received['result']
        equipaC = received['equipaC']
        equipaF = received['equipaF']

        models.Event.objects.filter(id=id).update(status=False, result=result)

        aux = result.split('-')

        if(aux[0] > aux[1]):
            res='0'
        elif(aux[0] == aux[1]):
            res='1'
        elif(aux[0] < aux[1]):
            res='2'

        message = 'bet_end;' + str(id) + ';' + res + ';' + equipaC + ';' + equipaF

        messaging.send_message(message)

        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='bad form')
            

def getEventView(request, id):
    event = get_object_or_404(models.Event, id=id)

    new_event = {}
    new_event['id'] = event.id
    new_event['type'] = event.type
    new_event['competition'] = event.competition.name
    new_event['equipaC'] = event.equipaC.name
    new_event['equipaCsimb'] = event.equipaC.simbolo
    new_event['equipaF'] = event.equipaF.name
    new_event['equipaFsimb'] = event.equipaF.simbolo
    new_event['oddV'] = event.oddV
    new_event['oddE'] = event.oddE
    new_event['oddD'] = event.oddD
    new_event['date'] = event.date.strftime('%d %b')
    new_event['time'] = event.time.strftime('%Hh%M')
    new_event['status'] = event.status
    new_event['result'] = event.result

    return JsonResponse(new_event, safe=False)

def getEventsView(request, usertype):

    #FILTRAR EVENTOS PREMIUM PARA USERS NAO PREMIUM
    if(usertype == 1):
        events = models.Event.objects.filter(status=True).order_by('date')
    else: events = models.Event.objects.filter(type=0, status=True).order_by('date')

    #FILTRAR EVENTOS ONDE O USER JA TENHA APOSTADO

    aux = []
    for event in events:
        new_event = {}
        new_event['id'] = event.id
        new_event['type'] = event.type
        new_event['competition'] = event.competition.name
        new_event['equipaC'] = event.equipaC.name
        new_event['equipaCsimb'] = event.equipaC.simbolo
        new_event['equipaF'] = event.equipaF.name
        new_event['equipaFsimb'] = event.equipaF.simbolo
        new_event['oddV'] = event.oddV
        new_event['oddE'] = event.oddE
        new_event['oddD'] = event.oddD
        new_event['date'] = event.date.strftime('%d %b')
        new_event['time'] = event.time.strftime('%Hh%M')
        new_event['status'] = event.status
        new_event['result'] = event.result
        aux.append(new_event)
    return JsonResponse(aux, safe=False)

def getAllEventsView(request):
    events = models.Event.objects.all().order_by('date')
    aux = []
    for event in events:
        new_event = {}
        new_event['id'] = event.id
        new_event['type'] = event.type
        new_event['competition'] = event.competition.name
        new_event['equipaC'] = event.equipaC.name
        new_event['equipaCsimb'] = event.equipaC.simbolo
        new_event['equipaF'] = event.equipaF.name
        new_event['equipaFsimb'] = event.equipaF.simbolo
        new_event['oddV'] = event.oddV
        new_event['oddE'] = event.oddE
        new_event['oddD'] = event.oddD
        new_event['date'] = event.date.strftime('%d %b')
        new_event['time'] = event.time.strftime('%Hh%M')
        new_event['status'] = event.status
        new_event['result'] = event.result
        aux.append(new_event)
    return JsonResponse(aux, safe=False)

def getActiveEventsView(request):
    events = models.Event.objects.filter(status=True).order_by('date')
    aux = []
    for event in events:
        new_event = {}
        new_event['id'] = event.id
        new_event['type'] = event.type
        new_event['competition'] = event.competition.name
        new_event['equipaC'] = event.equipaC.name
        new_event['equipaCsimb'] = event.equipaC.simbolo
        new_event['equipaF'] = event.equipaF.name
        new_event['equipaFsimb'] = event.equipaF.simbolo
        new_event['oddV'] = event.oddV
        new_event['oddE'] = event.oddE
        new_event['oddD'] = event.oddD
        new_event['date'] = event.date.strftime('%d %b')
        new_event['time'] = event.time.strftime('%Hh%M')
        new_event['status'] = event.status
        new_event['result'] = event.result
        aux.append(new_event)
    return JsonResponse(aux, safe=False)

def gCompetitionTeamsView(request, id):
    teams = []
    teams = models.Competition.objects.get(id=id).teams.all()

    aux = []
    for team in teams:
        new_team = {}
        new_team['id'] = team.id
        new_team['name'] = team.name
        new_team['simbolo'] = team.simbolo
        aux.append(new_team)

    return JsonResponse(aux, safe=False)
        

def gNotCompetitionTeamsView(request, id):
    aux = []
    teams = models.Team.objects.all()
    for team in teams:
        try:
            team.competitions.get(id=id)
        except:
            new_team = {}
            new_team['id'] = team.id
            new_team['name'] = team.name
            new_team['simbolo'] = team.simbolo
            aux.append(new_team)

    return JsonResponse(aux, safe=False)

def CompetitionTeamView(request, idcomp, idteam):
    team = get_object_or_404(models.Team, id=idteam)

    try:
        competition = models.Competition.objects.get(id=idcomp)
    except:
        return HttpResponseBadRequest('Invalid Competition')

    competition.teams.add(team)

    return HttpResponse('ok')

def dCompetitionTeamView(request, idcomp, idteam):
    team = get_object_or_404(models.Team, id=idteam)

    
    competition = get_object_or_404(models.Competition, id=idcomp)
    
    
    competition.teams.remove(team)

    return HttpResponse('ok')