from django.db import models
from django.utils.text import slugify

class ModelCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Model Typology / Category"
        verbose_name_plural = "Model Typologies & Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PhysicalModelProject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(ModelCategory, on_delete=models.CASCADE, related_name="projects")
    scale_ratio = models.CharField(max_length=20, default="1:50", help_text="e.g. 1:50, 1:100, 1:200")
    year = models.CharField(max_length=20, default="2024")
    day = models.CharField(max_length=20, blank=True, default="Monday")
    precision_tolerance = models.CharField(max_length=30, default="0.1mm", help_text="Fabrication accuracy")
    materials_used = models.CharField(
        max_length=255, 
        blank=True,
        default="Laser-cut acrylic, basswood, SLA resin 3D print, brass rod joinery"
    )
    fabrication_methods = models.CharField(
        max_length=255, 
        blank=True,
        default="Hybrid 3D Printing, Laser Cutting, CNC Milling, Hand Finishing"
    )
    dimensions_cm = models.CharField(max_length=50, blank=True, default="120 x 80 x 45 cm")
    illumination = models.CharField(max_length=100, blank=True, default="Integrated 3000K warm LED lighting")
    description = models.TextField(help_text="Technical narrative, scale rationale, and craft details")
    subtitle = models.CharField(max_length=255, blank=True, default="Precision Fabrication & Architectural Scale")
    video_url = models.CharField(max_length=255, blank=True, default="https://www.youtube.com/embed/_BZZkFzuLQs", help_text="YouTube or video embed URL")
    cover_image = models.ImageField(upload_to="modelmaking/", help_text="Primary scale model photo")
    company_logo = models.ImageField(upload_to="modelmaking/clients/", blank=True, null=True, help_text="Client or partner company logo (optional, defaults to Roha logo)")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Scale Model Project"
        verbose_name_plural = "Scale Model Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Scale {self.scale_ratio})"


class FabricationSpecification(models.Model):
    project = models.OneToOneField(PhysicalModelProject, on_delete=models.CASCADE, related_name="specifications")
    scale = models.CharField(max_length=30, blank=True, default="1:50")
    tolerance = models.CharField(max_length=30, blank=True, default="0.1mm precision")
    base_material = models.CharField(max_length=120, blank=True, default="")
    finish = models.CharField(max_length=120, blank=True, default="Satin architectural white, clear lacquered timber")
    lead_time = models.CharField(max_length=50, blank=True, default="3 - 4 weeks")
    client = models.CharField(max_length=120, blank=True, default="Architectural Studio / Developer")
    status = models.CharField(max_length=50, blank=True, default="Completed", choices=[
        ('In Fabrication', 'In Fabrication / 3D Printing'),
        ('Assembled', 'Assembled & Wired'),
        ('Delivered', 'Delivered & Installed')
    ])

    class Meta:
        verbose_name = "Fabrication Specification"
        verbose_name_plural = "Fabrication Specifications"

    def __str__(self):
        return f"Fabrication Specs for {self.project.title}"


class ModelGalleryImage(models.Model):
    project = models.ForeignKey(PhysicalModelProject, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="modelmaking/gallery/")
    caption = models.CharField(max_length=200, blank=True, help_text="e.g. 0.1mm micro-louvers detail")
    subtitle = models.CharField(max_length=200, blank=True, default="Fabrication Detail")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Model Detail Photo"
        verbose_name_plural = "Model Detail Photos"

    def __str__(self):
        return f"Detail: {self.caption or self.project.title}"


class ModelQuotationRequest(models.Model):
    client_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=120, blank=True)
    desired_scale = models.CharField(max_length=30, choices=[
        ('1:50', '1:50 (Detailed Interior / Building)'),
        ('1:100', '1:100 (Standard Architecture)'),
        ('1:200', '1:200 (Complex / Commercial)'),
        ('1:500', '1:500 (Master Plan / Urban)'),
        ('Custom', 'Custom Scale Ratio'),
    ], default='1:100')
    deadline_date = models.DateField(blank=True, null=True)
    cad_file = models.FileField(upload_to="blueprints/", blank=True, null=True, help_text="Upload .DWG, .PDF, or .ZIP CAD files")
    notes = models.TextField(blank=True)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Model Quotation Request"
        verbose_name_plural = "Model Quotation Requests"

    def __str__(self):
        return f"Quote from {self.client_name} ({self.desired_scale})"
