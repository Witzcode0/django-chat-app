from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from apps.users.models import chatUser
from functools import wraps
import re


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.error(request, "Please login first.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

def register_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # 🔹 Basic Required Validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect("register")

        # 🔹 Username unique check
        if chatUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # 🔹 Email unique check
        if chatUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # 🔹 Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # 🔹 Password strength validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("register")

        if not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect("register")

        if not re.search(r"[0-9]", password):
            messages.error(request, "Password must contain at least one number.")
            return redirect("register")

        # 🔹 Create user with hashed password
        chatUser.objects.create(
            username=username,
            email=email,
            bio=bio,
            password=make_password(password)
        )

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "register.html")

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "All fields are required.")
            return redirect("login")

        try:
            user = chatUser.objects.get(username=username)
        except chatUser.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

        # 🔐 Check hashed password
        if not check_password(password, user.password):
            messages.error(request, "Invalid username or password.")
            return redirect("login")

        # ✅ Store user in session
        request.session["user_id"] = str(user.id)
        request.session["username"] = user.username

        messages.success(request, "Login successful!")
        return redirect("dashboard")  # change as needed

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("login")

def get_logged_in_user(request):
    user_id = request.session.get("user_id")
    if user_id:
        return chatUser.objects.filter(id=user_id).first()
    return None

@login_required_custom
def dashboard_view(request):
    return render(request, "dashboard.html")

@login_required_custom
def profile_view(request):
    user = get_logged_in_user(request)
    return render(request, "profile.html", {"user": user})