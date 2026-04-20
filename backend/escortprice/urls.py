from django.urls import path
from rest_framework.routers import DefaultRouter

from escortprice.views import EscortPriceViewSet

router = DefaultRouter()
router.register(r'escortprice', EscortPriceViewSet)

urlpatterns = []
urlpatterns += router.urls
