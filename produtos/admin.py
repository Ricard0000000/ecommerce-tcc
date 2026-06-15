from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import (
    Produto,
    Categoria,
    Banner,
    Pedido,
    ItemPedido
)


# ❌ REMOVE USERS E GROUPS DO ADMIN
admin.site.unregister(Group)
admin.site.unregister(User)


# 📁 CATEGORIA
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nome',
    )

    search_fields = ('nome',)

    ordering = ('nome',)


# 📦 PRODUTO
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nome',
        'categoria',
        'preco',
        'estoque',
        'peso',
        'ativo'
    )

    list_display_links = ('id', 'nome')

    list_filter = (
        'ativo',
        'categoria',
    )

    search_fields = (
        'nome',
        'descricao',
    )

    ordering = ('nome',)

    list_editable = (
        'preco',
        'estoque',
        'ativo',
    )

    list_per_page = 20

    fieldsets = (

        ('🛍 Produto', {
            'fields': (
                'nome',
                'descricao',
                'categoria'
            )
        }),

        ('💰 Comercial', {
            'fields': (
                'preco',
                'estoque'
            )
        }),

        ('📦 Frete', {
            'fields': (
                'peso',
                'altura',
                'largura',
                'comprimento'
            )
        }),

        ('⚙ Status', {
            'fields': (
                'ativo',
            )
        }),

        ('🖼 Imagem', {
            'fields': (
                'imagem',
            )
        }),
    )

    actions = [
        'marcar_como_ativo',
        'marcar_como_inativo'
    ]

    def marcar_como_ativo(self, request, queryset):
        queryset.update(ativo=True)
    marcar_como_ativo.short_description = "Ativar produtos selecionados"

    def marcar_como_inativo(self, request, queryset):
        queryset.update(ativo=False)
    marcar_como_inativo.short_description = "Desativar produtos selecionados"


# 🎯 BANNER
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'ativo',
    )

    list_filter = ('ativo',)

    ordering = ('id',)

    fieldsets = (
        ('🖼 Banner', {
            'fields': ('imagem', 'ativo')
        }),
    )


# 📦 ITENS DO PEDIDO
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0

    readonly_fields = (
        'produto',
        'preco',
        'quantidade'
    )

    can_delete = False


# 🧾 PEDIDOS
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nome_cliente',
        'telefone',
        'cidade',
        'total',
        'status',
        'mercadopago_id',
        'criado_em'
    )

    list_filter = (
        'status',
        'cidade',
        'criado_em'
    )

    search_fields = (
        'id',
        'nome_cliente',
        'telefone',
        'cidade',
        'mercadopago_id'
    )

    readonly_fields = (
        'criado_em',
        'total',
        'mercadopago_id'
    )

    fieldsets = (

        ('🧾 Pedido', {
            'fields': (
                'usuario',
                'status',
                'total',
                'mercadopago_id',
                'criado_em'
            )
        }),

        ('📦 Dados de Entrega', {
            'fields': (
                'nome_cliente',
                'telefone',
                'cep',
                'cidade',
                'endereco',
                'numero',
                'complemento'
            )
        }),

        ('🚚 Frete', {
            'fields': (
                'valor_frete',
                'tipo_frete',
                'prazo_entrega'
            )
        }),

    )

    inlines = [ItemPedidoInline]