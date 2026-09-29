from django.urls import path
from .views import (
    ContactInquiryListCreateView,
    ContactInquiryDetailView,
    NewsletterSubscribeView
)

urlpatterns = [
    path('submit/', ContactInquiryListCreateView.as_view(), name='inquiry-submit'),
    path('list/', ContactInquiryListCreateView.as_view(), name='inquiry-list'),
    path('<int:pk>/', ContactInquiryDetailView.as_view(), name='inquiry-detail'),
    path('subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
]
