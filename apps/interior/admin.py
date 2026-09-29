from django.contrib import admin
from django.utils.html import format_html
from .models import InteriorCategory, InteriorProject, InteriorSpecification, InteriorGalleryImage

class InteriorSpecificationInline(admin.StackedInline):
    model = InteriorSpecification
    can_delete = False
    verbose_name = "Spatial & Material Specification"
    verbose_name_plural = "Spatial & Material Specifications"
    fieldsets = (
        ("Spatial Dimensions & Performance", {
            "fields": ("area", "floors", "style", "status", "duration", "budget")
        }),
        ("Craft & Architecture", {
            "fields": ("material_palette", "lighting_design", "architect", "client")
        }),
    )


class InteriorGalleryImageInline(admin.TabularInline):
    model = InteriorGalleryImage
    extra = 2
    fields = ('thumbnail_preview', 'image', 'caption', 'order')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 6px; object-fit: cover;" />', obj.image.url)
        return "-"
    thumbnail_preview.short_description = "Preview"


@admin.register(InteriorProject)
class InteriorProjectAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'title', 'category', 'location', 'year', 'is_featured', 'order')
    list_display_links = ('cover_preview', 'title')
    list_editable = ('is_featured', 'order')
    list_filter = ('category', 'is_featured', 'year', 'specifications__status')
    search_fields = ('title', 'description', 'location', 'specifications__architect', 'specifications__client')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [InteriorSpecificationInline, InteriorGalleryImageInline]

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width: 70px; height: 50px; border-radius: 6px; object-fit: cover;" />', obj.cover_image.url)
        return "-"
    cover_preview.short_description = "Cover"


@admin.register(InteriorCategory)
class InteriorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'projects_count')
    prepopulated_fields = {'slug': ('name',)}

    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = "Total Projects"
