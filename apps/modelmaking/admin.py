from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ModelCategory,
    PhysicalModelProject,
    FabricationSpecification,
    ModelGalleryImage,
    ModelQuotationRequest
)

class FabricationSpecificationInline(admin.StackedInline):
    model = FabricationSpecification
    can_delete = False
    verbose_name = "Fabrication & Workshop Specification"
    verbose_name_plural = "Fabrication & Workshop Specifications"
    fieldsets = (
        ("Precision & Scale", {
            "fields": ("scale", "tolerance", "lead_time", "status")
        }),
        ("Materiality & Craft", {
            "fields": ("base_material", "finish", "client")
        }),
    )


class ModelGalleryImageInline(admin.TabularInline):
    model = ModelGalleryImage
    extra = 2
    fields = ('thumbnail_preview', 'image', 'caption', 'order')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 6px; object-fit: cover;" />', obj.image.url)
        return "-"
    thumbnail_preview.short_description = "Preview"


@admin.register(PhysicalModelProject)
class PhysicalModelProjectAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'title', 'category', 'scale_ratio', 'precision_tolerance', 'year', 'is_featured', 'order')
    list_display_links = ('cover_preview', 'title')
    list_editable = ('is_featured', 'order')
    list_filter = ('category', 'scale_ratio', 'is_featured', 'year')
    search_fields = ('title', 'description', 'materials_used', 'fabrication_methods')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FabricationSpecificationInline, ModelGalleryImageInline]

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width: 70px; height: 50px; border-radius: 6px; object-fit: cover;" />', obj.cover_image.url)
        return "-"
    cover_preview.short_description = "Cover"


@admin.register(ModelCategory)
class ModelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'projects_count')
    prepopulated_fields = {'slug': ('name',)}

    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = "Scale Models Count"


@admin.register(ModelQuotationRequest)
class ModelQuotationRequestAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'email', 'desired_scale', 'deadline_date', 'cad_download', 'is_reviewed', 'created_at')
    list_editable = ('is_reviewed',)
    list_filter = ('desired_scale', 'is_reviewed', 'created_at')
    search_fields = ('client_name', 'email', 'company', 'notes')

    def cad_download(self, obj):
        if obj.cad_file:
            return format_html('<a href="{}" target="_blank" style="color: #205b63; font-weight: bold;">Download CAD</a>', obj.cad_file.url)
        return "No File"
    cad_download.short_description = "CAD Blueprint"
