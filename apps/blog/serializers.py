from rest_framework import serializers
from apps.core.fields import FlexibleImageField
from .models import BlogCategory, Author, BlogPost, BlogGalleryImage

class BlogCategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'posts_count']


class AuthorSerializer(serializers.ModelSerializer):
    avatar = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'avatar', 'bio']


class BlogGalleryImageSerializer(serializers.ModelSerializer):
    image = FlexibleImageField(required=True)

    class Meta:
        model = BlogGalleryImage
        fields = ['id', 'image', 'caption', 'subtitle', 'order']


class BlogPostListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(), source='category', write_only=True, required=False
    )
    author = serializers.CharField(source='author.name', read_only=True, default="ROHA Editorial")
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, required=False
    )
    type = serializers.CharField(source='article_type', required=False)
    readTime = serializers.CharField(source='read_time', required=False)
    image = FlexibleImageField(required=False, allow_null=True)
    cover_image = FlexibleImageField(source='image', required=False, allow_null=True)
    gallery_images = BlogGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'category_id',
            'author', 'author_id', 'type', 'year', 'readTime', 'image', 'cover_image',
            'gallery_images', 'is_published'
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(), source='category', write_only=True, required=False
    )
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, required=False
    )
    type = serializers.CharField(source='article_type', required=False)
    readTime = serializers.CharField(source='read_time', required=False)
    image = FlexibleImageField(required=False, allow_null=True)
    cover_image = FlexibleImageField(source='image', required=False, allow_null=True)
    gallery_images = BlogGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'category_id',
            'author', 'author_id', 'type', 'year', 'readTime', 'image', 'cover_image',
            'content', 'gallery_images', 'is_published', 'created_at'
        ]

