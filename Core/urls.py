from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('create/', views.create_item, name='create_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.my_profile, name='my_profile'),
]