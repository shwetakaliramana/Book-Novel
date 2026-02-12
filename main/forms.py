from django import forms
from adminapp.models import BookReview, BookRating

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'})
        }

class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
        }
