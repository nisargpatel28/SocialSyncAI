from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer


class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all().order_by('id')
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'id': serializer.instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'status': 'deleted'})


class ReviewListCreateView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, product_id):
        """List all reviews for a product"""
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request, product_id):
        """Create a new review (authenticated users only)"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        existing_review = Review.objects.filter(product=product, user=request.user).first()
        if existing_review:
            return Response(
                {'error': 'You have already reviewed this product'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, review_id):
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None
    
    def get(self, request, review_id):
        """Get a specific review"""
        review = self.get_object(review_id)
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def put(self, request, review_id):
        """Update a review (owner only)"""
        review = self.get_object(review_id)
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if review.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, review_id):
        """Delete a review (owner only)"""
        review = self.get_object(review_id)
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if review.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        review.delete()
        return Response({'status': 'deleted'})
