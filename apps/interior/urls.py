from django.urls import path
from .views import (
    InteriorCategoryListView,
    InteriorCategoryDetailView,
    InteriorProjectListView,
    InteriorProjectDetailView,
    InteriorGalleryImageListCreateView,
    InteriorGalleryImageDetailView
)

urlpatterns = [
    path('categories/', InteriorCategoryListView.as_view(), name='interior-category-list'),
    path('categories/<int:pk>/', InteriorCategoryDetailView.as_view(), name='interior-category-detail'),
    path('projects/', InteriorProjectListView.as_view(), name='interior-project-list'),
    path('projects/<int:pk>/', InteriorProjectDetailView.as_view(), name='interior-project-detail'),
    path('projects/<int:project_id>/gallery/', InteriorGalleryImageListCreateView.as_view(), name='interior-project-gallery-list-create'),
    path('gallery/<int:pk>/', InteriorGalleryImageDetailView.as_view(), name='interior-gallery-image-detail'),
]
