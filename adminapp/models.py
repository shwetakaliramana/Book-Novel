
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify

# Wishlist model
class Wishlist(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
	book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='wishlisted_by')
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'book')

	def __str__(self):
		return f"{self.user.username} wishes {self.book.title}"

# Brand
class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True, db_index=True)
	slug = models.SlugField(max_length=100, unique=True, blank=True)
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	def __str__(self):
		return self.name

# Multiple images for Book
class ProductImage(models.Model):
	book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='book_covers/')
	alt_text = models.CharField(max_length=255, blank=True)
	def __str__(self):
		return f"Image for {self.book.title}"

# Author
class Author(models.Model):
	name = models.CharField(max_length=255, db_index=True)
	bio = models.TextField(blank=True)
	slug = models.SlugField(max_length=255, unique=True, blank=True)
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	def __str__(self):
		return self.name

# Category
class Category(models.Model):
	name = models.CharField(max_length=100, unique=True, db_index=True)
	slug = models.SlugField(max_length=100, unique=True, blank=True)
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	def __str__(self):
		return self.name

# Era
class Era(models.Model):
	name = models.CharField(max_length=50, unique=True, db_index=True, help_text="e.g. '1810s', 'Regency Era', '1600s', 'Elizabethan Era'")
	slug = models.SlugField(max_length=50, unique=True, blank=True)
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	def __str__(self):
		return self.name

# Book
class Book(models.Model):
	STATUS_CHOICES = [
		("featured", "Featured"),
		("trending", "Trending"),
		("normal", "Normal"),
	]
	title = models.CharField(max_length=255, db_index=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
	era = models.ForeignKey(Era, on_delete=models.SET_NULL, null=True, related_name="books")
	brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
	description = models.TextField()
	cover_image = models.ImageField(upload_to="book_covers/")
	pdf_file = models.FileField(upload_to="book_pdfs/", blank=True, null=True, help_text="Upload PDF for online reading")
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="normal", db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	slug = models.SlugField(max_length=255, unique=True, blank=True)
	stock = models.PositiveIntegerField(default=0, help_text="Number of items in stock")

	class Meta:
		indexes = [
			models.Index(fields=["title"]),
			models.Index(fields=["status"]),
		]
		ordering = ["-created_at"]

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title

	@property
	def average_rating(self):
		reviews = self.reviews.filter(is_approved=True)
		if reviews.exists() and hasattr(reviews.first(), 'rating'):
			return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
		return None

# BookReview
class BookReview(models.Model):
	book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
	review = models.TextField()
	rating = models.PositiveSmallIntegerField(default=5)
	is_approved = models.BooleanField(default=False, help_text='Approve this review for public display')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['book', 'user']),
		]
	def __str__(self):
		return f"{self.user.username} review for {self.book.title}"

# BookRating
class BookRating(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_ratings')
	rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		unique_together = ('book', 'user')
		indexes = [
			models.Index(fields=['book', 'user']),
		]
	def __str__(self):
		return f"{self.user.username} rated {self.book.title}: {self.rating}"

# Cart
class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
	created_at = models.DateTimeField(auto_now_add=True)
	checked_out = models.BooleanField(default=False)
	def __str__(self):
		return f"Cart #{self.id} for {self.user.username}"

# CartItem
class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	book = models.ForeignKey('Book', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	def __str__(self):
		return f"{self.quantity} x {self.book.title}"

	@property
	def total_price(self):
		return self.book.price * self.quantity

# Order
class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
	cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
	placed_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=[('pending','Pending'),('completed','Completed')], default='pending')
	def __str__(self):
		return f"Order #{self.id} by {self.user.username}"
