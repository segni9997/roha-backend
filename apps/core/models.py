from django.db import models

class StudioProfile(models.Model):
    studio_name = models.CharField(max_length=255, default="ROHA Interior and Architects")
    tagline = models.CharField(max_length=255, default="Precision Model Making & Curated Interior Architecture")
    about_narrative = models.TextField(
        default="We shape spaces that evoke emotion and elevate human experience. From bespoke residential sanctuaries to high-performance commercial headquarters, our work synthesizes light, materiality, and ergonomic precision."
    )
    address = models.TextField(
        default="Golagol, Haile Gebre Silase St, Addis Ababa, HANAN K Plaza, 8th floor"
    )
    email = models.EmailField(default="roha@gmail.com")
    phone = models.CharField(max_length=50, default="+251 911 00 00 00")
    whatsapp = models.CharField(max_length=50, blank=True, default="+251 911 00 00 00")
    office_hours = models.CharField(max_length=100, default="Mon - Fri: 8:30 AM - 6:00 PM")
    
    # Social links
    twitter_url = models.URLField(blank=True, default="#")
    instagram_url = models.URLField(blank=True, default="#")
    linkedin_url = models.URLField(blank=True, default="#")
    
    logo = models.ImageField(upload_to="pages/logos/", blank=True, null=True)

    class Meta:
        verbose_name = "Studio Profile & Global Settings"
        verbose_name_plural = "Studio Profile & Global Settings"

    def __str__(self):
        return self.studio_name


class StudioMetric(models.Model):
    metric_number = models.CharField(max_length=20, help_text="e.g. 12 or 500")
    unit = models.CharField(max_length=20, blank=True, help_text="e.g. YRS or +")
    label = models.CharField(max_length=100, help_text="e.g. Experience or Scale Models")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Studio Metric / Stat"
        verbose_name_plural = "Studio Metrics & Stats"

    def __str__(self):
        return f"{self.metric_number}{self.unit} - {self.label}"


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, help_text="e.g. Principal Architect, Lead Modeler")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="pages/team/", blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} ({self.role})"


class Page(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('interior', 'Interior Architecture Page'),
        ('model-making', 'Model Making Page'),
        ('about', 'About Studio Page'),
        ('contact', 'Contact Us Page'),
        ('gallery', '360 Panorama Gallery Page'),
    ]
    slug = models.CharField(max_length=50, unique=True, choices=PAGE_CHOICES)
    title = models.CharField(max_length=200)
    meta_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['slug']
        verbose_name = "Page (Content Builder)"
        verbose_name_plural = "Pages (Content Builder)"

    def __str__(self):
        return dict(self.PAGE_CHOICES).get(self.slug, self.slug)


class PageSection(models.Model):
    SECTION_CHOICES = [
        ('hero', 'Hero Banner & Headline'),
        ('philosophy', 'Studio Philosophy / Manifesto'),
        ('expertise', 'Architectural Expertise & Services'),
        ('metrics', 'Key Studio Metrics & Numbers'),
        ('showcase', 'Curated Project Showcase'),
        ('banner', 'Visual Atmosphere Strip'),
        ('cta', 'Consultation / Contact CTA'),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="sections")
    section_key = models.CharField(
        max_length=60, 
        choices=SECTION_CHOICES,
        default='hero',
        help_text="Block type defining layout and function on the frontend"
    )
    heading = models.CharField(max_length=255, blank=True)
    subheading = models.CharField(max_length=255, blank=True)
    body_text = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="pages/banners/", blank=True, null=True)
    cta_text = models.CharField(max_length=80, blank=True)
    cta_link = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Page Section Block"
        verbose_name_plural = "Page Section Blocks"

    def __str__(self):
        return f"[{self.page.slug.upper()}] {self.section_key} - {self.heading or 'Section'}"


class TrustedClient(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="clients/", blank=True, null=True)
    industry = models.CharField(max_length=100, default="Real Estate & Development")
    project_count = models.CharField(max_length=50, blank=True, default="Multi-scale Projects")
    featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    website_url = models.URLField(blank=True, default="#")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Trusted Client / Partner"
        verbose_name_plural = "Trusted Clients & Partners"

    def __str__(self):
        return f"{self.name} ({self.industry})"

