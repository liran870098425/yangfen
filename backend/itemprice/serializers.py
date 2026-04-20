from dvadmin.utils.serializers import CustomModelSerializer
from itemprice.models import ItemPrice


class ItemPriceSerializer(CustomModelSerializer):
    """物品价格序列化器"""

    class Meta:
        model = ItemPrice
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ItemPriceListSerializer(CustomModelSerializer):
    """物品价格列表序列化器"""

    class Meta:
        model = ItemPrice
        fields = '__all__'
