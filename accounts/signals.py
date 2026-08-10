from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def enviar_email_boas_vindas(sender, instance, created, **kwargs):
    if created:  # Só dispara se um NOVO usuário for criado
        # Garante que temos um e-mail válido antes de tentar enviar
        if instance.email:
            assunto = 'Bem-vindo ao nosso E-commerce!'
            mensagem = (
                f'Olá, {instance.username}!\n\n'
                'Sua conta foi criada com sucesso no nosso sistema.\n'
                'Estamos muito felizes em ter você por aqui. Aproveite nossas ofertas!\n\n'
                'Boas compras!'
            )
            remetente = settings.EMAIL_HOST_USER
            destinatario = [instance.email]
            
            # fail_silently=True evita que o site trave se o e-mail falhar por algum motivo externo
            send_mail(assunto, message=mensagem, from_email=remetente, recipient_list=destinatario, fail_silently=True)