from django.contrib import admin
from itemprice.models import ItemPrice


@admin.register(ItemPrice)
class ItemPriceAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'reference_price', 'out_price', 'item_remark', 'created_at')
    search_fields = ('item_name', 'item_remark')
    list_filter = ('created_at',)
