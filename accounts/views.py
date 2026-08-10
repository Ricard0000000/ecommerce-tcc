from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail  
from django.conf import settings        

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email')
            user.save()

            # --- 📨 DISPARO AUTOMÁTICO DO E-MAIL DE BOAS-VINDAS ---
            if user.email:  
                try:
                    assunto = 'Bem-vindo à nossa loja! 🎉'
                    mensagem = (
                        f'Olá, {user.username}!\n\n'
                        f'Sua conta foi criada com sucesso no nosso sistema. '
                        f'Agora você já pode fazer o seu login, montar o seu carrinho '
                        f'e aproveitar todos os nossos produtos!\n\n'
                        f'Obrigado por se cadastrar conosco.'
                    )
                    
                    send_mail(
                        assunto,
                        mensagem,
                        settings.EMAIL_HOST_USER,
                        [user.email],  
                        fail_silently=True
                    )
                except Exception as e:
                    print("Erro ao enviar e-mail de cadastro:", e)

            # 💡 MATAMOS A CHARADA AQUI: 
            # Se ele digitou um e-mail, mostra para onde foi enviado. Se não digitou, dá a mensagem padrão.
            if user.email:
                messages.success(
                    request,
                    f"Conta criada com sucesso! E-mail de confirmação enviado para {user.email}."
                )
            else:
                messages.success(
                    request,
                    "Conta criada com sucesso! Faça login agora."
                )

            return redirect('login')
        else:
            print("ERROS FORM:")
            print(form.errors)
    else:
        form = UserCreationForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )