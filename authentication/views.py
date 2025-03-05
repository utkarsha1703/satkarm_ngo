from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from gfg import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail, EmailMessage
from . tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def home(request):
    return render(request, "authentication/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "")  
        fname = request.POST.get("fname", "")  # Default to empty string if missing
        lname = request.POST.get("lname", "")
        email = request.POST.get("email", "")
        pass1 = request.POST.get('pass1',"")
        pass2 = request.POST.get('pass2',"")
        
        print("Username:", username)
        print("First Name:", fname)
        print("Last Name:", lname)
        print("Email:", email)
        print('Password:', pass1)
        print('Password:', pass2)

        # ✅ Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, " Username already taken. Please choose a different one.")
            return redirect('register')

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, " Email is already registered. Try logging in.")
            return redirect('register')

        # ✅ Check if passwords match
        if pass1 != pass2:
            messages.error(request, "❌ Passwords do not match!")
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers.")
            return redirect('register')

        # ✅ Create a new user
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, "✅ Your account has been successfully created. We have sent  you a confirmation email, please confirm your email adderss in order to activate your account.")

        #wlc email

        subject = 'Welcome to Satkarma'
        message = "Hello" +myuser.first_name + "!! \n" + "Welcome to Satkarma. Thank you for visiting our website. \n We have also send your a confirmation email, please confirm your email adderss in order to activate your account. \n\n Thanking you "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(
            subject, 
            message, 
            from_email, 
            to_list,  
            fail_silently=True  # ✅ Corrected placement
)

 
        # Email Adderee Confirmation email.

    current_site = get_current_site(request)
    email_subject = "Confirm your email."
    message2 = render_to_string('email confirmation.html', {
        'name': myuser.first_name,
        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        'tokens' : generate_token.make_token(myuser)
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
    )
    email.fail_silently = True
    email.send()

    
    return redirect('signin')
    return render(request, "authentication/register.html",)

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, username=username, password=pass1)  
        print(f"Authenticated User: {user}")

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Invalid Credentials, Please try again.")
            return redirect('signin')

    return render(request, "authentication/signin.html")   

def signout(request):
    logout(request)
    messages.success(request, " logged out successfully.")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Congratulations! Your account has been activated.")
        return redirect('home')
    else:
        return render(request, 'authentication/activation_failed.html')