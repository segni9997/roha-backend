from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import InteriorCategory, InteriorProject, InteriorGalleryImage
from .serializers import (
    InteriorCategorySerializer,
    InteriorProjectListSerializer,
    InteriorProjectDetailSerializer,
    InteriorGalleryImageSerializer
)

class InteriorCategoryListView(generics.ListCreateAPIView):
    queryset = InteriorCategory.objects.all().order_by('name')
    serializer_class = InteriorCategorySerializer
    pagination_class = None


class InteriorCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InteriorCategory.objects.all()
    serializer_class = InteriorCategorySerializer
    lookup_field = 'pk'


class InteriorProjectListView(generics.ListCreateAPIView):
    queryset = InteriorProject.objects.all().select_related('category').order_by('order', '-created_at')
    serializer_class = InteriorProjectListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'category__name', 'is_featured', 'year']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['order', 'year', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InteriorProjectDetailSerializer
        return InteriorProjectListSerializer


class InteriorProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InteriorProject.objects.all().select_related('category', 'specifications').prefetch_related('gallery_images')
    serializer_class = InteriorProjectDetailSerializer
    lookup_field = 'pk'


class InteriorGalleryImageListCreateView(generics.ListCreateAPIView):
    serializer_class = InteriorGalleryImageSerializer
    pagination_class = None

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return InteriorGalleryImage.objects.filter(project_id=project_id).order_by('order', 'id')

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = InteriorProject.objects.get(pk=project_id)
        serializer.save(project=project)


class InteriorGalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InteriorGalleryImage.objects.all()
    serializer_class = InteriorGalleryImageSerializer
    lookup_field = 'pk'

