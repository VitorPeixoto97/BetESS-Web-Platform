import django_filters.rest_framework
from rest_framework import viewsets
from .models import Clube, Atleta
from .serializers import *


class ClubeViewSet(viewsets.ModelViewSet):
    queryset = Clube.objects.all()
    serializer_class = ClubeSerializer

class FormacaoViewSet(viewsets.ModelViewSet):
    queryset = Formacao.objects.all()
    serializer_class = FormacaoSerializer

class AtletaViewSet(viewsets.ModelViewSet):
    queryset = Atleta.objects.all()
    serializer_class = AtletaSerializer

class GestorViewSet(viewsets.ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer

class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer

class JogoViewSet(viewsets.ModelViewSet):
    queryset = Jogo.objects.all()
    serializer_class = JogoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = '__all__'

class ConvocadoViewSet(viewsets.ModelViewSet):
    queryset = Convocado.objects.all()
    serializer_class = ConvocadoSerializer

class TipoEventoViewSet(viewsets.ModelViewSet):
    queryset = TipoEvento.objects.all()
    serializer_class = TipoEventoSerializer

class TiposSelecionadosViewSet(viewsets.ModelViewSet):
    queryset = TiposSelecionados.objects.all()
    serializer_class = TiposSelecionadosSerializer

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer