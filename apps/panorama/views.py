from rest_framework import generics
from .models import PanoramicTour, PanoramicScene, TourGalleryImage
from .serializers import (
    PanoramicTourSerializer,
    PanoramicSceneSerializer,
    TourGalleryImageSerializer
)

class PanoramicTourListView(generics.ListCreateAPIView):
    queryset = PanoramicTour.objects.all().prefetch_related('scenes__hotspots', 'gallery_images').order_by('-created_at')
    serializer_class = PanoramicTourSerializer


class PanoramicTourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PanoramicTour.objects.all().prefetch_related('scenes__hotspots', 'gallery_images')
    serializer_class = PanoramicTourSerializer
    lookup_field = 'pk'


class PanoramicSceneListCreateView(generics.ListCreateAPIView):
    serializer_class = PanoramicSceneSerializer
    pagination_class = None

    def get_queryset(self):
        tour_id = self.kwargs.get('tour_id')
        if tour_id:
            return PanoramicScene.objects.filter(tour_id=tour_id).order_by('order')
        return PanoramicScene.objects.all().order_by('order')

    def perform_create(self, serializer):
        tour_id = self.kwargs.get('tour_id')
        tour = PanoramicTour.objects.get(id=tour_id)
        serializer.save(tour=tour)


class PanoramicSceneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PanoramicScene.objects.all()
    serializer_class = PanoramicSceneSerializer
    lookup_field = 'pk'


class TourGalleryImageListCreateView(generics.ListCreateAPIView):
    serializer_class = TourGalleryImageSerializer
    pagination_class = None

    def get_queryset(self):
        tour_id = self.kwargs.get('tour_id')
        return TourGalleryImage.objects.filter(tour_id=tour_id).order_by('order', 'id')

    def perform_create(self, serializer):
        tour_id = self.kwargs.get('tour_id')
        tour = PanoramicTour.objects.get(pk=tour_id)
        serializer.save(tour=tour)


class TourGalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourGalleryImage.objects.all()
    serializer_class = TourGalleryImageSerializer
    lookup_field = 'pk'

