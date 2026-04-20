from django.urls import path
from rest_framework.routers import DefaultRouter
from itemprice.views import ItemPriceViewSet

router = DefaultRouter()
router.register('itemprice', ItemPriceViewSet, basename='itemprice')

urlpatterns = []
urlpatterns += router.urls
