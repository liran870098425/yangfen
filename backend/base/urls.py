# -*- coding: utf-8 -*-
"""
author:码同学 极光
date:2025/5/17
desc: 
sample: 
"""
from rest_framework.routers import SimpleRouter

from base.views import ProjectInfoView, ModuleInfoView

router = SimpleRouter()
# router.register("base/envInfo", EnvInfoView)
router.register("base/projectInfo", ProjectInfoView)
router.register("base/moduleInfo", ModuleInfoView)

urlpatterns = [
]
urlpatterns += router.urls