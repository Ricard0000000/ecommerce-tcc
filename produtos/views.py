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


# 🏠 HOME (Correção definitiva da trava de segurança)
def home(request):
    # 💡 Usando o operador AND do Django (vírgula):
    # O produto precisa estar ativo (True)
    # E o produto precisa estar com 'destaque_home=True' (Exibir na Home?)
    # E a categoria dele também precisa estar com 'destaque_home=True'
    produtos = Produto.objects.filter(
        ativo=True,
        destaque_home=True,
        categoria__destaque_home=True
    )

    # Mantém o restante da sua lógica igual
    categorias = Categoria.objects.all()
    banner = Banner.objects.filter(ativo=True).first()
    carrinho = limpar_carrinho(request.session.get('carrinho', {}))
    request.session['carrinho'] = carrinho
    total_itens = sum(carrinho.values())

    return render(request, 'home.html', {
        'produtos': produtos,
        'categorias': categorias,
        'total_itens': total_itens,
        'banner': banner
    })


# 📁 CATEGORIA (Correção: Mostra todos os produtos ativos da categoria clicada)
def produtos_categoria(request, categoria_id):
    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    # 💡 ATENÇÃO AQUI: Para a página da categoria, buscamos apenas se está ATIVO.
    # Não colocamos o filtro de destaque_home aqui, senão o produto some da categoria também!
    produtos = Produto.objects.filter(
        ativo=True,
        categoria=categoria
    )

    # Mantém todas as categorias na barra de navegação
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
    produto = get_object_or_404(Produto, id=id)
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto.id)

    carrinho[produto_id] = carrinho.get(produto_id, 0) + 1
    request.session['carrinho'] = carrinho
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "message": f"{produto.nome} adicionado 🛒",
        "total_itens": sum(carrinho.values())
    })

# 🛒 VER CARRINHO
def ver_carrinho(request):
    carrinho = limpar_carrinho(request.session.get('carrinho', {}))
    request.session['carrinho'] = carrinho

    # --- ALTERAÇÃO AQUI: Limpa o frete sempre que abrir o carrinho ---
    if 'frete_selecionado' in request.session:
        del request.session['frete_selecionado']
    # -----------------------------------------------------------------

    produtos = Produto.objects.filter(id__in=carrinho.keys())
    itens = []
    total = 0

    for produto in produtos:
        quantidade = carrinho.get(str(produto.id), 0)
        subtotal = produto.preco * quantidade
        itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
        total += subtotal

    # Como acabamos de deletar o frete da sessão acima, 
    # o total_com_frete será sempre igual ao total dos produtos aqui
    total_com_frete = total
    frete_selecionado = None 

    return render(request, 'carrinho.html', {
        'itens': itens,
        'total': total,
        'total_com_frete': total_com_frete,
        'total_itens': sum(carrinho.values()),
        'frete_selecionado': frete_selecionado
    })


# 🔥 CHECKOUT
@login_required
def checkout(request):
    carrinho = limpar_carrinho(request.session.get('carrinho', {}))

    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('ver_carrinho')

    produtos = Produto.objects.filter(id__in=carrinho.keys())
    itens = []
    total = 0

    for produto in produtos:
        quantidade = carrinho.get(str(produto.id), 0)
        subtotal = produto.preco * quantidade
        itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
        total += subtotal

    frete_selecionado = request.session.get('frete_selecionado')
    total_com_frete = total

    if frete_selecionado:
        try:
            valor_frete = float(str(frete_selecionado.get('valor', 0)).replace(',', '.'))
            total_com_frete += Decimal(str(valor_frete))
        except (ValueError, TypeError):
            pass

    return render(request, 'checkout.html', {
        'itens': itens,
        'total': total,
        'total_com_frete': total_com_frete,
        'frete_selecionado': frete_selecionado,
        'cep_calculado': request.session.get('cep_calculado', '') # 👈 Adicione essa linha aqui
    })


# ➖ DIMINUIR
def diminuir_carrinho(request, id):
    carrinho = request.session.get('carrinho', {})
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
    carrinho = request.session.get('carrinho', {})
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
    return render(request, 'painel.html', {'produtos': produtos})


# ✏️ EDITAR
@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.nome = request.POST['nome']
        produto.preco = request.POST['preco']
        produto.ativo = True
        produto.save()
        messages.success(request, "Produto updated!")
        return redirect('painel')

    return render(request, 'editar_produto.html', {'produto': produto})


# 🗑 EXCLUIR
@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    messages.success(request, "Produto excluído!")
    return redirect('painel')































# ==============================================================================
# 💳 BLOCO 3: FINALIZAR PEDIDO, SUCESSO, MEUS PEDIDOS, MERCADO PAGO E FRETE
# ==============================================================================
from django.core.mail import send_mail  # 👈 Importação adicionada para os e-mails

@login_required
def finalizar_pedido(request):
    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('ver_carrinho')

    produtos = Produto.objects.filter(id__in=carrinho.keys())
    total = Decimal('0.00')

    for produto in produtos:
        quantidade = carrinho.get(str(produto.id), 0)
        total += produto.preco * quantidade

    # Adiciona o valor do frete ao total final do Pedido gerado
    frete_selecionado = request.session.get('frete_selecionado')
    if frete_selecionado:
        try:
            valor_frete = float(str(frete_selecionado.get('valor', 0)).replace(',', '.'))
            total += Decimal(str(valor_frete))
        except (ValueError, TypeError):
            pass

    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total,
        status='pendente',
        nome_cliente=request.POST.get('nome_cliente', ''),
        telefone=request.POST.get('telefone', ''),
        cep=request.POST.get('cep', ''),
        cidade=request.POST.get('cidade', ''),
        endereco=request.POST.get('endereco', ''),
        numero=request.POST.get('numero', ''),
        complemento=request.POST.get('complemento', ''),
    )

    for produto in produtos:
        quantidade = carrinho.get(str(produto.id), 0)
        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            preco=produto.preco,
            quantidade=quantidade
        )

    # Limpa carrinho e frete após criar o pedido com sucesso
    request.session['carrinho'] = {}
    if 'frete_selecionado' in request.session:
        del request.session['frete_selecionado']
    request.session.modified = True

    return redirect('pagamento_pix', pedido_id=pedido.id)


# 🎉 PEDIDO SUCESSO
@login_required
def pedido_sucesso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'pedido_sucesso.html', {'pedido': pedido})


# 📋 MEUS PEDIDOS
@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'meus_pedidos.html', {'pedidos': pedidos})


# 🔎 DETALHE DO PEDIDO
@login_required
def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    itens = pedido.itens.all()
    return render(request, 'detalhe_pedido.html', {'pedido': pedido, 'itens': itens})


# ⚡ MERCADO PAGO: PIX
@login_required
def pagamento_pix(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    qr_code = None
    qr_code_base64 = None

    try:
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        payment_data = {
            "transaction_amount": float(pedido.total),
            "description": f"Pedido #{pedido.id}",
            "payment_method_id": "pix",
            "payer": {
                "email": pedido.usuario.email
            }
        }

        resultado = sdk.payment().create(payment_data)

        if resultado["status"] == 201:
            resposta = resultado["response"]
            pedido.mercadopago_id = str(resposta["id"])
            pedido.save()

            qr_code = resposta["point_of_interaction"]["transaction_data"]["qr_code"]
            qr_code_base64 = resposta["point_of_interaction"]["transaction_data"]["qr_code_base64"]

    except Exception as e:
        print("ERRO MP:", e)

    return render(request, 'pagamento_pix.html', {
        'pedido': pedido,
        'qr_code': qr_code,
        'qr_code_base64': qr_code_base64,
    })


# 🔍 VERIFICAR STATUS DO PAGAMENTO (E ENVIAR E-MAIL SE APROVADO)
@login_required
def verificar_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    if not pedido.mercadopago_id:
        return JsonResponse({'status': 'erro'})

    try:
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        pagamento = sdk.payment().get(pedido.mercadopago_id)
        status_mp = pagamento["response"]["status"]

        if status_mp == "approved":
            # Só dispara se o status no banco ainda não era 'pago' (evita duplicar e-mails)
            if pedido.status != "pago":
                pedido.status = "pago"
                pedido.save()

                # --- 📨 DISPARO DO E-MAIL DE CONFIRMAÇÃO ---
                try:
                    assunto = f'Pagamento Confirmado! Pedido #{pedido.id}'
                    
                    # Monta a listagem de produtos para o corpo do e-mail
                    lista_itens = ""
                    for item in pedido.itens.all():
                        lista_itens += f"- {item.produto.nome} (Qtd: {item.quantidade}) - R$ {item.preco}\n"

                    mensagem = (
                        f'Olá, {pedido.nome_cliente or pedido.usuario.username}!\n\n'
                        f'Seu pagamento para o pedido #{pedido.id} foi aprovado com sucesso! 🎉\n\n'
                        f'--- Detalhes do Pedido ---\n'
                        f'{lista_itens}\n'
                        f'Valor Total Pago: R$ {pedido.total}\n\n'
                        f'--- Endereço de Entrega ---\n'
                        f'{pedido.endereco}, Nº {pedido.numero}\n'
                        f'{pedido.cidade} - CEP: {pedido.cep}\n\n'
                        f'Obrigado por comprar conosco! Entraremos em contato assim que o produto for postado.'
                    )
                    
                    send_mail(
                        assunto,
                        mensagem,
                        settings.EMAIL_HOST_USER,
                        [pedido.usuario.email],
                        fail_silently=True
                    )
                except Exception as email_error:
                    print("Erro ao enviar e-mail de confirmação:", email_error)
                # -------------------------------------------

            return JsonResponse({'status': 'aprovado'})

        return JsonResponse({'status': 'pendente'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'erro'})


# 🚚 VIEWS INTEGRADAS: CALCULAR E SELECIONAR FRETE
def calcular_frete(request):
    if request.method == 'POST':
        cep_destino = request.POST.get('cep')
        if not cep_destino:
            return JsonResponse({'success': False, 'message': 'CEP não fornecido.'})
        
        request.session['cep_calculado'] = cep_destino
        request.session.modified = True

        carrinho = limpar_carrinho(request.session.get('carrinho', {}))
        if not carrinho:
            return JsonResponse({'success': False, 'message': 'O carrinho está vazio.'})
            
        produtos_no_banco = Produto.objects.filter(id__in=carrinho.keys())
        produtos_carrinho_api = []
        
        for produto in produtos_no_banco:
            quantidade = carrinho.get(str(produto.id), 0)
            produtos_carrinho_api.append({
                "id": str(produto.id),
                "width": float(produto.largura),
                "height": float(produto.altura),
                "length": float(produto.comprimento),
                "weight": float(produto.peso),
                "insurance_value": float(produto.preco),
                "quantity": int(quantidade)
            })
        
        from .melhor_envio import calcular_frete_api
        
        res_api = calcular_frete_api(cep_destino, produtos_carrinho_api)
        
        if isinstance(res_api, list):
            opcoes_validas = []
            for item in res_api:
                if 'error' not in item and 'price' in item:
                    opcoes_validas.append({
                        'name': item.get('name'),
                        'price': item.get('price'),
                        'delivery_time': item.get('delivery_time')
                    })
            return JsonResponse({'success': True, 'opcoes': opcoes_validas})
            
        elif isinstance(res_api, dict) and 'message' in res_api:
            return JsonResponse({'success': False, 'message': res_api['message']})
            
        return JsonResponse({'success': False, 'message': 'Nenhuma opção de frete disponível no momento.'})
        
    return JsonResponse({'success': False, 'message': 'Método inválido.'})

def selecionar_frete(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor = request.POST.get('valor')
        
        if nome and valor:
            request.session['frete_selecionado'] = {
                'name': nome,
                'valor': valor
            }
            request.session.modified = True
            return JsonResponse({'success': True})
            
        return JsonResponse({'success': False, 'message': 'Dados incompletos.'})
        
    return JsonResponse({'success': False, 'message': 'Método inválido.'})