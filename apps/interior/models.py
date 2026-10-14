from django.db import models
from django.utils.text import slugify

class InteriorCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Interior Typology / Category"
        verbose_name_plural = "Interior Typologies & Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class InteriorProject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(InteriorCategory, on_delete=models.SET_NULL, related_name="projects", null=True, blank=True)
    categories = models.ManyToManyField(InteriorCategory, related_name="multi_projects", blank=True)
    location = models.CharField(max_length=150, default="Addis Ababa, Ethiopia")
    year = models.CharField(max_length=20, default="2024")
    description = models.TextField(help_text="Project overview and spatial curation philosophy")
    subtitle = models.CharField(max_length=255, blank=True, default="Transforming the Future of Contemporary Living")
    video_url = models.CharField(max_length=255, blank=True, default="https://www.youtube.com/embed/_BZZkFzuLQs", help_text="YouTube or video embed URL")
    cover_image = models.ImageField(upload_to="interior/", help_text="Primary project visual")
    company_logo = models.ImageField(upload_to="interior/clients/", blank=True, null=True, help_text="Client or partner company logo (optional, defaults to Roha logo)")
    is_featured = models.BooleanField(default=False, help_text="Highlight on Home and Featured grids")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Interior Project"
        verbose_name_plural = "Interior Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        cat_name = self.category.name if self.category else "Uncategorized"
        return f"{self.title} ({cat_name})"


class InteriorSpecification(models.Model):
    project = models.OneToOneField(InteriorProject, on_delete=models.CASCADE, related_name="specifications")
    area = models.CharField(max_length=50, blank=True, default="450 m²", help_text="Floor area")
    floors = models.PositiveIntegerField(default=1, blank=True)
    style = models.CharField(max_length=100, blank=True, default="Contemporary Minimalist")
    material_palette = models.CharField(max_length=255, blank=True, default="")
    lighting_design = models.CharField(max_length=255, blank=True, default="Indirect warm 2700K LED coves, fluted pendants")
    duration = models.CharField(max_length=50, blank=True, default="12 months")
    budget = models.CharField(max_length=50, blank=True, default="Confidential")
    architect = models.CharField(max_length=120, blank=True, default="ROHA Interior Studio")
    client = models.CharField(max_length=120, blank=True, default="Private Residence")
    status = models.CharField(max_length=50, blank=True, default="Completed", choices=[
        ('Concept', 'Concept & Spatial Planning'),
        ('In Progress', 'In Construction / Fit-Out'),
        ('Completed', 'Completed')
    ])

    class Meta:
        verbose_name = "Spatial Specification"
        verbose_name_plural = "Spatial Specifications"

    def __str__(self):
        return f"Specs for {self.project.title}"


class InteriorGalleryImage(models.Model):
    project = models.ForeignKey(InteriorProject, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="interior/gallery/")
    caption = models.CharField(max_length=200, blank=True, help_text="e.g. Master Bedroom custom joinery")
    subtitle = models.CharField(max_length=200, blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        return f"Photo: {self.caption or self.project.title}"
