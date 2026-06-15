from django.db import models
from django.contrib.auth.models import User


# 📁 CATEGORIA
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='categorias/')

    def __str__(self):
        return self.nome


# 📦 PRODUTO
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()

    # 📦 Dados para cálculo de frete
    peso = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1.00
    )

    altura = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=20.00
    )

    largura = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=20.00
    )

    comprimento = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=20.00
    )

    ativo = models.BooleanField(default=True)

    imagem = models.ImageField(
        upload_to='produtos/',
        null=True,
        blank=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='produtos',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome


# 🎯 BANNER
class Banner(models.Model):
    imagem = models.ImageField(upload_to='banners/')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Banner {self.id}"


# 🧾 PEDIDO
class Pedido(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    # 🆔 ID do pagamento Mercado Pago
    mercadopago_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # 📦 DADOS ENTREGA
    nome_cliente = models.CharField(
        max_length=150,
        blank=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    cep = models.CharField(
        max_length=20,
        blank=True
    )

    cidade = models.CharField(
        max_length=100,
        blank=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True
    )

    numero = models.CharField(
        max_length=20,
        blank=True
    )

    complemento = models.CharField(
        max_length=255,
        blank=True
    )

    # 🚚 FRETE
    valor_frete = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    tipo_frete = models.CharField(
        max_length=100,
        blank=True
    )

    prazo_entrega = models.IntegerField(
        null=True,
        blank=True
    )

    codigo_frete = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"


# 📦 ITENS DO PEDIDO
class ItemPedido(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantidade = models.IntegerField()

    def __str__(self):
        return f"{self.produto.nome} ({self.quantidade})"

# 🔐 TOKEN MELHOR ENVIO
class MelhorEnvioToken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Token Melhor Envio"