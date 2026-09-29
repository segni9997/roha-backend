from django.db import models

class ContactInquiry(models.Model):
    SERVICE_CHOICES = [
        ('Interior Design', 'Interior Architecture & Curation'),
        ('Scale Model Making', 'Precision Scale Model Making'),
        ('360 Virtual Tour', '360° Virtual Tour & Panoramas'),
        ('General Architectural Inquiry', 'General Architectural Inquiry'),
    ]

    STATUS_CHOICES = [
        ('New', 'New Lead'),
        ('Reviewed', 'Reviewed by Architect'),
        ('Contacted', 'Client Contacted'),
        ('Proposal Sent', 'Proposal / Estimate Sent'),
        ('Archived', 'Archived'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, default="+251")
    service_interest = models.CharField(max_length=80, choices=SERVICE_CHOICES, default='Interior Design')
    message = models.TextField()
    blueprint_attachment = models.FileField(
        upload_to="blueprints/", 
        blank=True, 
        null=True,
        help_text="Uploaded drawing, CAD, or PDF file"
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='New')
    admin_notes = models.TextField(blank=True, help_text="Internal studio notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client Consultation Inquiry"
        verbose_name_plural = "Client Consultation Inquiries"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.service_interest}) - {self.status}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email
