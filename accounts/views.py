from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.email = request.POST.get('email')

            user.save()

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