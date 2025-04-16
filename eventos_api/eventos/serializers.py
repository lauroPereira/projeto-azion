from rest_framework import serializers
from .models import Evento, Erro

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class ErroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Erro
        fields = '__all__'