from django.db import models
from dvadmin.utils.models import CoreModel


class RunBladePrice(CoreModel):
    """
    三角洲跑刀跑手价格台账
    """
    TYPE_CHOICES = (
        ("跑刀", "跑刀"),
        ("跑手", "跑手"),
    )
    business_type = models.CharField(max_length=20, verbose_name="业务类型", choices=TYPE_CHOICES)
    
    GRID_CHOICES = (
        ("9格", "9格"),
        ("6格", "6格"),
        ("4格", "4格"),
        ("2格", "2格"),
        ("4-6格", "4-6格"),
    )
    grid_type = models.CharField(max_length=20, verbose_name="物品格子", choices=GRID_CHOICES)
    
    unit_price = models.CharField(max_length=50, verbose_name="单人单价(R)", blank=True, null=True)
    rmb = models.FloatField(verbose_name="人民币R", default=0)
    game_money = models.CharField(max_length=50, verbose_name="对应游戏币", blank=True, null=True)
    remark = models.CharField(max_length=200, verbose_name="备注说明", blank=True, null=True)

    class Meta:
        verbose_name = "三角洲跑刀跑手价格"
        verbose_name_plural = "三角洲跑刀跑手价格"
        ordering = ["business_type", "grid_type"]

    def __str__(self):
        return f"{self.business_type}-{self.grid_type}-{self.unit_price}R"
