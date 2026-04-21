from dvadmin.utils.serializers import CustomModelSerializer
from runbladeprice.models import RunBladePrice


class RunBladePriceSerializer(CustomModelSerializer):
    """跑刀跑手价格序列化器"""

    class Meta:
        model = RunBladePrice
        fields = '__all__'
        read_only_fields = ('id', 'create_datetime', 'update_datetime')


class RunBladePriceListSerializer(CustomModelSerializer):
    """跑刀跑手价格列表序列化器"""

    class Meta:
        model = RunBladePrice
        fields = '__all__'
