from django.urls import path
from rest_framework import routers
from uitest.views import BusinessRecordViewSet

urlpatterns = []

router = routers.SimpleRouter()
router.register(r'uitest/business', BusinessRecordViewSet, basename='business')

urlpatterns += router.urls
