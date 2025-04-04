from celery import shared_task

@shared_task
def processar_evento_async(titulo, descricao):
    print(f"[Celery] Processando evento: {titulo} - {descricao}")
    return f"Evento processado: {titulo}"