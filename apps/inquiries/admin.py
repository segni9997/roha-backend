from django.contrib import admin
from django.utils.html import format_html
from .models import ContactInquiry, NewsletterSubscriber

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'service_interest', 'status', 'attachment_link', 'created_at')
    list_editable = ('status',)
    list_filter = ('service_interest', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'message', 'admin_notes')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'service_interest', 'message', 'attachment_link', 'created_at')

    fieldsets = (
        ("Client Information", {
            "fields": ("first_name", "last_name", "email", "phone", "service_interest")
        }),
        ("Brief & Attached Drawings", {
            "fields": ("message", "attachment_link", "created_at")
        }),
        ("Studio Triage & Notes", {
            "fields": ("status", "admin_notes")
        }),
    )

    def attachment_link(self, obj):
        if obj.blueprint_attachment:
            return format_html('<a href="{}" target="_blank" style="color: #205b63; font-weight: bold;">Download Attachment</a>', obj.blueprint_attachment.url)
        return "None"
    attachment_link.short_description = "Blueprint / File"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_editable = ('is_active',)
    search_fields = ('email',)
