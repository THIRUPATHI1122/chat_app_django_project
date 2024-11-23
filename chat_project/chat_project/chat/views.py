from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message
import json
from django.http import JsonResponse


# User Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Create a new user
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'chat/member_register.html')


# User Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('member_list')
        else:
            return render(request, 'chat/member_login.html', {'error': 'Invalid credentials'})
    return render(request, 'chat/member_login.html')


# User Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# List of Members View
@login_required
def member_list(request):
    # Exclude the logged-in user from the list
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat/member_list.html', {'users': users})


# Private Chat View
@login_required
def private_chat(request, username):
    recipient = get_object_or_404(User, username=username)

    if request.method == 'POST':
        # Handle new message submission via AJAX
        data = json.loads(request.body)
        content = data.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)

    # Fetch all messages between the logged-in user and the recipient
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)
    ).order_by('timestamp')

    return render(request, 'chat/private_message.html', {'recipient': recipient, 'messages': messages})

# Chat History View
@login_required
def chat_history(request, username):
    # Get the recipient user object or 404 if not found
    recipient = get_object_or_404(User, username=username)

    # Fetch messages between the logged-in user and the recipient
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)
    ).order_by('timestamp')

    # Render the message history template with messages
    return render(request, 'chat/private_message_history.html', {
        'messages': messages,
        'recipient': recipient,
    })
