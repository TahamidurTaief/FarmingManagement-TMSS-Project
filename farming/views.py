# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from app.models import CustomUser
from django.core.files.storage import default_storage  # For handling file uploads
from django.contrib.auth import authenticate, login
from django.contrib import messages






def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if a profile picture was uploaded
        profile_picture = request.FILES.get('profile_picture')

        # Validate if the user already exists by email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        # Create a new user
        try:
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                phone_number=phone_number,
                first_name=name,
                is_staff=False  # Correct field for staff status
            )

            # Handle profile picture upload if provided
            if profile_picture:
                user.profile_picture.save(profile_picture.name, profile_picture)

            user.save()

            # Authenticate and log in the user after successful signup
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the dashboard or home page

        except Exception as e:
            messages.error(request, f'Error creating account: {e}')
            return redirect('signup')

    return render(request, 'pages/signup.html')







# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to dashboard or another view
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'pages/login.html')





# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
