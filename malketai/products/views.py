import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('id')
        data = [
            {
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
            }
            for p in products
        ]
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

        for field in ('name', 'brand', 'category', 'sku', 'price', 'description', 'is_active'):
            if field in payload:
                setattr(product, field, payload[field])
        product.save()
        return JsonResponse({'status': 'updated'})

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'status': 'deleted'})
