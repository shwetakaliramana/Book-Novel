from django.urls import path
from .views import (
    HomeView, CategoryBooksView, AuthorBooksView, EraBooksView, BookDetailView, SearchResultsView, AboutView, ContactView, PrivacyView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryBooksView.as_view(), name='category'),
    path('author/<slug:slug>/', AuthorBooksView.as_view(), name='author'),
    path('era/<slug:slug>/', EraBooksView.as_view(), name='era'),
    path('book/<slug:slug>/', BookDetailView.as_view(), name='book_detail'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
]
