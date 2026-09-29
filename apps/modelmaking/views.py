from rest_framework import generics, filters, status, response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ModelCategory, PhysicalModelProject, ModelQuotationRequest, ModelGalleryImage
from .serializers import (
    ModelCategorySerializer,
    PhysicalModelProjectListSerializer,
    PhysicalModelProjectDetailSerializer,
    ModelQuotationRequestSerializer,
    ModelGalleryImageSerializer
)

class ModelCategoryListView(generics.ListCreateAPIView):
    queryset = ModelCategory.objects.all().order_by('name')
    serializer_class = ModelCategorySerializer
    pagination_class = None


class ModelCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ModelCategory.objects.all()
    serializer_class = ModelCategorySerializer
    lookup_field = 'pk'


class PhysicalModelProjectListView(generics.ListCreateAPIView):
    queryset = PhysicalModelProject.objects.all().select_related('category').order_by('order', '-created_at')
    serializer_class = PhysicalModelProjectListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'category__name', 'scale_ratio', 'is_featured', 'year']
    search_fields = ['title', 'description', 'materials_used', 'fabrication_methods']
    ordering_fields = ['order', 'year', 'scale_ratio']


class PhysicalModelProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhysicalModelProject.objects.all().select_related('category', 'specifications').prefetch_related('gallery_images')
    serializer_class = PhysicalModelProjectDetailSerializer
    lookup_field = 'pk'


class ModelQuotationCreateView(generics.ListCreateAPIView):
    queryset = ModelQuotationRequest.objects.all().order_by('-created_at')
    serializer_class = ModelQuotationRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(
            {
                "status": "success",
                "message": "Model quotation request received. Our master fabricator will review the CAD drawings and respond.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class ModelQuotationDetailView(generics.RetrieveDestroyAPIView):
    queryset = ModelQuotationRequest.objects.all()
    serializer_class = ModelQuotationRequestSerializer
    lookup_field = 'pk'


class ModelGalleryImageListCreateView(generics.ListCreateAPIView):
    serializer_class = ModelGalleryImageSerializer
    pagination_class = None

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ModelGalleryImage.objects.filter(project_id=project_id).order_by('order', 'id')

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = PhysicalModelProject.objects.get(pk=project_id)
        serializer.save(project=project)


class ModelGalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ModelGalleryImage.objects.all()
    serializer_class = ModelGalleryImageSerializer
    lookup_field = 'pk'

