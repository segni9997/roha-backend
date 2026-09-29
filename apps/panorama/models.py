from django.db import models
from django.utils.text import slugify

class PanoramicTour(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="panoramas/", blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "360° Virtual Tour"
        verbose_name_plural = "360° Virtual Tours"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PanoramicScene(models.Model):
    tour = models.ForeignKey(PanoramicTour, on_delete=models.CASCADE, related_name="scenes")
    scene_id = models.CharField(max_length=80, help_text="Unique key within tour, e.g. livingRoom, kitchen")
    name = models.CharField(max_length=120, help_text="Display label, e.g. Living Room, Main Lobby")
    panorama = models.ImageField(
        upload_to="panoramas/equirectangular/",
        help_text="2:1 aspect ratio equirectangular 360 photo"
    )
    initial_yaw = models.FloatField(default=0.0, help_text="Starting horizontal rotation (deg)")
    initial_pitch = models.FloatField(default=0.0, help_text="Starting vertical angle (deg)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('tour', 'scene_id')
        verbose_name = "Panoramic Room / Scene"
        verbose_name_plural = "Panoramic Rooms & Scenes"

    def __str__(self):
        return f"{self.tour.title} -> {self.name} ({self.scene_id})"


class Hotspot(models.Model):
    scene = models.ForeignKey(PanoramicScene, on_delete=models.CASCADE, related_name="hotspots")
    pitch = models.FloatField(help_text="Vertical coordinate (-90 to +90)")
    yaw = models.FloatField(help_text="Horizontal coordinate (-180 to +180)")
    hotspot_type = models.CharField(
        max_length=20, 
        choices=[('scene', 'Scene Transition'), ('info', 'Information Tooltip')],
        default='scene'
    )
    text = models.CharField(max_length=150, help_text="Tooltip label e.g. 'Go to Kitchen'")
    target_scene = models.ForeignKey(
        PanoramicScene, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name="incoming_hotspots",
        help_text="Destination scene if type is 'scene'"
    )
    target_yaw = models.FloatField(default=0.0, help_text="Camera yaw upon arrival")
    target_pitch = models.FloatField(default=0.0, help_text="Camera pitch upon arrival")
    css_class = models.CharField(max_length=50, default="custom-hotspot")

    class Meta:
        verbose_name = "Interactive Hotspot"
        verbose_name_plural = "Interactive Hotspots"

    def __str__(self):
        return f"Hotspot: '{self.text}' in {self.scene.name}"


class TourGalleryImage(models.Model):
    tour = models.ForeignKey(PanoramicTour, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="panoramas/gallery/")
    caption = models.CharField(max_length=200, blank=True, help_text="e.g. Master Suite Spatial Perspective")
    subtitle = models.CharField(max_length=200, blank=True, default="Spatial Render / Photo")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Virtual Tour Gallery Photo"
        verbose_name_plural = "Virtual Tour Gallery Photos"

    def __str__(self):
        return f"Gallery Photo: {self.caption or self.tour.title}"

