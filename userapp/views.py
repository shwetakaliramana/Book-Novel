from django.contrib.auth import logout

from django.shortcuts import redirect
import pyttsx3 as pt
def logout_view(request):
	logout(request)
	return redirect('login')
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
def speak(text):
	engine = pt.init()
	engine.say(text)
	engine.setProperty('rate', 150)  # Adjust speech rate if needed
	engine.setProperty('volume', 0.8)  # Adjust volume if needed
	engine.setProperty('voice', 'english')  # Set voice to English
	engine.runAndWait()
@login_required
def profile_view(request):
	profile, created = UserProfile.objects.get_or_create(user=request.user)
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
	else:
		form = UserProfileForm(instance=profile)
	return render(request, 'userapp/profile.html', {'form': form, 'profile': profile})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib import messages

import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
	return str(random.randint(100000, 999999))


def register_view(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = True
			user.save()
			otp = generate_otp()
			profile, created = UserProfile.objects.get_or_create(user=user)
			profile.otp_code = otp
			profile.otp_created = timezone.now()
			profile.is_verified = False
			profile.save()
			from userapp.emails import send_welcome_email, send_otp_email
			send_welcome_email(user)
			send_otp_email(user, otp)
			request.session['pending_user_id'] = user.id
			messages.success(request, 'Registration successful! Please check your email for the OTP.')
			return redirect('otp_verify')
	else:
		form = UserRegisterForm()
	speak("Please fill out the registration form.")
	return render(request, 'userapp/register.html', {'form': form})
# OTP verification view
from django.shortcuts import render, redirect
def otp_verify_view(request):
	user_id = request.session.get('pending_user_id')
	if not user_id:
		messages.error(request, 'Session expired. Please register again.')
		return redirect('register')
	profile = UserProfile.objects.get(user_id=user_id)
	if request.method == 'POST':
		otp = request.POST.get('otp')
		if profile.otp_code == otp:
			profile.is_verified = True
			profile.otp_code = ''
			profile.save()
			del request.session['pending_user_id']
			messages.success(request, 'OTP verified! You can now log in.')
			return redirect('login')
		else:
			messages.error(request, 'Invalid OTP. Please try again.')
		speak("Thank you for registering! Please check your email for the OTP to verify your account.")
	return render(request, 'userapp/otp_verify.html')

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			# Check OTP verification
			if hasattr(user, 'profile') and not user.profile.is_verified:
				messages.error(request, 'Please verify your email with OTP before logging in.')
				request.session['pending_user_id'] = user.id
				return redirect('otp_verify')
			login(request, user)
			messages.success(request, 'Login successful!')
			return redirect('home')
	else:
		form = AuthenticationForm()
	return render(request, 'userapp/login.html', {'form': form})
