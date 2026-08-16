from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list'),
    path('<int:product_id>/', views.ProductDetailView.as_view(),
         name='product-detail'),
    path('<int:product_id>/reviews/', views.ReviewListCreateView.as_view(),
         name='review-list-create'),
    path('reviews/<int:review_id>/', views.ReviewDetailView.as_view(),
         name='review-detail'),
    path('<int:product_id>/generate-content/',
         views.ProductGenerateContentView.as_view(), name='product-generate-content'),
]
