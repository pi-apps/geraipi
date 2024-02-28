from django.urls import include, path
from rest_framework import routers

from apidata.viewsets.auth_viewset import (
    GroupViewSet,
    MeViewSet,
    RegisterUserAPIView,
    UserAuthToken,
    UserViewSet,
)
from apidata.viewsets.produks_viewset import (
    GambarProdukViewset,
    KategoriViewset,
    ProdukViewSet,
    TipeProdukViewset,
    WarnaProdukViewset,
)
from apidata.viewsets.slides_viewset import SlidesViewSet
from apidata.viewsets.stores_viewset import UserStoreAddressViewset, UserStoreViewset
from apidata.viewsets.ulasan_viewset import UlasanViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"slides", SlidesViewSet)
router.register(r"produks", ProdukViewSet)
router.register(r"tipes", TipeProdukViewset)
router.register(r"kategoris", KategoriViewset)
router.register(r"warnas", WarnaProdukViewset)
router.register(r"gambarproduks", GambarProdukViewset)
router.register(r"stores", UserStoreViewset)
router.register(r"storeaddres", UserStoreAddressViewset)
router.register(r"ulasanproduk", UlasanViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("login", UserAuthToken.as_view()),
    path("register", RegisterUserAPIView.as_view()),
    path("me", MeViewSet.as_view()),
]
