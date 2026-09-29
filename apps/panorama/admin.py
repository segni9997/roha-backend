from django.contrib import admin
from django.utils.html import format_html
from .models import PanoramicTour, PanoramicScene, Hotspot, TourGalleryImage


class HotspotInline(admin.TabularInline):
    model = Hotspot
    extra = 1
    fk_name = "scene"
    fields = ('text', 'hotspot_type', 'pitch', 'yaw', 'target_scene', 'target_yaw', 'target_pitch', 'css_class')


class PanoramicSceneInline(admin.TabularInline):
    model = PanoramicScene
    extra = 1
    fields = ('scene_id', 'name', 'panorama_preview', 'panorama', 'initial_yaw', 'initial_pitch', 'order')
    readonly_fields = ('panorama_preview',)

    def panorama_preview(self, obj):
        if obj.panorama:
            return format_html('<img src="{}" style="height: 45px; border-radius: 4px; object-fit: cover;" />', obj.panorama.url)
        return "-"
    panorama_preview.short_description = "Preview"


class TourGalleryImageInline(admin.TabularInline):
    model = TourGalleryImage
    extra = 1
    fields = ('image', 'caption', 'subtitle', 'order')


@admin.register(PanoramicTour)
class PanoramicTourAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'title', 'slug', 'scenes_count', 'is_featured', 'created_at')
    list_editable = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PanoramicSceneInline, TourGalleryImageInline]


    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width: 70px; height: 45px; border-radius: 4px; object-fit: cover;" />', obj.cover_image.url)
        return "-"
    cover_preview.short_description = "Cover"

    def scenes_count(self, obj):
        return obj.scenes.count()
    scenes_count.short_description = "Rooms / Scenes"


@admin.register(PanoramicScene)
class PanoramicSceneAdmin(admin.ModelAdmin):
    list_display = ('panorama_preview', 'name', 'scene_id', 'tour', 'hotspots_count', 'order')
    list_filter = ('tour',)
    search_fields = ('name', 'scene_id', 'tour__title')
    inlines = [HotspotInline]

    def panorama_preview(self, obj):
        if obj.panorama:
            return format_html('<img src="{}" style="height: 45px; border-radius: 4px; object-fit: cover;" />', obj.panorama.url)
        return "-"
    panorama_preview.short_description = "360 Image"

    def hotspots_count(self, obj):
        return obj.hotspots.count()
    hotspots_count.short_description = "Hotspots"
