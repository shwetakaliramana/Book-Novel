from django.urls import path
from .views import CheckoutView, OrderConfirmedView, dashboard_view, ReadBookView, AddToCartView, RemoveFromCartView, CartDetailView, AddToWishlistView, RemoveFromWishlistView, WishlistDetailView, UpdateCartQuantityView, OrderHistoryView

urlpatterns = [
    path('dashboard/', dashboard_view, name='admin_dashboard'),
    path('read/<int:book_id>/', ReadBookView.as_view(), name='read_book'),
    path('cart/add/<int:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update/<int:item_id>/', UpdateCartQuantityView.as_view(), name='update_cart_quantity'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/confirmed/', OrderConfirmedView.as_view(), name='order_confirmed'),
    path('orders/history/', OrderHistoryView.as_view(), name='order_history'),
    path('wishlist/add/<int:book_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('wishlist/', WishlistDetailView.as_view(), name='wishlist_detail'),
    
]
