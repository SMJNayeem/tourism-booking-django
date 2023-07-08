from django.shortcuts import render
from django.http import HttpResponse


# def registration(request):
#     return render(request, "accounts/register.html")


# def login(request):
#     return render(request, "accounts/login.html")


from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from .models import User, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from cart.models import Cart, CartItem
# from cart.views import _cart_id
import requests

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # username = email.split("@")[0]

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.username = username
            user.save()

            # User Activation

            # current_site = get_current_site(request)
            mail_subject = "Please activate your account. "
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": "http://127.0.0.1:8000",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Registration Successful")

            return redirect("accounts/login/?command-verification&email-" + email)
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


def loginUser(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)
        user.save()

        if user is not None:
            try:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect("homePage")
            except:
                messages.error(request, "Wrong Credentials")
        else:
            messages.error(request, "Invalid login credientials.")
            return redirect("login")

    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    messages.success(request, "You are logged out.")

    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


# @login_required(login_url="loginUser")
# def dashboard(request):
#     return render(request, "accounts/dashboard.html")


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = "Reset your Password. "
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, "Password reset mail has been sent to your emaill address"
            )
            return redirect("login")

        else:
            messages.error(request, "Account does not exists. ")
            return redirect("forgotPassword")

    return render(request, "accounts/forgotPassword.html")


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Reset your password.")
        return redirect("resetPassword")
    else:
        messages.error(request, "This link has been expired. ")
        return redirect("login")


def resetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()

            messages.success(request, "Password reset successfully. ")
            return redirect("login")
        else:
            messages.error(request, "Password does not match")
            return redirect("resetPassword")
    else:
        return render(request, "accounts/resetPassword.html")


# @login_required
# def profileUpdate(request):
#     profile = get_object_or_404(UserProfile, user=request.user)
#     return redirect("profile", profile.user.username)
