from rest_framework import serializers
from .models import ContactInquiry, NewsletterSubscriber

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'service_interest', 'message', 'blueprint_attachment',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']
