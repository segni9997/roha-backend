from django.urls import path
from .views import (
    StudioProfileView,
    StudioMetricListView,
    StudioMetricDetailView,
    TeamMemberListView,
    TeamMemberDetailView,
    PageListView,
    PageDetailView,
    PageSectionListCreateView,
    PageSectionDetailView,
    FileUploadView,
    TrustedClientListView,
    TrustedClientDetailView
)
from .auth_views import AdminLoginView, AdminMeView

urlpatterns = [
    # File upload from device
    path('upload/', FileUploadView.as_view(), name='file-upload'),

    # Auth
    path('auth/login/', AdminLoginView.as_view(), name='admin-login'),
    path('auth/me/', AdminMeView.as_view(), name='admin-me'),

    # Studio Profile & Settings
    path('studio-profile/', StudioProfileView.as_view(), name='studio-profile'),
    path('metrics/', StudioMetricListView.as_view(), name='metrics-list'),
    path('metrics/<int:pk>/', StudioMetricDetailView.as_view(), name='metrics-detail'),
    path('team/', TeamMemberListView.as_view(), name='team-list'),
    path('team/<int:pk>/', TeamMemberDetailView.as_view(), name='team-detail'),

    # Page Content Builder
    path('pages/', PageListView.as_view(), name='pages-list'),
    path('pages/<str:slug>/', PageDetailView.as_view(), name='page-detail'),
    path('pages/<str:page_slug>/sections/', PageSectionListCreateView.as_view(), name='page-sections-list-create'),
    path('sections/<int:pk>/', PageSectionDetailView.as_view(), name='page-section-detail'),

    # Trusted Clients & Partners
    path('clients/', TrustedClientListView.as_view(), name='clients-list'),
    path('clients/<int:pk>/', TrustedClientDetailView.as_view(), name='clients-detail'),
]
