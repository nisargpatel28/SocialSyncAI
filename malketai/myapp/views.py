from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import ContactForm
# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product

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


# --- Product API views (simple JSON endpoints) ---


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('id')
        data = []
        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'brand': p.brand,
                'category': p.category,
                'sku': p.sku,
                'price': str(p.price),
                'description': p.description,
                'is_active': p.is_active,
                'created_at': p.created_at.isoformat() if p.created_at else None,
                'updated_at': p.updated_at.isoformat() if p.updated_at else None,
            })
        return JsonResponse({'products': data})

    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        sku = payload.get('sku')
        if not sku:
            return JsonResponse({'error': 'SKU is required'}, status=400)

        product = Product.objects.create(
            name=payload.get('name', ''),
            brand=payload.get('brand'),
            category=payload.get('category'),
            sku=sku,
            price=payload.get('price', 0),
            description=payload.get('description', ''),
            is_active=payload.get('is_active', True),
        )
        return JsonResponse({'id': product.id}, status=201)


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'category': product.category,
            'sku': product.sku,
            'price': str(product.price),
            'description': product.description,
            'is_active': product.is_active,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'updated_at': product.updated_at.isoformat() if product.updated_at else None,
        }
        return JsonResponse(data)

    if request.method in ('PUT', 'PATCH'):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # update allowed fields
        for field in ('name', 'brand', 'category', 'sku', 'price', 'description', 'is_active'):
            if field in payload:
                setattr(product, field, payload[field])
        product.save()
        return JsonResponse({'status': 'updated'})

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'status': 'deleted'})
