from django.db import models
from dvadmin.utils.models import CoreModel


class EscortPrice(CoreModel):
    """
    三角洲护航价格台账
    """
    PACKAGE_TYPE_CHOICES = (
        ("体验单", "体验单"),
        ("绝密监狱航天", "绝密监狱航天"),
        ("绝密巴克什", "绝密巴克什"),
        ("赌约单", "赌约单"),
    )
    package_type = models.CharField(max_length=50, verbose_name="套餐类型", choices=PACKAGE_TYPE_CHOICES)
    package_name = models.CharField(max_length=200, verbose_name="套餐名称")
    sell_price = models.FloatField(verbose_name="出售价格(R)", default=0)
    guarantee_money = models.FloatField(verbose_name="保底游戏币(w)", default=0)
    bomb_extra = models.FloatField(verbose_name="炸单额外加(w)", default=0)
    game_times = models.CharField(max_length=50, verbose_name="对局场次", blank=True, null=True)
    remark = models.CharField(max_length=200, verbose_name="套餐备注", blank=True, null=True)

    class Meta:
        verbose_name = "三角洲护航价格"
        verbose_name_plural = "三角洲护航价格"
        ordering = ["package_type", "sell_price"]

    def __str__(self):
        return f"{self.package_type}-{self.package_name}-{self.sell_price}R"
