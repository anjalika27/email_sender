from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from email_sender.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login


def send_email(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        to_email = request.POST.get("to_email")
        from_email = EMAIL_HOST_USER

        send_mail(subject, message, from_email, [to_email])

        return HttpResponse("<h1>sent email!</h1>")

    else:
        return render(request, "send_email.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(username=username)

        if user.exists():
            return HttpResponse("<h1>User exists!</h1>")

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        return redirect("/login/")

    return render(request, "register.html")


def logoutform(request):
    logout(request)
    return redirect("/login/")


def loginform(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if not User.objects.filter(username=username).exists():
            return HttpResponse("<h1>Enter valid username</h1>")

        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponse("<h1>Enter valid password</h1>")

        else:
            login(request, user)  # session of user
            return redirect("/send_email/")

    return render(request, "login.html")
