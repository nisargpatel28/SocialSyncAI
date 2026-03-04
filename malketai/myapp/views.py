from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import ContactForm
# Create your views here.

def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('index') 

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.info(request, "User account not found")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user_obj = authenticate(username = username, password = password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj) 
                return redirect('index')
        
            messages.info(request, 'Invalid Info')
            return redirect('/')

        return render(request, 'users/admin_login.html')
    except Exception as e:
        messages.info(request, 'Invalid Info')
        return redirect('/')

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
 
