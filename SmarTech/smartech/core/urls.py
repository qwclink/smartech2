from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.product_list, name="product_list"),
    path('product/<int:pk>/', views.product_detail, name="product_detail"),
    path('add/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart_view, name='cart'),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('guestbook/', views.guestbook, name="guestbook"),
    path('admin-panel/', views.admin_panel, name="admin_panel"),
    path('edit_product/<int:pk>/', views.edit_product, name="edit_product"),
    path('delete_product/<int:pk>/', views.delete_product, name="delete_product"),
    path('delete-message/<int:pk>/', views.delete_message, name='delete_message'),
    path('logout', views.logout, name="logout"),
    path('order/create/', views.create_order, name='create_order'),
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/complete/<int:pk>/', views.complete_order, name='complete_order'),
    path('orders/cancel/<int:pk>/', views.cancel_order, name='cancel_order'),
]
