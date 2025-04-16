from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Evento, Erro
from .serializers import EventoSerializer, ErroSerializer
from .tasks import processar_evento_async

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        evento = serializer.save()
        processar_evento_async.delay(evento.titulo, evento.descricao)
        
class ErroViewSet(viewsets.ModelViewSet):
    queryset = Erro.objects.all()
    serializer_class = ErroSerializer
    permission_classes = [permissions.IsAuthenticated]