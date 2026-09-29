from rest_framework import generics, status, response, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ContactInquiry, NewsletterSubscriber
from .serializers import ContactInquirySerializer, NewsletterSubscriberSerializer

class ContactInquiryListCreateView(generics.ListCreateAPIView):
    queryset = ContactInquiry.objects.all().order_by('-created_at')
    serializer_class = ContactInquirySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['service_interest', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(
            {
                "status": "success",
                "message": "Thank you! Your architectural inquiry has been recorded. Our team will contact you shortly.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class ContactInquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    lookup_field = 'pk'


class NewsletterSubscribeView(generics.ListCreateAPIView):
    queryset = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    serializer_class = NewsletterSubscriberSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return response.Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        return response.Response(
            {
                "status": "success",
                "message": "Subscribed to ROHA Architectural Journal updates.",
                "already_subscribed": not created
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
