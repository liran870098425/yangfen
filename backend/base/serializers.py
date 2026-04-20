# -*- coding: utf-8 -*-
"""
author:码同学 极光
date:2025/5/17
desc: 
sample: 
"""
import json

from rest_framework import serializers

from base.models import ProjectInfo, ModuleInfo
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.string_util import is_json


class ProjectInfoSerializer(CustomModelSerializer):
    class Meta:
        model = ProjectInfo
        fields = '__all__'

class ModuleInfoSerializer(CustomModelSerializer):
    class Meta:
        model = ModuleInfo
        fields = '__all__'



