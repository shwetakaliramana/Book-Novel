from django.db import models
from django.contrib.auth.models import User

class UserActivity(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
	action = models.CharField(max_length=100)
	book = models.ForeignKey('adminapp.Book', on_delete=models.SET_NULL, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f"{self.user.username} {self.action} {self.book if self.book else ''} at {self.timestamp}"
from django.db import models


from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(blank=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	is_verified = models.BooleanField(default=False)
	otp_code = models.CharField(max_length=6, blank=True, null=True)
	otp_created = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return f"Profile: {self.user.username}"
