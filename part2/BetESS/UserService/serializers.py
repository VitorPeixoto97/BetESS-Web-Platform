from rest_framework import serializers
from .models import *

class ClubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clube
        fields = '__all__'

class FormacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formacao
        fields = '__all__'

class AtletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atleta
        fields = '__all__'

class GestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestor
        fields = '__all__'

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = '__all__'

class JogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogo
        fields = '__all__'

class ConvocadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocado
        fields = '__all__'

class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvento
        fields = '__all__'

class TiposSelecionadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposSelecionados
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'