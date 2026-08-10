from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Produto, Categoria, Banner, Pedido, ItemPedido

# 1. REMOVE GRUPOS E USUÁRIOS
admin.site.unregister(Group)
admin.site.unregister(User)

# 2. INLINES
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('produto', 'preco', 'quantidade')

# 3. ADMIN CONFIGURATIONS
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('exibir_nome',)
    
    def exibir_nome(self, obj): return obj.nome
    exibir_nome.short_description = "" # Sem título
    
    def get_actions(self, request): return None

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Removido o 'destaque_home' daqui:
    list_display = ('nome', 'preco', 'estoque', 'ativo')
    list_editable = ('ativo',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('ativo_exibicao',)
    
    def ativo_exibicao(self, obj): return obj.ativo
    ativo_exibicao.short_description = "Ativo"
    
    def get_actions(self, request): return None

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente_exibicao', 'status_exibicao', 'total_exibicao', 'data_exibicao')
    inlines = [ItemPedidoInline]
    
    def cliente_exibicao(self, obj): return obj.nome_cliente
    cliente_exibicao.short_description = "Cliente"
    
    def status_exibicao(self, obj): return obj.status
    status_exibicao.short_description = "Status"
    
    def total_exibicao(self, obj): return obj.total
    total_exibicao.short_description = "Total"
    
    def data_exibicao(self, obj): return obj.criado_em
    data_exibicao.short_description = "Data"
    
    def get_actions(self, request): return None