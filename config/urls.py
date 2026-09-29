from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # OpenAPI Schema & Interactive Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Modular API v1 Routes
    path('api/v1/core/', include('apps.core.urls')),
    path('api/v1/interior/', include('apps.interior.urls')),
    path('api/v1/modelmaking/', include('apps.modelmaking.urls')),
    path('api/v1/panoramas/', include('apps.panorama.urls')),
    path('api/v1/blog/', include('apps.blog.urls')),
    path('api/v1/inquiries/', include('apps.inquiries.urls')),
]

# Serve media uploads in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin header and branding
admin.site.site_header = "ROHA Architectural Studio — Admin Portal"
admin.site.site_title = "ROHA Admin"
admin.site.index_title = "Studio Content, Portfolio & Inquiry Management"
