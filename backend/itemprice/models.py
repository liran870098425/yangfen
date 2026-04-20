from django.db import models
from dvadmin.utils.models import CoreModel


class ItemPrice(CoreModel):
    """
    物品价格台账
    """
    item_name = models.CharField(max_length=200, verbose_name="物资名称")
    reference_price = models.FloatField(verbose_name="参考价格", blank=True, null=True, default=0)
    out_price = models.FloatField(verbose_name="出价格", blank=True, null=True, default=0)
    item_remark = models.CharField(max_length=200, verbose_name="物品备注规格", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "物品价格台账"
        verbose_name_plural = "物品价格台账"
        ordering = ["item_name"]

    def __str__(self):
        return self.item_name
