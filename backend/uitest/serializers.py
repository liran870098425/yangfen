from rest_framework import serializers
from uitest.models import BusinessRecord
from dvadmin.utils.serializers import CustomModelSerializer


class BusinessRecordSerializer(CustomModelSerializer):
    """业务数据登记序列化器"""

    class Meta:
        model = BusinessRecord
        fields = '__all__'
        read_only_fields = (
            'profit', 'monthly_receipt',
            'monthly_platform_deduct', 'monthly_cost_total', 'monthly_profit_total',
            'total_platform_deduct', 'total_cost_all', 'total_profit_all',
        )


class BusinessRecordListSerializer(CustomModelSerializer):
    """业务数据登记列表序列化器"""

    class Meta:
        model = BusinessRecord
        fields = '__all__'


class BusinessRecordStatsSerializer(serializers.Serializer):
    """统计数据序列化器"""
    total_platform_deduct = serializers.FloatField(allow_null=True)
    total_cost_deduct = serializers.FloatField(allow_null=True)
    total_profit = serializers.FloatField(allow_null=True)
    total_receipt = serializers.FloatField(allow_null=True)
