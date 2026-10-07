from django.contrib import admin
from django.utils.html import format_html
from .models import StudioProfile, StudioMetric, TeamMember, Page, PageSection

class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 1
    classes = ('collapse',)
    fieldsets = (
        ("Block Identification & Role", {
            "fields": (('section_key', 'order', 'is_active'), ('heading', 'subheading'))
        }),
        ("Content Narrative & Media", {
            "fields": ('body_text', ('background_image', 'image_preview'))
        }),
        ("Action Link / Button", {
            "fields": (('cta_text', 'cta_link'),)
        }),
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" style="height: 60px; max-width: 140px; border-radius: 6px; object-fit: cover; border: 1px solid #cbd5e1;" />', 
                obj.background_image.url
            )
        return format_html('<span style="color: #94a3b8; font-style: italic;">No media uploaded</span>')
    image_preview.short_description = "Visual Preview"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('page_badge', 'title', 'is_active', 'sections_count', 'live_page_link', 'updated_at')
    list_display_links = ('page_badge', 'title')
    list_editable = ('is_active',)
    inlines = [PageSectionInline]

    PAGE_URL_MAP = {
        'home': '',
        'interior': 'interior',
        'model-making': 'model-making',
        'about': 'about',
        'contact': 'contactus',
        'gallery': 'gallery',
    }

    def page_badge(self, obj):
        colors = {
            'home': ('#0369a1', '#e0f2fe'),
            'interior': ('#047857', '#d1fae5'),
            'model-making': ('#b45309', '#fef3c7'),
            'about': ('#7e22ce', '#f3e8ff'),
            'contact': ('#be123c', '#ffe4e6'),
            'gallery': ('#0f766e', '#ccfbf1'),
        }
        fg, bg = colors.get(obj.slug, ('#334155', '#f1f5f9'))
        return format_html(
            '<span style="background: {}; color: {}; font-weight: 800; font-family: monospace; padding: 3px 8px; border-radius: 6px; font-size: 11px; text-transform: uppercase;">{}</span>',
            bg, fg, obj.slug
        )
    page_badge.short_description = "Page Slug"

    def sections_count(self, obj):
        count = obj.sections.count()
        return format_html(
            '<span style="font-weight: 700; color: #172a2b;">{} blocks</span>', count
        )
    sections_count.short_description = "Blocks"

    def live_page_link(self, obj):
        path = self.PAGE_URL_MAP.get(obj.slug, obj.slug)
        url = f"http://localhost:5173/{path}"
        return format_html(
            '<a href="{}" target="_blank" style="display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; background: #205b63; color: #ffffff; border-radius: 6px; font-weight: 700; font-size: 11px; text-decoration: none;">Live View ↗</a>',
            url
        )
    live_page_link.short_description = "Frontend Preview"


@admin.register(StudioProfile)
class StudioProfileAdmin(admin.ModelAdmin):
    list_display = ('studio_name', 'email', 'phone', 'address')

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(StudioMetric)
class StudioMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_display', 'label', 'order')
    list_editable = ('order',)

    def metric_display(self, obj):
        return format_html(
            '<span style="font-weight: 800; font-size: 14px; color: #205b63;">{}{}</span>',
            obj.metric_number, obj.unit
        )
    metric_display.short_description = "Stat"


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'role', 'order')
    list_editable = ('order',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #cbd5e1;" />', obj.photo.url)
        return format_html('<span style="color: #94a3b8;">No photo</span>')
    photo_preview.short_description = "Portrait"


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'page_badge', 'section_key', 'heading', 'subheading', 'order', 'is_active')
    list_display_links = ('heading', 'section_key')
    list_filter = ('page', 'section_key', 'is_active')
    search_fields = ('heading', 'subheading', 'body_text')
    list_editable = ('order', 'is_active')

    def page_badge(self, obj):
        return format_html(
            '<span style="background: #e0f2fe; color: #0369a1; font-weight: 700; font-family: monospace; padding: 2px 6px; border-radius: 4px; font-size: 11px;">{}</span>',
            obj.page.slug
        )
    page_badge.short_description = "Page"

    def image_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" style="height: 40px; width: 70px; border-radius: 4px; object-fit: cover; border: 1px solid #cbd5e1;" />', 
                obj.background_image.url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No media</span>')
    image_preview.short_description = "Media"


from .models import TrustedClient

@admin.register(TrustedClient)
class TrustedClientAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'industry', 'project_count', 'featured', 'order')
    list_display_links = ('name',)
    list_filter = ('featured', 'industry')
    search_fields = ('name', 'industry')
    list_editable = ('featured', 'order')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height: 32px; max-width: 80px; object-fit: contain;" />', obj.logo.url)
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No logo</span>')
    logo_preview.short_description = "Logo"

