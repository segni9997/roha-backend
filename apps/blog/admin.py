from django.contrib import admin
from django.utils.html import format_html
from .models import BlogCategory, Author, BlogPost, BlogGalleryImage

class BlogGalleryImageInline(admin.TabularInline):
    model = BlogGalleryImage
    extra = 1
    fields = ('image', 'caption', 'subtitle', 'order')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'title', 'category', 'author', 'article_type', 'read_time', 'is_published', 'created_at')
    list_display_links = ('cover_preview', 'title')
    list_editable = ('is_published',)
    list_filter = ('category', 'article_type', 'is_published', 'year')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogGalleryImageInline]

    def cover_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 70px; height: 45px; border-radius: 4px; object-fit: cover;" />', obj.image.url)
        return "-"
    cover_preview.short_description = "Cover"



@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'posts_count')
    prepopulated_fields = {'slug': ('name',)}

    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = "Articles"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'avatar_preview')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;" />', obj.avatar.url)
        return "-"
    avatar_preview.short_description = "Avatar"
