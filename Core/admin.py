from django.contrib import admin
from .models import Favorite, Item, Category, TradeType, Status, ItemImage, User

# Register your models here.kkkkk
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(TradeType)
admin.site.register(Status)
admin.site.register(ItemImage)
admin.site.register(Favorite)
admin.site.register(User)