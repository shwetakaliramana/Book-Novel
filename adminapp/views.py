from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Book, Cart, CartItem, Order, Wishlist

class OrderHistoryView(LoginRequiredMixin, View):
	def get(self, request):
		orders = Order.objects.filter(user=request.user).order_by('-placed_at').select_related('cart')
		return render(request, 'adminapp/order_history.html', {'orders': orders})
# Update Cart Quantity
class UpdateCartQuantityView(LoginRequiredMixin, View):
	def post(self, request, item_id):
		item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__checked_out=False)
		try:
			quantity = int(request.POST.get('quantity', 1))
			if quantity < 1:
				item.delete()
				messages.info(request, 'Item removed from cart.')
			else:
				# Prevent adding more than available stock
				if quantity > item.book.stock:
					messages.error(request, f'Only {item.book.stock} in stock.')
					quantity = item.book.stock
				item.quantity = quantity
				item.save()
				messages.success(request, 'Cart updated.')
		except Exception:
			messages.error(request, 'Invalid quantity.')
		return redirect('cart_detail')

from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Book, Cart, CartItem, Order, Wishlist
# Add to Wishlist
class AddToWishlistView(LoginRequiredMixin, View):
	def post(self, request, book_id):
		book = get_object_or_404(Book, id=book_id)
		Wishlist.objects.get_or_create(user=request.user, book=book)
		messages.success(request, f'Added {book.title} to wishlist.')
		return redirect('wishlist_detail')

# Remove from Wishlist
class RemoveFromWishlistView(LoginRequiredMixin, View):
	def post(self, request, book_id):
		wishlist_item = get_object_or_404(Wishlist, user=request.user, book_id=book_id)
		wishlist_item.delete()
		messages.info(request, 'Item removed from wishlist.')
		return redirect('wishlist_detail')

# Wishlist Page
class WishlistDetailView(LoginRequiredMixin, View):
	def get(self, request):
		wishlist_items = Wishlist.objects.filter(user=request.user).select_related('book')
		return render(request, 'adminapp/wishlist.html', {'wishlist_items': wishlist_items})

# Read Book Online
class ReadBookView(LoginRequiredMixin, View):
	def get(self, request, book_id):
		book = get_object_or_404(Book, id=book_id)
		if not book.pdf_file:
			messages.error(request, 'No PDF available for this book.')
			return redirect('book_detail', slug=book.slug)
		# Optional: limit preview for free users (example: first 5 pages)
		# For now, show full PDF to logged-in users
		return render(request, 'adminapp/read_book.html', {'book': book})

# Add to Cart
class AddToCartView(LoginRequiredMixin, View):
	def post(self, request, book_id):
		book = get_object_or_404(Book, id=book_id)
		cart, created = Cart.objects.get_or_create(user=request.user, checked_out=False)
		item, created = CartItem.objects.get_or_create(cart=cart, book=book)
		if not created:
			item.quantity += 1
			item.save()
		messages.success(request, f'Added {book.title} to cart.')
		return redirect('cart_detail')

# Remove from Cart
class RemoveFromCartView(LoginRequiredMixin, View):
	def post(self, request, item_id):
		item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__checked_out=False)
		item.delete()
		messages.info(request, 'Item removed from cart.')
		return redirect('cart_detail')

# Cart Page
class CartDetailView(LoginRequiredMixin, View):
	def get(self, request):
		cart = Cart.objects.filter(user=request.user, checked_out=False).first()
		items = cart.items.select_related('book') if cart else []
		total = sum(item.book.price * item.quantity for item in items) if cart else 0
		item_count = sum(item.quantity for item in items) if cart else 0
		return render(request, 'adminapp/cart_detail.html', {
			'cart': cart,
			'items': items,
			'total': total,
			'item_count': item_count
		})

# Checkout (Place Order)
class CheckoutView(LoginRequiredMixin, View):
	def post(self, request):
			cart = Cart.objects.filter(user=request.user, checked_out=False).first()
			if not cart or not cart.items.exists():
				messages.error(request, 'Your cart is empty.')
				return redirect('cart_detail')

			# Update inventory for each item
			for item in cart.items.select_related('book'):
				if item.quantity > item.book.stock:
					messages.error(request, f'Not enough stock for {item.book.title}.')
					return redirect('cart_detail')
			for item in cart.items.select_related('book'):
				item.book.stock -= item.quantity
				item.book.save()

			cart.checked_out = True
			cart.save()
			order = Order.objects.create(user=request.user, cart=cart, status='completed')

			# Send order confirmation email
			from userapp.emails import send_order_confirmation_email
			send_order_confirmation_email(request.user, order)

			# Optionally clear cart items (if you want to keep order history, keep them attached to order)
			# cart.items.all().delete()

			messages.success(request, 'Order placed successfully!')
			return redirect('order_confirmed')

# Order Confirmed
class OrderConfirmedView(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'adminapp/order_confirmed.html')

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from adminapp.models import Book, Author, Category

@staff_member_required
def dashboard_view(request):
	total_books = Book.objects.count()
	total_authors = Author.objects.count()
	total_categories = Category.objects.count()
	recent_books = Book.objects.order_by('-created_at')[:5]

	# Analytics: most viewed books, most active users
	from userapp.models import UserActivity
	from django.db.models import Count
	most_viewed_books = (
		UserActivity.objects.filter(action='viewed', book__isnull=False)
		.values('book__title')
		.annotate(view_count=Count('id'))
		.order_by('-view_count')[:5]
	)
	most_active_users = (
		UserActivity.objects.values('user__username')
		.annotate(action_count=Count('id'))
		.order_by('-action_count')[:5]
	)

	return render(request, 'adminapp/dashboard.html', {
		'total_books': total_books,
		'total_authors': total_authors,
		'total_categories': total_categories,
		'recent_books': recent_books,
		'most_viewed_books': most_viewed_books,
		'most_active_users': most_active_users,
	})


