from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('create/', views.create_item, name='create_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]