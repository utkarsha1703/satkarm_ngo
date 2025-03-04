from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # ✅ Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Username already taken. Please choose a different one.")
            return redirect('register')

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "❌ Email is already registered. Try logging in.")
            return redirect('register')

        # ✅ Check if passwords match
        if pass1 != pass2:
            messages.error(request, "❌ Passwords do not match!")
            return redirect('register')

        # ✅ Create a new user
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "✅ Your account has been successfully created.")
        return redirect('signin')

    return render(request, "authentication/register.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Invalid Credentials, Please try again.")
            return redirect('home')

    return render(request, "authentication/signin.html")   

def signout(request):
    logout(request)
    messages.success(request, " logged out successfully.")
    return redirect('home')