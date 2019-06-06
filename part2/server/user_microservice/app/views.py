from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group
from . import models
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

def gUsersView(request):
    users = models.User.objects.all()
    aux = []
    for user in users:
        aux.append(model_to_dict(user))
    return JsonResponse(aux, safe=False)

def infoUserView(request, email):
  user = models.User.objects.get(email=email)

  return JsonResponse(model_to_dict(user))

def userView(request, username, email, password, name, coins):
    existe = False
    for user in models.User.objects.all():
        if user.email == email:
            existe = True
    if not existe:
        models.User.objects.create(username=username, email=email, password=password, name=name, coins=coins+10)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest(content='user already exists')

def cUserView(request, id, email, username, password, name, coins):
    models.User.objects.filter(id=id).update(email, username, password, name, coins)
    return HttpResponse('ok')

def dUserView(request, id):
    user = get_object_or_404(models.User, id=id)
    user.delete()
    return HttpResponse('ok')
