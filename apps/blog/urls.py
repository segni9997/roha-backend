from django.urls import path
from .views import (
    BlogCategoryListView,
    BlogCategoryDetailView,
    BlogPostListView,
    BlogPostDetailView,
    BlogGalleryImageListCreateView,
    BlogGalleryImageDetailView
)

urlpatterns = [
    path('categories/', BlogCategoryListView.as_view(), name='blog-category-list'),
    path('categories/<int:pk>/', BlogCategoryDetailView.as_view(), name='blog-category-detail'),
    path('posts/', BlogPostListView.as_view(), name='blog-post-list'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('posts/<int:post_id>/gallery/', BlogGalleryImageListCreateView.as_view(), name='blog-gallery-list'),
    path('gallery/<int:pk>/', BlogGalleryImageDetailView.as_view(), name='blog-gallery-detail'),
]

