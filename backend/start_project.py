#!/usr/bin/env python
"""
启动 Django 项目，解决兼容性问题
"""
import sys
import os

# 添加 cgi 兼容模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'temp_cgi_fix'))

# 应用兼容性补丁
import rest_framework.serializers
if not hasattr(rest_framework.serializers, 'NullBooleanField'):
    # 创建兼容性别名
    rest_framework.serializers.NullBooleanField = rest_framework.serializers.BooleanField

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)