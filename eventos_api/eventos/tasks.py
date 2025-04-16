from celery import shared_task
from .tasks_warning import processar_warning_evento
from .tasks_error import processar_error_evento

@shared_task(queue="celery")  # essa task atua como dispatcher
def processar_evento_async(titulo, descricao):
    print(f"[Dispatcher] Processando evento: {titulo} - {descricao}")

    status = "success"
    if "warning" in descricao.lower():
        print(f"[Dispatcher] Evento 'warning' detectado: {descricao}")
        status = "warning"
    elif "error" in descricao.lower():
        print(f"[Dispatcher] Evento 'error' detectado: {descricao}")
        status = "error"

    if status == "warning":
        processar_warning_evento.apply_async(args=[titulo, descricao])
    elif status == "error":
        processar_error_evento.apply_async(args=[titulo, descricao])
    else:
        print("[Dispatcher] Evento 'success' não precisa de processamento adicional.")
