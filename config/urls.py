from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from produtos.views import (
    home,
    adicionar_carrinho,
    adicionar_carrinho_ajax,
    ver_carrinho,
    diminuir_carrinho,
    remover_carrinho,
    painel_produtos,
    editar_produto,
    excluir_produto,
    produtos_categoria,
    produto_detalhe,
    finalizar_pedido,
    pedido_sucesso,
    meus_pedidos,
    detalhe_pedido,
    checkout,
    pagamento_pix,
    verificar_pagamento,
    teste_melhor_envio
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # HOME
    path('', home, name='home'),

    # TESTE MELHOR ENVIO
    path(
        'teste-melhor-envio/',
        teste_melhor_envio,
        name='teste_melhor_envio'
),

    # ACCOUNTS
    path('accounts/', include('accounts.urls')),

    # CATEGORIA
    path(
        'categoria/<int:categoria_id>/',
        produtos_categoria,
        name='produtos_categoria'
    ),

    # PRODUTO
    path(
        'produto/<int:id>/',
        produto_detalhe,
        name='produto_detalhe'
    ),

    # CARRINHO
    path('carrinho/', ver_carrinho, name='ver_carrinho'),

    path(
        'carrinho/add/<int:id>/',
        adicionar_carrinho,
        name='add_carrinho'
    ),

    path(
        'carrinho/diminuir/<int:id>/',
        diminuir_carrinho,
        name='diminuir_carrinho'
    ),

    path(
        'carrinho/remover/<int:id>/',
        remover_carrinho,
        name='remover_carrinho'
    ),

    # AJAX
    path(
        'carrinho/ajax/add/<int:id>/',
        adicionar_carrinho_ajax,
        name='add_carrinho_ajax'
    ),

    # CHECKOUT
    path(
        'checkout/',
        checkout,
        name='checkout'
    ),

    # PAGAMENTO PIX
    path(
        'pagamento-pix/<int:pedido_id>/',
        pagamento_pix,
        name='pagamento_pix'
    ),

    path(
        'verificar-pagamento/<int:pedido_id>/',
        verificar_pagamento,
        name='verificar_pagamento'
    ),

    # FINALIZAR PEDIDO
    path(
        'finalizar-pedido/',
        finalizar_pedido,
        name='finalizar_pedido'
    ),

    # PEDIDO SUCESSO
    path(
        'pedido/sucesso/<int:pedido_id>/',
        pedido_sucesso,
        name='pedido_sucesso'
    ),

    # MEUS PEDIDOS
    path(
        'meus-pedidos/',
        meus_pedidos,
        name='meus_pedidos'
    ),

    # DETALHE PEDIDO
    path(
        'pedido/<int:pedido_id>/',
        detalhe_pedido,
        name='detalhe_pedido'
    ),

    # LOGIN
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    # LOGOUT
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='login'
        ),
        name='logout'
    ),

    # PAINEL
    path(
        'painel/',
        painel_produtos,
        name='painel'
    ),

    path(
        'painel/editar/<int:id>/',
        editar_produto,
        name='editar_produto'
    ),

    path(
        'painel/excluir/<int:id>/',
        excluir_produto,
        name='excluir_produto'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )