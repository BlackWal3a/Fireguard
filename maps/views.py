from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CoordinateData
from django.utils import timezone
from datetime import timedelta

@csrf_exempt
def send_coordinates(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            latitude = float(data.get('latitude'))
            longitude = float(data.get('longitude'))

            # Save the data in the database
            CoordinateData.objects.create(title=title, latitude=latitude, longitude=longitude)

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

# In views.py
def landing(request):
    context = {
            'user': request.user,
        }
    return render(request, 'fireguard/landing.html', context)

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after sign-up
            return redirect('map')  # Redirect to the home page
    else:
        form = SignUpForm()
    return render(request, 'fireguard/sign_up.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Avoid KeyError with .get()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('map')  # Make sure 'map' is a valid URL name
        else:
            messages.error(request, 'Invalid username or password.')

    # If not POST or authentication fails, re-render the form
    return render(request, 'fireguard/login.html')



@login_required
def maps(request):
    # Get the username of the authenticated user
    username = request.user.username    

    # Get current time
    current_time = timezone.now()

    # Filter coordinates: keep only those sent within the last 30 minutes
    recent_coordinates = CoordinateData.objects.filter(date_sent__gte=current_time - timedelta(minutes=30))

    # Delete coordinates that are 30 minutes or older
    old_coordinates = CoordinateData.objects.filter(date_sent__lt=current_time - timedelta(minutes=30))
    old_coordinates.delete()  # Delete old coordinates from the database

    # Convert coordinates to JSON and pass to the template
    coordinates = list(recent_coordinates.values('latitude', 'longitude', 'title', 'date_sent'))
    return render(request, 'fireguard/map.html', {
        'coordinates': json.dumps(coordinates, default=str),  # JSON-serialize with default for dates
        'username': username  # Pass the username to the template
    })

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the login page (or any other page)
