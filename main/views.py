
from django.shortcuts import render, get_object_or_404
from django.views import View
from adminapp.models import Book, Category, Author, Era
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg

# Product detail view
class BookDetailView(DetailView):
	model = Book
	template_name = 'book_detail.html'
	context_object_name = 'book'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['images'] = self.object.images.all()
		context['reviews'] = self.object.reviews.filter(is_approved=True)
		return context

class PrivacyView(View):
	def get(self, request):
		context = get_common_context()
		return render(request, 'privacy.html', context)

class ContactView(View):
	def get(self, request):
		context = get_common_context()
		return render(request, 'contact.html', context)

class AboutView(View):
	def get(self, request):
		context = get_common_context()
		return render(request, 'about.html', context)

def get_common_context():
	return {
		'categories': Category.objects.all(),
		'authors': Author.objects.all(),
		'eras': Era.objects.all(),
	}

class HomeView(ListView):
	model = Book
	template_name = 'home.html'
	context_object_name = 'new_books'
	paginate_by = 8

	def get_queryset(self):
		queryset = Book.objects.order_by('-created_at')
		category = self.request.GET.get('category')
		author = self.request.GET.get('author')
		min_price = self.request.GET.get('min_price')
		max_price = self.request.GET.get('max_price')
		brand = self.request.GET.get('brand')
		if category:
			queryset = queryset.filter(category__slug=category)
		if author:
			queryset = queryset.filter(author__slug=author)
		if brand:
			queryset = queryset.filter(brand__slug=brand)
		if min_price:
			queryset = queryset.filter(price__gte=min_price)
		if max_price:
			queryset = queryset.filter(price__lte=max_price)
		return queryset[:8]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_common_context())
		context['featured_books'] = Book.objects.filter(status='featured')[:5]
		context['trending_books'] = Book.objects.filter(status='trending')[:8]
		from adminapp.models import Brand
		context['brands'] = Brand.objects.all()
		return context

class CategoryBooksView(ListView):
	model = Book
	template_name = 'category.html'
	context_object_name = 'books'
	paginate_by = 8

	def get_queryset(self):
		self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
		return Book.objects.filter(category=self.category)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_common_context())
		context['category'] = self.category
		return context

class AuthorBooksView(ListView):
	model = Book
	template_name = 'category.html'
	context_object_name = 'books'
	paginate_by = 8

	def get_queryset(self):
		self.author = get_object_or_404(Author, slug=self.kwargs['slug'])
		return Book.objects.filter(author=self.author)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_common_context())
		context['category'] = self.author
		return context

class EraBooksView(ListView):
	model = Book
	template_name = 'category.html'
	context_object_name = 'books'
	paginate_by = 8

	def get_queryset(self):
		self.era = get_object_or_404(Era, slug=self.kwargs['slug'])
		return Book.objects.filter(era=self.era)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_common_context())
		context['category'] = self.era
		return context

class BookDetailView(DetailView):
	model = Book
	template_name = 'book_detail.html'
	context_object_name = 'book'

	def get_object(self):
		book = get_object_or_404(Book, slug=self.kwargs['slug'])
		# Track user activity for book view
		if self.request.user.is_authenticated:
			from userapp.models import UserActivity
			UserActivity.objects.create(user=self.request.user, action='viewed', book=book)
		return book

	def post(self, request, *args, **kwargs):
		from .forms import BookRatingForm, BookReviewForm
		self.object = self.get_object()
		rating_form = BookRatingForm(request.POST)
		review_form = BookReviewForm(request.POST)
		if request.user.is_authenticated:
			if 'rating' in request.POST:
				if rating_form.is_valid():
					self.object.ratings.update_or_create(
						user=request.user,
						defaults={'rating': rating_form.cleaned_data['rating']}
					)
			if 'review' in request.POST:
				if review_form.is_valid():
					self.object.reviews.create(
						user=request.user,
						review=review_form.cleaned_data['review']
					)
		return self.get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		from .forms import BookRatingForm, BookReviewForm
		context = super().get_context_data(**kwargs)
		context.update(get_common_context())
		book = self.get_object()
		# Related books: same category, exclude self
		context['related_books'] = Book.objects.filter(category=book.category).exclude(id=book.id)[:3]
		# Book rating form and average
		user_rating = None
		if self.request.user.is_authenticated:
			user_rating = book.ratings.filter(user=self.request.user).first()
		context['rating_form'] = BookRatingForm(initial={'rating': user_rating.rating if user_rating else None})
		ratings = book.ratings.all()
		context['average_rating'] = round(ratings.aggregate(Avg('rating'))['rating__avg'] or 0, 2)
		context['user_rating'] = user_rating.rating if user_rating else None
		# Book review form and reviews
		context['review_form'] = BookReviewForm()
		context['reviews'] = book.reviews.select_related('user').filter(is_approved=True)
		return context


class SearchResultsView(ListView):
	def get(self, request, *args, **kwargs):
		# Track user activity for search
		if request.user.is_authenticated:
			from userapp.models import UserActivity
			UserActivity.objects.create(user=request.user, action='searched', book=None)
		return super().get(request, *args, **kwargs)
	model = Book
	template_name = 'search_results.html'
	context_object_name = 'books'
	paginate_by = 8

	def get_queryset(self):
		query = self.request.GET.get('q', '')
		return Book.objects.filter(
			Q(title__icontains=query) |
			Q(author__name__icontains=query) |
			Q(category__name__icontains=query)
		).distinct()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_common_context())
		context['query'] = self.request.GET.get('q', '')
		return context
