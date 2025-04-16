from celery import shared_task
from .models import Erro
from django.core.mail import send_mail

@shared_task(queue="error_queue")
def processar_error_evento(titulo, descricao):
    print(f"[ERROR] Evento crítico: {titulo} - Enviando e-mail...")
    Erro.objects.create(titulo=titulo, descricao=descricao)
    send_mail(
        subject="ERRO CRÍTICO",
        message=f"Título: {titulo}\nDescrição: {descricao}",
        from_email="sistema@eventos.com",
        recipient_list=["admin@exemplo.com"],
        fail_silently=False
    )
