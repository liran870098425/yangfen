from django.urls import path
from rest_framework.routers import DefaultRouter

from runbladeprice.views import RunBladePriceViewSet

router = DefaultRouter()
router.register(r'runbladeprice', RunBladePriceViewSet)

urlpatterns = []
urlpatterns += router.urls
