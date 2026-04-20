from dvadmin.utils.serializers import CustomModelSerializer
from escortprice.models import EscortPrice


class EscortPriceSerializer(CustomModelSerializer):
    """护航价格序列化器"""

    class Meta:
        model = EscortPrice
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EscortPriceListSerializer(CustomModelSerializer):
    """护航价格列表序列化器"""

    class Meta:
        model = EscortPrice
        fields = '__all__'
