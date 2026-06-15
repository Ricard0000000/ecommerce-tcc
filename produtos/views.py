import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from .models import Produto, Categoria, Banner, Pedido, ItemPedido

@login_required
def teste_melhor_envio(request):

    from .melhor_envio import testar_api

    return JsonResponse(testar_api())

# 🔧 FUNÇÃO AUXILIAR: limpa carrinho
def limpar_carrinho(carrinho):

    carrinho_limpo = {}

    for produto_id, quantidade in carrinho.items():

        if Produto.objects.filter(id=produto_id).exists():
            carrinho_limpo[str(produto_id)] = quantidade

    return carrinho_limpo


# 🛒 DADOS GLOBAIS DO CARRINHO
def dados_carrinho(request):

    carrinho = limpar_carrinho(
        request.session.get('carrinho', {})
    )

    request.session['carrinho'] = carrinho

    total_itens = sum(carrinho.values())

    categorias = Categoria.objects.all()

    return {
        'total_itens': total_itens,
        'categorias': categorias
    }


# 🏠 HOME
def home(request):

    produtos = Produto.objects.filter(ativo=True)

    categorias = Categoria.objects.all()

    banner = Banner.objects.filter(
        ativo=True
    ).first()

    carrinho = limpar_carrinho(
        request.session.get('carrinho', {})
    )

    request.session['carrinho'] = carrinho

    total_itens = sum(carrinho.values())

    return render(request, 'home.html', {
        'produtos': produtos,
        'categorias': categorias,
        'total_itens': total_itens,
        'banner': banner
    })


# 📁 CATEGORIA
def produtos_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    produtos = Produto.objects.filter(
        ativo=True,
        categoria=categoria
    )

    categorias = Categoria.objects.all()

    banner = Banner.objects.filter(
        ativo=True
    ).first()

    carrinho = limpar_carrinho(
        request.session.get('carrinho', {})
    )

    request.session['carrinho'] = carrinho

    total_itens = sum(carrinho.values())

    return render(request, 'home.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_atual': categoria,
        'total_itens': total_itens,
        'banner': banner
    })


# 📄 DETALHE PRODUTO
def produto_detalhe(request, id):

    produto = get_object_or_404(
        Produto,
        id=id
    )

    categorias = Categoria.objects.all()

    carrinho = limpar_carrinho(
        request.session.get('carrinho', {})
    )

    request.session['carrinho'] = carrinho

    total_itens = sum(carrinho.values())

    return render(request, 'produto.html', {
        'produto': produto,
        'categorias': categorias,
        'total_itens': total_itens
    })


# ➕ ADICIONAR CARRINHO
def adicionar_carrinho(request, id):

    produto = get_object_or_404(
        Produto,
        id=id
    )

    carrinho = request.session.get(
        'carrinho',
        {}
    )

    produto_id = str(produto.id)

    carrinho[produto_id] = (
        carrinho.get(produto_id, 0) + 1
    )

    request.session['carrinho'] = carrinho
    request.session.modified = True

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'home'
        )
    )


# 🚀 AJAX
def adicionar_carrinho_ajax(request, id):

    produto = get_object_or_404(
        Produto,
        id=id
    )

    carrinho = request.session.get(
        'carrinho',
        {}
    )

    produto_id = str(produto.id)

    carrinho[produto_id] = (
        carrinho.get(produto_id, 0) + 1
    )

    request.session['carrinho'] = carrinho
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "message": f"{produto.nome} adicionado 🛒",
        "total_itens": sum(carrinho.values())
    })


# 🛒 VER CARRINHO
def ver_carrinho(request):

    carrinho = limpar_carrinho(
        request.session.get('carrinho', {})
    )

    request.session['carrinho'] = carrinho

    produtos = Produto.objects.filter(
        id__in=carrinho.keys()
    )

    itens = []

    total = 0

    for produto in produtos:

        quantidade = carrinho.get(
            str(produto.id),
            0
        )

        subtotal = produto.preco * quantidade

        itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })

        total += subtotal

    return render(request, 'carrinho.html', {
        'itens': itens,
        'total': total,
        'total_itens': sum(carrinho.values())
    })


# 🔥 CHECKOUT
@login_required
def checkout(request):

    carrinho = limpar_carrinho(
        request.session.get('carrinho', {})
    )

    if not carrinho:

        messages.error(
            request,
            "Seu carrinho está vazio."
        )

        return redirect('ver_carrinho')

    produtos = Produto.objects.filter(
        id__in=carrinho.keys()
    )

    itens = []

    total = 0

    for produto in produtos:

        quantidade = carrinho.get(
            str(produto.id),
            0
        )

        subtotal = produto.preco * quantidade

        itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })

        total += subtotal

    return render(request, 'checkout.html', {
        'itens': itens,
        'total': total
    })


# ➖ DIMINUIR
def diminuir_carrinho(request, id):

    carrinho = request.session.get(
        'carrinho',
        {}
    )

    produto_id = str(id)

    if produto_id in carrinho:

        carrinho[produto_id] -= 1

        if carrinho[produto_id] <= 0:
            del carrinho[produto_id]

    request.session['carrinho'] = carrinho
    request.session.modified = True

    return redirect('ver_carrinho')


# 🗑 REMOVER
def remover_carrinho(request, id):

    carrinho = request.session.get(
        'carrinho',
        {}
    )

    produto_id = str(id)

    if produto_id in carrinho:
        del carrinho[produto_id]

    request.session['carrinho'] = carrinho
    request.session.modified = True

    return redirect('ver_carrinho')


# 🔐 PAINEL
@login_required
def painel_produtos(request):

    produtos = Produto.objects.all()

    return render(request, 'painel.html', {
        'produtos': produtos
    })


# ✏️ EDITAR
@login_required
def editar_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id
    )

    if request.method == 'POST':

        produto.nome = request.POST['nome']
        produto.preco = request.POST['preco']
        produto.ativo = True

        produto.save()

        messages.success(
            request,
            "Produto atualizado!"
        )

        return redirect('painel')

    return render(request, 'editar_produto.html', {
        'produto': produto
    })


# 🗑 EXCLUIR
@login_required
def excluir_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id
    )

    produto.delete()

    messages.success(
        request,
        "Produto excluído!"
    )

    return redirect('painel')


# 💳 FINALIZAR PEDIDO
@login_required
def finalizar_pedido(request):

    carrinho = request.session.get(
        'carrinho',
        {}
    )

    if not carrinho:

        messages.error(
            request,
            "Seu carrinho está vazio."
        )

        return redirect('ver_carrinho')

    produtos = Produto.objects.filter(
        id__in=carrinho.keys()
    )

    total = Decimal('0.00')

    for produto in produtos:

        quantidade = carrinho.get(
            str(produto.id),
            0
        )

        total += produto.preco * quantidade

    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total,
        status='pendente',

        nome_cliente=request.POST.get(
            'nome_cliente',
            ''
        ),

        telefone=request.POST.get(
            'telefone',
            ''
        ),

        cep=request.POST.get(
            'cep',
            ''
        ),

        cidade=request.POST.get(
            'cidade',
            ''
        ),

        endereco=request.POST.get(
            'endereco',
            ''
        ),

        numero=request.POST.get(
            'numero',
            ''
        ),

        complemento=request.POST.get(
            'complemento',
            ''
        ),
    )

    for produto in produtos:

        quantidade = carrinho.get(
            str(produto.id),
            0
        )

        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            preco=produto.preco,
            quantidade=quantidade
        )

    request.session['carrinho'] = {}
    request.session.modified = True

    return redirect(
        'pagamento_pix',
        pedido_id=pedido.id
    )


# 🎉 PEDIDO SUCESSO
@login_required
def pedido_sucesso(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        usuario=request.user
    )

    return render(request, 'pedido_sucesso.html', {
        'pedido': pedido
    })


# 📋 MEUS PEDIDOS
@login_required
def meus_pedidos(request):

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')

    return render(request, 'meus_pedidos.html', {
        'pedidos': pedidos
    })


# 🔎 DETALHE DO PEDIDO
@login_required
def detalhe_pedido(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        usuario=request.user
    )

    itens = pedido.itens.all()

    return render(request, 'detalhe_pedido.html', {
        'pedido': pedido,
        'itens': itens
    })

# PIX
@login_required
def pagamento_pix(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        usuario=request.user
    )

    qr_code = None
    qr_code_base64 = None

    try:

        print("=================================")
        print("USUARIO LOGADO:", request.user)
        print("EMAIL USUARIO:", request.user.email)
        print("PEDIDO USUARIO:", pedido.usuario)
        print("EMAIL PEDIDO:", pedido.usuario.email)
        print("=================================")

        sdk = mercadopago.SDK(
            settings.MERCADOPAGO_ACCESS_TOKEN
        )

        payment_data = {
            "transaction_amount": float(pedido.total),
            "description": f"Pedido #{pedido.id}",
            "payment_method_id": "pix",
            "payer": {
                "email": pedido.usuario.email
            }
        }

        resultado = sdk.payment().create(payment_data)

        print("RESPOSTA MP:")
        print(resultado)

        if resultado["status"] == 201:

            resposta = resultado["response"]

            pedido.mercadopago_id = str(
                resposta["id"]
            )
            pedido.save()

            print(
                "PAGAMENTO SALVO:",
                pedido.mercadopago_id
            )

            qr_code = resposta[
                "point_of_interaction"
            ]["transaction_data"][
                "qr_code"
            ]

            qr_code_base64 = resposta[
                "point_of_interaction"
            ]["transaction_data"][
                "qr_code_base64"
            ]

    except Exception as e:

        print("ERRO MP:")
        print(e)

    return render(
        request,
        'pagamento_pix.html',
        {
            'pedido': pedido,
            'qr_code': qr_code,
            'qr_code_base64': qr_code_base64,
        }
    )


@login_required
def verificar_pagamento(request, pedido_id):

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        usuario=request.user
    )

    if not pedido.mercadopago_id:

        return JsonResponse({
            'status': 'erro'
        })

    try:

        sdk = mercadopago.SDK(
            settings.MERCADOPAGO_ACCESS_TOKEN
        )

        pagamento = sdk.payment().get(
            pedido.mercadopago_id
        )

        status_mp = pagamento[
            "response"
        ]["status"]

        print(
            "STATUS MP:",
            status_mp
        )

        if status_mp == "approved":

            pedido.status = "pago"
            pedido.save()

            return JsonResponse({
                'status': 'aprovado'
            })

        return JsonResponse({
            'status': 'pendente'
        })

    except Exception as e:

        print(e)

        return JsonResponse({
            'status': 'erro'
        })