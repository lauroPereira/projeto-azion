from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Evento
from .serializers import EventoSerializer
from .tasks import processar_evento_async

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        evento = serializer.save()
        processar_evento_async.delay(evento.titulo, evento.descricao)