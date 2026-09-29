from django.urls import path
from .views import (
    ModelCategoryListView,
    ModelCategoryDetailView,
    PhysicalModelProjectListView,
    PhysicalModelProjectDetailView,
    ModelQuotationCreateView,
    ModelQuotationDetailView,
    ModelGalleryImageListCreateView,
    ModelGalleryImageDetailView
)

urlpatterns = [
    path('categories/', ModelCategoryListView.as_view(), name='model-category-list'),
    path('categories/<int:pk>/', ModelCategoryDetailView.as_view(), name='model-category-detail'),
    path('projects/', PhysicalModelProjectListView.as_view(), name='model-project-list'),
    path('projects/<int:pk>/', PhysicalModelProjectDetailView.as_view(), name='model-project-detail'),
    path('projects/<int:project_id>/gallery/', ModelGalleryImageListCreateView.as_view(), name='model-project-gallery-list-create'),
    path('gallery/<int:pk>/', ModelGalleryImageDetailView.as_view(), name='model-gallery-image-detail'),
    path('quote-request/', ModelQuotationCreateView.as_view(), name='model-quote-request'),
    path('quote-request/<int:pk>/', ModelQuotationDetailView.as_view(), name='model-quote-detail'),
]
