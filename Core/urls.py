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
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('favoris/', views.favorites_list, name='favorites_list'),
    path('item/<int:item_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('item/<int:item_id>/contact/', views.item_contact, name='item_contact'),
]