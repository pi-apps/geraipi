from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.views.base_view import FrontPage
from produk.models import Cart, CartItem, Produk


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class AddToCartAppend(FrontPage):
    def get(self, request, id):
        produk = Produk.objects.get(pk=id)
        cart = Cart.objects.filter(user=request.user.id, status=1)
        cart = cart.first()
        if not cart:
            cart = Cart.objects.create(user=request.user, status=1)
            cart.save()

        cart_item = CartItem.objects.create(cart=cart, produk=produk)
        cart_item.save()
        return JsonResponse({"status": True})
