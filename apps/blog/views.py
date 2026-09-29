from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogCategory, BlogPost, BlogGalleryImage
from .serializers import (
    BlogCategorySerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogGalleryImageSerializer
)

class BlogCategoryListView(generics.ListCreateAPIView):
    queryset = BlogCategory.objects.all().order_by('name')
    serializer_class = BlogCategorySerializer
    pagination_class = None


class BlogCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    lookup_field = 'pk'


class BlogPostListView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().select_related('category', 'author').prefetch_related('gallery_images').order_by('-created_at')
    serializer_class = BlogPostListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'category__name', 'article_type', 'year', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'year']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogPostDetailSerializer
        return BlogPostListSerializer


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all().select_related('category', 'author').prefetch_related('gallery_images')
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'pk'


class BlogGalleryImageListCreateView(generics.ListCreateAPIView):
    serializer_class = BlogGalleryImageSerializer
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return BlogGalleryImage.objects.filter(post_id=post_id).order_by('order', 'id')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = BlogPost.objects.get(pk=post_id)
        serializer.save(post=post)


class BlogGalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogGalleryImage.objects.all()
    serializer_class = BlogGalleryImageSerializer
    lookup_field = 'pk'

