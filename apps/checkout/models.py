from django.db import models

# cria as instancias do carrinho com o manager
from ..produto.models import Product


class CartItemManager(models.Manager):
    def add_item(self, cart_key, product):
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(cart_key=cart_key, product=product, price=product.price)

        return cart_item, created

# item do carrinho
class CartItem(models.Model):
    cart_key = models.CharField(u'Chave do Carrinho', max_length=50, db_index=True)
    product = models.ForeignKey('produto.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(u'Quantidade', default=1)
    price = models.DecimalField(u'Preço', decimal_places=2, max_digits=6)
    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return '{} [{}]' .format(self.product, self.quantity)

    # método para retornar o total do pedido (carrinho de compras)
    def total(self):
        aggregate_queryset = self.itens.aggregate(
            total=models.Sum(
                models.F('price') * models.F('quantity'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']


# cria o pedido de acordo com os itens do carrinho
class OrderManager(models.Manager):
    def create_order(self, user, cart_itens, endereco, logradouro, cep, numero):
        order = self.create(user=user, endereco=endereco, logradouro=logradouro, cep=cep, numero=numero)
        for cart_item in cart_itens:
            order_item = OrderItem.objects.create(order=order, quantity=cart_item.quantity, product=cart_item.product,
                                                  price=cart_item.price)
        return order

# pedido
class Order(models.Model):
    STATUS_CHOICES = (
        (1, 'Pedido Recebido'),
        (2, 'Pagamento Confirmado'),
        (3, 'Pagamento Negado'),
        (4, 'Cancelado'),
    )

    user = models.ForeignKey('auth.User', verbose_name="Usuário", on_delete=models.CASCADE, null=True, blank=True)
    endereco = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    cep = models.PositiveIntegerField()
    numero = models.PositiveIntegerField()
    status = models.IntegerField(u'Situação', choices=STATUS_CHOICES, default=1, blank=True)
    created = models.DateTimeField(u'Criado em', auto_now_add=True)

    objects = OrderManager()
    order = models.Manager()

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return 'Pedido #{}'.format(self.id)

    # método para pegar os produtos do carrinho
    def products(self):
        products_ids = self.itens.values_list('product')
        return Product.objects.filter(id__in=products_ids)

    # método para retornar o valor total do pedido (pedido feito)
    def total(self):
        aggregate_queryset = self.itens.aggregate(
            total=models.Sum(
                models.F('price') * models.F('quantity'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']

# item do pedido
class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Pedido", related_name='itens', on_delete=models.CASCADE)
    product = models.ForeignKey('produto.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(u'Quantidade', default=1)
    price = models.DecimalField(u'Preço', decimal_places=2, max_digits=6,)

    class Meta:
        verbose_name = "Item do pedido"
        verbose_name_plural = "Itens dos pedidos"

    def __str__(self):
        return '[{}] Produto: {}'.format(self.order, self.product)

    # pega o total do valor pelo item do pedido ex: [ maçãs(un: R$ 1,50) x 10 = 15,00 ]
    def total_item(self):
        return self.price * self.quantity


# post save -- exclui todos os valores cadastrados e referentes ao carrinho de compras
# da seção do usuário após ele clicar para "finalizar compra"

def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()

models.signals.post_save.connect(post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item')