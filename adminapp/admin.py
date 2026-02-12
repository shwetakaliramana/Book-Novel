from django.contrib import admin
from .models import Author, Category, Era, Book, BookRating, BookReview, Cart, CartItem, Order, Brand, Wishlist

# Brand
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ["name"]
	list_display = ("name", "slug")

# Wishlist
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
	list_display = ("user", "book", "added_at")
	search_fields = ("user__username", "book__title")

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'created_at', 'checked_out')
	list_filter = ('checked_out',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'cart', 'book', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'cart', 'placed_at', 'status')
	list_filter = ('status',)
@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
	list_display = ("book", "user", "created_at", "is_approved", "review")
	search_fields = ("book__title", "user__username", "review")
	list_filter = ("book", "user", "is_approved")
@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
	list_display = ("book", "user", "rating", "created_at")
	search_fields = ("book__title", "user__username")

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ["name"]
	list_display = ("name", "slug")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ["name"]
	list_display = ("name", "slug")

@admin.register(Era)
class EraAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	search_fields = ["name"]
	list_display = ("name", "slug")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ["title", "author__name", "category__name"]
	list_display = ("title", "author", "category", "era", "status", "created_at")
	list_filter = ("status", "category", "era", "author")
	readonly_fields = ("created_at", "updated_at")
