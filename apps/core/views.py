from rest_framework import generics, views, response, status
from .models import StudioProfile, StudioMetric, TeamMember, Page, PageSection
from .serializers import (
    StudioProfileSerializer,
    StudioMetricSerializer,
    TeamMemberSerializer,
    PageSerializer,
    PageSectionSerializer
)

class StudioProfileView(views.APIView):
    def get(self, request):
        profile = StudioProfile.objects.first()
        if not profile:
            profile = StudioProfile.objects.create()
        serializer = StudioProfileSerializer(profile, context={'request': request})
        return response.Response(serializer.data)

    def put(self, request):
        profile = StudioProfile.objects.first()
        if not profile:
            profile = StudioProfile.objects.create()
        serializer = StudioProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class StudioMetricListView(generics.ListCreateAPIView):
    queryset = StudioMetric.objects.all().order_by('order')
    serializer_class = StudioMetricSerializer
    pagination_class = None


class StudioMetricDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudioMetric.objects.all()
    serializer_class = StudioMetricSerializer
    lookup_field = 'pk'


class TeamMemberListView(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all().order_by('order')
    serializer_class = TeamMemberSerializer
    pagination_class = None


class TeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    lookup_field = 'pk'


class PageListView(generics.ListCreateAPIView):
    queryset = Page.objects.all().order_by('slug')
    serializer_class = PageSerializer
    pagination_class = None


class PageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        page, _ = Page.objects.get_or_create(
            slug=slug,
            defaults={
                'title': f"ROHA {slug.replace('-', ' ').title()}",
                'meta_description': f"ROHA Studio {slug} page",
                'is_active': True,
            }
        )
        return page


class PageSectionListCreateView(generics.ListCreateAPIView):
    serializer_class = PageSectionSerializer
    pagination_class = None

    def get_queryset(self):
        page_slug = self.kwargs.get('page_slug')
        if page_slug:
            return PageSection.objects.filter(page__slug=page_slug).order_by('order')
        return PageSection.objects.all().order_by('order')

    def perform_create(self, serializer):
        page_slug = self.kwargs.get('page_slug')
        page, _ = Page.objects.get_or_create(
            slug=page_slug,
            defaults={
                'title': f"ROHA {page_slug.replace('-', ' ').title()}",
                'is_active': True,
            }
        )
        serializer.save(page=page)


class PageSectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PageSection.objects.all()
    serializer_class = PageSectionSerializer
    lookup_field = 'pk'


from .models import TrustedClient
from .serializers import TrustedClientSerializer

class TrustedClientListView(generics.ListCreateAPIView):
    queryset = TrustedClient.objects.all().order_by('order', 'id')
    serializer_class = TrustedClientSerializer
    pagination_class = None


class TrustedClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrustedClient.objects.all()
    serializer_class = TrustedClientSerializer
    lookup_field = 'pk'



import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser

class FileUploadView(views.APIView):
    """
    Accepts multipart file uploads (images and videos from local device),
    saves them to MEDIA_ROOT/media_library/, and returns the public URL.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return response.Response(
                {'error': 'No file provided. Expected "file" field in form-data.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        base_name, ext = os.path.splitext(file_obj.name)
        clean_base = "".join(c for c in base_name if c.isalnum() or c in ('-', '_')).strip() or "asset"
        unique_name = f"{uuid.uuid4().hex[:8]}_{clean_base}{ext.lower()}"
        relative_path = os.path.join('media_library', unique_name)

        saved_file_name = default_storage.save(relative_path, file_obj)
        url = default_storage.url(saved_file_name)
        if not url.startswith('/'):
            url = settings.MEDIA_URL + url

        return response.Response({
            'url': url,
            'filename': file_obj.name,
            'size': file_obj.size,
            'content_type': getattr(file_obj, 'content_type', '')
        }, status=status.HTTP_201_CREATED)

