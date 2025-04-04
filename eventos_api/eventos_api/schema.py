import graphene
from graphene_django.types import DjangoObjectType
from eventos.models import Evento  # ajuste conforme seu modelo

class EventoType(DjangoObjectType):
    class Meta:
        model = Evento
        fields = ("id", "titulo", "descricao", "resultado")

class Query(graphene.ObjectType):
    eventos_warning = graphene.List(EventoType)

    def resolve_eventos_warning(root, info):
        return Evento.objects.filter(descricao__icontains="warning")

schema = graphene.Schema(query=Query)
