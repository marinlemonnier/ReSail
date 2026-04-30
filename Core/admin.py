from django.contrib import admin
from .models import Item, Category, TradeType, Status, ItemImage

# Register your models here.kkkkk
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(TradeType)
admin.site.register(Status)
admin.site.register(ItemImage)