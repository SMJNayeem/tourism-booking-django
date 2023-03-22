from django.shortcuts import render
from django.http import HttpResponse


def homePage(request):
    return render(request, 'home.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def contactus(request):
    return render(request, 'contact.html')
