from celery import shared_task
from .models import Erro

@shared_task(queue="warning_queue")
def processar_warning_evento(titulo, descricao):
    print(f"[WARNING] Salvando evento warning: {titulo}")
    Erro.objects.create(titulo=titulo, descricao=descricao)
