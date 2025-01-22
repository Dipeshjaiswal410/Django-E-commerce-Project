from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),  # Keep this line
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/<int:quantity>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create_order/', views.create_order, name='create_order'),
    # Product APIs
    path('api/products/', views.product_list, name='api_product_list'),
    path('api/products/<int:pk>/', views.product_detail, name='api_product_detail'),
    
    # Cart APIs
    path('api/cart/', views.cart_view, name='api_cart'),
    
    # Order APIs
    path('api/orders/', views.create_order, name='api_create_order'),
    path('api/orders/list/', views.order_list, name='api_order_list'),
]