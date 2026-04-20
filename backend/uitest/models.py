from django.db import models
from django.db.models import Sum
from datetime import datetime
from dvadmin.utils.models import CoreModel


class BusinessRecord(CoreModel):
    """
    业务数据登记
    """
    wechat_id = models.CharField(max_length=100, verbose_name="微信号", blank=True, null=True)
    demand = models.CharField(max_length=200, verbose_name="需求", blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="数量", blank=True, null=True)
    contact = models.CharField(max_length=100, verbose_name="联系方式", blank=True, null=True)
    collision_platform = models.CharField(max_length=100, verbose_name="撞车平台", blank=True, null=True)
    shipment_platform = models.CharField(max_length=100, verbose_name="出货平台", blank=True, null=True)
    payment_method = models.CharField(max_length=50, verbose_name="付款方式", blank=True, null=True)
    is_paid = models.BooleanField(default=False, verbose_name="是否付款")

    price_payable = models.FloatField(verbose_name="应付价格", blank=True, null=True, default=0)
    price_actual = models.FloatField(verbose_name="实付价格", blank=True, null=True, default=0)
    platform_deduct = models.FloatField(verbose_name="平台扣除", blank=True, null=True, default=0)
    cost_deduct = models.FloatField(verbose_name="成本扣除", blank=True, null=True, default=0)
    redpacket = models.FloatField(verbose_name="红包", blank=True, null=True, default=0)
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    profit = models.FloatField(verbose_name="盈余", blank=True, null=True)
    monthly_receipt = models.FloatField(verbose_name="月实收(流水)", blank=True, null=True)

    monthly_platform_deduct = models.FloatField(verbose_name="月平台总扣除", blank=True, null=True, default=0)
    monthly_cost_total = models.FloatField(verbose_name="月成本总", blank=True, null=True, default=0)
    monthly_profit_total = models.FloatField(verbose_name="月总盈余", blank=True, null=True, default=0)

    total_platform_deduct = models.FloatField(verbose_name="平台总扣除", blank=True, null=True, default=0)
    total_cost_all = models.FloatField(verbose_name="成本总", blank=True, null=True, default=0)
    total_profit_all = models.FloatField(verbose_name="总盈余", blank=True, null=True, default=0)

    record_date = models.DateField(verbose_name="业务日期", auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "业务数据登记"
        verbose_name_plural = "业务数据登记"
        ordering = ["-record_date"]

    def __str__(self):
        return f"{self.wechat_id}-{self.record_date}"

    def save(self, *args, **kwargs):
        # 计算基础公式
        self.profit = (self.price_actual or 0) - (self.platform_deduct or 0) - (self.cost_deduct or 0) + (self.redpacket or 0)
        self.monthly_receipt = (self.price_actual or 0) + (self.redpacket or 0)

        # 先保存基础数据
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

        # 更新汇总数据
        self.update_totals()

    def update_totals(self):
        """更新所有汇总字段"""
        if not self.record_date:
            return

        record_month = self.record_date.replace(day=1)
        if record_month.month == 12:
            next_month = record_month.replace(year=record_month.year + 1, month=1, day=1)
        else:
            next_month = record_month.replace(month=record_month.month + 1, day=1)

        # 按月汇总
        monthly_qs = BusinessRecord.objects.filter(
            record_date__gte=record_month,
            record_date__lt=next_month
        )

        monthly_stats = monthly_qs.aggregate(
            total_platform=Sum('platform_deduct'),
            total_cost=Sum('cost_deduct'),
            total_profit=Sum('profit')
        )

        # 全量汇总
        total_stats = BusinessRecord.objects.aggregate(
            total_platform=Sum('platform_deduct'),
            total_cost=Sum('cost_deduct'),
            total_profit=Sum('profit')
        )

        self.monthly_platform_deduct = monthly_stats['total_platform'] or 0
        self.monthly_cost_total = monthly_stats['total_cost'] or 0
        self.monthly_profit_total = monthly_stats['total_profit'] or 0

        self.total_platform_deduct = total_stats['total_platform'] or 0
        self.total_cost_all = total_stats['total_cost'] or 0
        self.total_profit_all = total_stats['total_profit'] or 0

        BusinessRecord.objects.filter(pk=self.pk).update(
            monthly_platform_deduct=self.monthly_platform_deduct,
            monthly_cost_total=self.monthly_cost_total,
            monthly_profit_total=self.monthly_profit_total,
            total_platform_deduct=self.total_platform_deduct,
            total_cost_all=self.total_cost_all,
            total_profit_all=self.total_profit_all,
        )

    @classmethod
    def update_all_totals(cls):
        """更新所有记录的汇总字段（删除记录后调用）"""
        records = cls.objects.all().order_by('record_date')
        for record in records:
            record.update_totals()

    @classmethod
    def get_monthly_summary(cls, month=None):
        """获取按月统计汇总"""
        if month:
            year, mon = map(int, month.split('-'))
            from datetime import date
            start_date = date(year, mon, 1)
            end_date = date(year, mon + 1, 1) if mon < 12 else date(year + 1, 1, 1)
            qs = cls.objects.filter(record_date__gte=start_date, record_date__lt=end_date)
        else:
            qs = cls.objects.all()

        return qs.aggregate(
            total_platform_deduct=Sum('platform_deduct'),
            total_cost_deduct=Sum('cost_deduct'),
            total_profit=Sum('profit'),
            total_receipt=Sum('monthly_receipt'),
        )
