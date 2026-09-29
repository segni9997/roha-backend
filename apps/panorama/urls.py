from django.urls import path
from .views import (
    PanoramicTourListView,
    PanoramicTourDetailView,
    PanoramicSceneListCreateView,
    PanoramicSceneDetailView,
    TourGalleryImageListCreateView,
    TourGalleryImageDetailView
)

urlpatterns = [
    path('tours/', PanoramicTourListView.as_view(), name='panoramic-tour-list'),
    path('tours/<int:pk>/', PanoramicTourDetailView.as_view(), name='panoramic-tour-detail'),
    path('tours/<int:tour_id>/scenes/', PanoramicSceneListCreateView.as_view(), name='panoramic-scene-list-create'),
    path('scenes/<int:pk>/', PanoramicSceneDetailView.as_view(), name='panoramic-scene-detail'),
    path('tours/<int:tour_id>/gallery/', TourGalleryImageListCreateView.as_view(), name='tour-gallery-list-create'),
    path('gallery/<int:pk>/', TourGalleryImageDetailView.as_view(), name='tour-gallery-detail'),
]

