from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from .forms import ContactForm
# Create your views here.


def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users/index.html', context)

# This is home page view function


def home_view(request):
    return render(request, 'form_app/home.html')

# This is to define contact_view function to handle the contact form


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return redirect('contact-success')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'form_app/contact.html', context)

# Define the contact succes view function to handle success page


def contact_success_view(request):
    return render(request, 'form_app/contact_success.html')
