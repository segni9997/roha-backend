from django.db import models
from django.utils.text import slugify

class BlogCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Journal Category"
        verbose_name_plural = "Journal Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="blog/authors/", blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    article_type = models.CharField(max_length=50, default="Guide", help_text="e.g. Guide, Case Study, Analysis, Opinion, Tutorial")
    year = models.CharField(max_length=20, default="2024")
    read_time = models.CharField(max_length=30, default="5 min read")
    description = models.TextField(help_text="Excerpt / Summary")
    image = models.ImageField(upload_to="blog/", help_text="Cover visual")
    content = models.JSONField(
        default=list, 
        help_text="Structured article blocks, e.g. [{'type': 'paragraph', 'text': '...'}, {'type': 'heading', 'text': '...'}]"
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Journal Article"
        verbose_name_plural = "Journal Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogGalleryImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="blog/gallery/")
    caption = models.CharField(max_length=200, blank=True, help_text="e.g. Editorial Figure / Diagram")
    subtitle = models.CharField(max_length=200, blank=True, default="Visual Monograph")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Blog Gallery Photo"
        verbose_name_plural = "Blog Gallery Photos"

    def __str__(self):
        return f"Photo: {self.caption or self.post.title}"

