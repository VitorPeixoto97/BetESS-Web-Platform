from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group
from . import models, forms
from django.contrib.auth.decorators import login_required, permission_required
import json
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class IndexView(generic.ListView):
	template_name = 'index.html'
	context_object_name = 'club_list'
	def get_queryset(self):
		return models.Clube.objects.order_by('-nome')[:5]

class PostsView(ListAPIView):
    authentication_class = (JSONWebTokenAuthentication,) # Don't forget to add a 'comma' after first element to make it a tuple
    permission_classes = (IsAuthenticated,)

def index(request):
    context = 'Hello World'
    return render(request, 'server/index.html', context)



'''
def loginView(request):
    form = forms.LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return HttpResponse('ok')
        else:
            return HttpResponseBadRequest(content='invalid user')
    else:
        return HttpResponseBadRequest(content='bad form')

def logoutView(request):
    logout(request)
'''

def infoUserView(request, email):
  if models.Gestor.objects.filter(email=email).count()==0:
    clube = models.Tecnico.objects.get(email=email).clube
  else:
    clube = models.Gestor.objects.get(email=email).clube

  return JsonResponse(model_to_dict(clube))

def advNome(request, form_id):
  formacao = get_object_or_404(models.Formacao, id=form_id)
  return JsonResponse(model_to_dict(formacao.clube))


@login_required
@permission_required('add_clube', raise_exception=True)
def clubeView(request, nome, cor, simbolo):
    existe = False
    for clube in models.Clube.objects.all():
        if clube.nome == nome:
            existe = True
    if not existe:
        models.Clube.objects.create(nome=nome, cor=cor, simbolo=simbolo)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='clube already exists')


@login_required
@permission_required('change_clube', raise_exception=True)
def cClubeView(request, id, cor, simbolo):
    models.Clube.objects.filter(id=id).update(cor=cor, simbolo=simbolo)
    return HttpResponse('ok')


@login_required
@permission_required('view_clube', raise_exception=True)
def gClubeView(request, id):
    clube = get_object_or_404(models.Clube, id=id)
    return JsonResponse(model_to_dict(clube))


@login_required
@permission_required('view_clube', raise_exception=True)
def gClubesView(request):
    clubes = models.Clube.objects.all()
    aux = []
    for clube in clubes:
        aux.append(model_to_dict(clube))
    return JsonResponse(aux)


@login_required
@permission_required('add_gestor', raise_exception=True)
def gestorView(request):
    form = forms.UserForm(request.POST)
    if form.is_valid():
        existe = False
        for u in User.objects.all():
            if u.email == form.cleaned_data['email']:
                existe = True
        if not existe:
            group = Group.objects.get('Gestor')
            user, created = User.objects.create_user(first_name=form.cleaned_data['nome'], username=form.cleaned_data['email'], email=form.cleaned_data['email'], password=form.cleaned_data['password'], groups=group)
            if created:
                user.save()
                models.Gestor.objects.create(email=form.cleaned_data['email'], clube=form.cleaned_data['clube'])
                return HttpResponse('ok')
            else:
                return HttpResponseBadRequest(content='error')
        else:
            return HttpResponseBadRequest(content='email already in use')
    else:
        return HttpResponseBadRequest(content='bad form')


@login_required
@permission_required('add_formacao', raise_exception=True)
def formacaoView(request, clube, nome):
    clubex = get_object_or_404(models.Clube, id=clube)
    if clubex.formacao_set.get(nome=nome) is None:
        models.Formacao.objects.create(nome=nome, clube=clube)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='formacao already exists')


@login_required
@permission_required('delete_formacao', raise_exception=True)
def dFormacaoView(request, id):
    formacao = get_object_or_404(models.Formacao, id=id)
    formacao.delete()
    return HttpResponse('ok')


@login_required
@permission_required('view_formacao', raise_exception=True)
def gFormacoesView(request, clube):
    clubex = get_object_or_404(models.Clube, id=clube)
    formacoes = clubex.formacao_set.all()
    aux = []
    for formacao in formacoes:
        aux.append(model_to_dict(formacao))
    return JsonResponse(aux)


@login_required
@permission_required('view_formacao', raise_exception=True)
def gFormacaoView(request, id):
    formacao = get_object_or_404(models.Formacao, id=id)
    return JsonResponse(model_to_dict(formacao))


@login_required
@permission_required('add_atleta', raise_exception=True)
def atletaView(request, licenca, nome, formacao, camisola):
    formacaox = get_object_or_404(models.Formacao, id=formacao)
    if formacaox.atleta_set.get(licenca=licenca) is None:
        models.Atleta.objects.create(nome=nome, formacao=formacao, licensa=licenca, camisola=camisola)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='atleta already exists')


@login_required
@permission_required('change_atleta', raise_exception=True)
def cAtletaView(request, id, formacao, camisola):
    models.Atleta.objects.filter(id=id).update(formacao=formacao, camisola=camisola)
    return HttpResponse('ok')


@login_required
@permission_required('delete_atleta', raise_exception=True)
def dAtletaView(request, id):
    atleta = get_object_or_404(models.Atleta, id=id)
    atleta.delete()
    return HttpResponse('ok')


@login_required
@permission_required('view_atleta', raise_exception=True)
def gAtletas(request, formacao):
    formacaox = get_object_or_404(models.Formacao, id=formacao)
    atletas = formacaox.atleta_set.all()
    aux = []
    for atleta in atletas:
        aux.append(model_to_dict(atleta))
    return JsonResponse(aux)


@login_required
@permission_required('view_atleta', raise_exception=True)
def gAtleta(request, id):
    atleta = get_object_or_404(models.Atleta, id=id)
    return JsonResponse(model_to_dict(atleta))


@login_required
@permission_required('add_tecnico', raise_exception=True)
def tecnicoView(request):
    form = forms.UserForm(request.POST)
    if form.is_valid():
        existe = False
        for u in User.objects.all():
            if u.email == form.cleaned_data['email']:
                existe = True
        if not existe:
            group = Group.objects.get('Tecnico')
            user, created = User.objects.create_user(first_name=form.cleaned_data['nome'], username=form.cleaned_data['email'], email=form.cleaned_data['email'], password=form.cleaned_data['password'], groups=group)
            if created:
                user.save()
                models.Tecnico.objects.create(email=form.cleaned_data['email'], clube=form.cleaned_data['clube'])
                return HttpResponse('ok')
            else:
                return HttpResponseBadRequest(content='error')
        else:
            return HttpResponseBadRequest(content='email already in use')
    else:
        return HttpResponseBadRequest(content='bad form')


@login_required
@permission_required('change_tecnico', raise_exception=True)
def cTecnicoView(request, id, grelhaC, grelhaB):
    models.Tecnico.objects.filter(id=id).update(grelhaCampo=grelhaC, grelhaB=grelhaB)
    return HttpResponse('ok')


@login_required
@permission_required('add_jogo', raise_exception=True)
def jogoView(request, clube, formacao, formacaoAdv, casa, data, hora, tipo):
    models.Jogo.objects.create(ipo=tipo, clube=clube, formacao=formacao, adversario=formacaoAdv, casa=casa, data=data, hora=hora)
    return HttpResponse('ok')


@login_required
@permission_required('change_jogo', raise_exception=True)
def cJogoView(request, idJogo, grelhaC, grelhaB):
    models.Jogo.objects.filter(id=idJogo).update(grelhaCampo=grelhaC, grelhaBaliza=grelhaB)
    return HttpResponse('ok')


#@login_required
#@permission_required('view_jogo', raise_exception=True)
def gJogosView(request, clube):
    clubex = get_object_or_404(models.Clube, id=clube)
    formacoes = clubex.formacao_set.all()
    aux = []
    for formacao in formacoes:
        formacaox = get_object_or_404(models.Formacao, nome=formacao.nome, clube=formacao.clube)
        jogos = formacaox.minhaequipa.all()
        for jogo in jogos:
            new_jogo = {}
            new_jogo['id'] = jogo.id
            new_jogo['tipo'] = jogo.tipo
            if(jogo.casa):
                new_jogo['casa'] = "C"
            else:
                new_jogo['casa'] = "F"
            new_jogo['data'] = jogo.data
            new_jogo['hora'] = jogo.hora
            new_jogo['resultado'] = gResultado(jogo.id)
            new_jogo['grelhaCampo'] = jogo.grelhaCampo
            new_jogo['grelhaBaliza'] = jogo.grelhaBaliza
            new_jogo['adversario'] = jogo.adversario.id
            new_jogo['formacao'] = jogo.formacao.id
            new_jogo['adv_nome'] = jogo.adversario.clube.nome
            new_jogo['form_nome'] = jogo.formacao.nome
            aux.append(new_jogo)
    return JsonResponse(aux, safe=False)

def adversario(form_id):
    formacao = get_object_or_404(models.Formacao, id=form_id)
    return formacao.clube


#@login_required
#@permission_required('view_jogo', raise_exception=True)
def gJogoView(request, id):
    jogo = get_object_or_404(models.Jogo, id=id)
    new_jogo = {}
    new_jogo['id'] = jogo.id
    new_jogo['tipo'] = jogo.tipo
    if(jogo.casa):
        new_jogo['casa'] = "C"
    else:
        new_jogo['casa'] = "F"
    new_jogo['data'] = jogo.data
    new_jogo['hora'] = jogo.hora
    new_jogo['resultado'] = gResultado(jogo.id)
    new_jogo['grelhaCampo'] = jogo.grelhaCampo
    new_jogo['grelhaBaliza'] = jogo.grelhaBaliza
    new_jogo['adversario'] = jogo.adversario.id
    new_jogo['formacao'] = jogo.formacao.id
    new_jogo['adv_nome'] = jogo.adversario.clube.nome
    new_jogo['form_nome'] = jogo.formacao.nome
    new_jogo['clube_nome'] = jogo.formacao.clube.nome
    new_jogo['logoMe'] = jogo.formacao.clube.simbolo
    new_jogo['logoAdv'] = jogo.adversario.clube.simbolo
    return JsonResponse(new_jogo)

def gResultado(id):
    jogo = get_object_or_404(models.Jogo, id=id)
    eventos = jogo.evento_set.all()
    aux = []
    golosC=0
    golosF=0
    if (eventos.count()==0): return ""
    for evento in eventos:
        if (evento.tipo.id==0 and evento.equipa==jogo.formacao):
            golosC+=1
        elif (evento.tipo.id==0 and evento.equipa==jogo.adversario):
            golosF+=1
    return str(golosC)+"-"+str(golosF) 



@login_required
@permission_required('add_convocado', raise_exception=True)
def convocadoView(request, jogo, atleta, emCampo):
    models.Convocado.objects.create(atleta=atleta, jogo=jogo, emCampo=emCampo)
    return HttpResponse('ok')


@login_required
@permission_required('change_convocado', raise_exception=True)
def cConvocadoView(request, jogo, atleta, emCampo):
    models.Convocado.objects.filter(atleta=atleta, jogo=jogo).update(emCampo=emCampo)
    return HttpResponse('ok')


@login_required
@permission_required('view_convocado', raise_exception=True)
def gConvocadosView(request, idJogo):
    jogo = get_object_or_404(models.Jogo, id=idJogo)
    convocados = jogo.convocado_set.all()
    aux = []
    for conv in convocados:
        aux.append(model_to_dict(conv))
    return JsonResponse(aux)


@login_required
@permission_required('add_evento', raise_exception=True)
def eventoView(request):
    form = forms.CriarEventoForm(request.POST)
    if form.is_valid():
        eq = form.cleaned_data['equipa']
        at1 = form.cleaned_data['atleta1']
        at2 = form.cleaned_data['atleta2']
        zC = form.cleaned_data['zonaC']
        zB = form.cleaned_data['zonaB']
        novo = form.cleaned_data['novoinst']

        if novo:
            models.Evento.objects.create(tipo=form.cleaned_data['tipo'], jogo=form.cleaned_data['jogo'], instante=form.cleaned_data['instante'], novoinstante=novo)
        elif eq and at1 and at2:
            models.Evento.objects.create(tipo=form.cleaned_data['tipo'], jogo=form.cleaned_data['jogo'], equipa=eq, atleta1=at1, atleta2=at2, instante=form.cleaned_data['instante'])
        elif eq and at1 and zC and zB:
            models.Evento.objects.create(tipo=form.cleaned_data['tipo'], jogo=form.cleaned_data['jogo'], equipa=eq, atleta1=at1, zonaCampo=zC, zonaBaliza=zB, instante=form.cleaned_data['instante'])
        elif eq and at1 and zC:
            models.Evento.objects.create(tipo=form.cleaned_data['tipo'], jogo=form.cleaned_data['jogo'], equipa=eq, atleta1=at1, zonaCampo=zC, instante=form.cleaned_data['instante'])
        elif eq:
            models.Evento.objects.create(tipo=form.cleaned_data['tipo'], jogo=form.cleaned_data['jogo'], equipa=eq, instante=form.cleaned_data['instante'])

        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='bad form')


@login_required
@permission_required('change_evento', raise_exception=True)
def cEventoView(request):
    form = forms.CriarEventoForm(request.POST)
    if form.is_valid():
        eq = form.cleaned_data['equipa']
        at1 = form.cleaned_data['atleta1']
        at2 = form.cleaned_data['atleta2']
        zC = form.cleaned_data['zonaC']
        zB = form.cleaned_data['zonaB']
        novo = form.cleaned_data['novoinst']

        if novo:
            models.Evento.objects.filter(id=form.cleaned_data['idEvento']).update(instante=form.cleaned_data['instante'], novoinstante=novo)
        elif eq and at1 and at2:
            models.Evento.objects.filter(id=form.cleaned_data['idEvento']).update(equipa=eq, atleta1=at1, atleta2=at2, instante=form.cleaned_data['instante'])
        elif eq and at1 and zC and zB:
            models.Evento.objects.filter(id=form.cleaned_data['idEvento']).update(equipa=eq, atleta1=at1, zonaCampo=zC, zonaBaliza=zB, instante=form.cleaned_data['instante'])
        elif eq and at1 and zC:
            models.Evento.objects.filter(id=form.cleaned_data['idEvento']).update(equipa=eq, atleta1=at1, zonaCampo=zC, instante=form.cleaned_data['instante'])
        elif eq:
            models.Evento.objects.filter(id=form.cleaned_data['idEvento']).update(equipa=eq, instante=form.cleaned_data['instante'])

        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='bad form')


@login_required
@permission_required('delete_evento', raise_exception=True)
def dEventoView(request, id):
    evento = get_object_or_404(models.Evento, id=id)
    evento.delete()
    return HttpResponse('ok')


@login_required
@permission_required('view_evento', raise_exception=True)
def gEventosView(request, idJogo):
    jogo = get_object_or_404(models.Jogo, id=idJogo)
    eventos = jogo.evento_set.all()
    aux = []
    for evento in eventos:
        aux.append(model_to_dict(evento))
    return JsonResponse(aux)


@login_required
@permission_required('view_evento', raise_exception=True)
def gEventoView(request, id):
    evento = get_object_or_404(models.Evento, id=id)
    return JsonResponse(model_to_dict(evento))


@login_required
@permission_required('add_tipoevento', raise_exception=True)
def tipoEventoView(request, tipo, atleta1, atleta2, zonaC, zonaB, novoinst):
    if models.TipoEvento.objects.get(tipo=tipo) is None:
        models.TipoEvento.objects.create(tipo=tipo, atleta1=atleta1, atleta2=atleta2, zonaC=zonaC, zonaB=zonaB, novoinst=novoinst)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='tipo already exists')


@login_required
@permission_required('view_tipoevento', raise_exception=True)
def gTiposEventosView(request):
    tipos = models.TipoEvento.objects.all()
    aux = []
    for tipo in tipos:
        aux.append(model_to_dict(tipo))
    return JsonResponse(aux)


@login_required
@permission_required('add_tiposselecionados', raise_exception=True)
def tipoSelecionadoView(request, tipo, tecnico):
    models.TiposSelecionados.objects.create(tecnico=tecnico, tipo=tipo)
    return HttpResponse('ok')


@login_required
@permission_required('delete_tiposselecionados', raise_exception=True)
def dTipoSelecionadoView(request, id):
    tipo = get_object_or_404(models.TiposSelecionados, id=id)
    tipo.delete()
    return HttpResponse('ok')


@login_required
@permission_required('view_tiposselecionados', raise_exception=True)
def gTiposSelecionadosView(request, tecnico):
    tecnicox = get_object_or_404(models.Tecnico, id=tecnico)
    tipos = tecnicox.tiposselecionados_set.all()
    aux=[]
    for tipo in tipos:
        aux.append(model_to_dict(tipo))
    return JsonResponse(aux)

