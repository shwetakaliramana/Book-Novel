from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:book_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/confirmed/', views.OrderConfirmedView.as_view(), name='order_confirmed'),
]
