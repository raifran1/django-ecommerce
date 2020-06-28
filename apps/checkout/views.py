from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from ..checkout.forms import OrderForm
from ..checkout.models import CartItem, Order
from ..produto.models import Product

# cria o carrinho de compras
class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])

        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(self.request.session.session_key, product)

        if created:
            messages.success(self.request, 'Produto adicionado com Sucesso')
        else:
            messages.success(self.request, 'Carrinho Atualizado')

        return reverse('cart')


# adicionar produtos / atualizar carrinho
class CartItemView(TemplateView):
    template_name = 'checkout/cart.html'

    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(CartItem, fields=('quantity',), can_delete=True, extra=0)
        session_key = self.request.session.session_key

        if session_key:
            if clear:
                formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key))
            else:
                formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key), data=self.request.POST or None)
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())

        return formset

    def get_context_data(self, **kwargs):

        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        context['carrinho'] = True

        session_key = self.request.session.session_key
        cart_itens = CartItem.objects.filter(cart_key=session_key)

        # calcula total
        total = 0
        for item in cart_itens:
            quant = item.quantity
            price = item.price
            total += quant * price
        context['total'] = total

        return context

    def post(self, request, *args, **kwargs):
        session_key = request.session.session_key
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)

        if formset.is_valid:
            formset.save()
            context['formset'] = self.get_formset(clear=True)

            if session_key and CartItem.objects.filter(cart_key=session_key).exists():
                messages.success(request, 'Carrinho Atualizado com Sucesso!')

        cart_itens = CartItem.objects.filter(cart_key=session_key)
        # calcula total
        total = 0
        for item in cart_itens:
            quant = item.quantity
            price = item.price
            total += quant * price
        context['total'] = total

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        session_key = request.session.session_key

        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            context['carrinho'] = True
        else:
            context['carrinho'] = False

        return self.render_to_response(context)


# finalizar compra
@login_required
def checkout_cart(request):
    session_key = request.session.session_key
    user = request.user
    cart_itens = CartItem.objects.filter(cart_key=session_key)
    if session_key and CartItem.objects.filter(cart_key=session_key).exists():
        form = OrderForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            order = Order.objects.create_order(
                user=request.user, cart_itens=cart_itens,
                endereco=f.endereco, logradouro=f.logradouro, cep=f.cep, numero=f.numero)
            cart_itens.delete()
            return redirect('pedidos')
        else:
            form = OrderForm()
    else:
        return redirect('cart')
    return render(request, 'checkout/checkout.html', locals())

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'checkout/order.html', locals())