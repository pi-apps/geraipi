from rest_framework import serializers

from produk.models import Cart, UlasanCart


class UlasanSerializer(serializers.HyperlinkedModelSerializer):
    cart = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = UlasanCart
        fields = [
            "url",
            "user",
            "cart",
            "catatan",
            "produkitem",
            "produk",
            "created_at",
        ]

    def get_cart(self, obj):
        carts = Cart.objects.filter(pk=obj.cart.id)
        carts = carts.first()
        return carts.kode

    def get_user(self, obj):
        user = Cart.objects.filter(pk=obj.cart.id)
        user = user.first()
        user = user.user
        user = user.username
        return user
