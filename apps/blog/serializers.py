from rest_framework import serializers
from django.utils.text import slugify
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
        queryset=BlogCategory.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )
    author = serializers.CharField(source='author.name', read_only=True, default="ROHA Editorial")
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, required=False, allow_null=True
    )
    type = serializers.CharField(source='article_type', required=False, allow_blank=True)
    readTime = serializers.CharField(source='read_time', required=False, allow_blank=True)
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
    category = serializers.CharField(source='category.name', read_only=True)
    category_details = BlogCategorySerializer(source='category', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )
    author = serializers.CharField(source='author.name', read_only=True, default="ROHA Editorial")
    author_details = AuthorSerializer(source='author', read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, required=False, allow_null=True
    )
    type = serializers.CharField(source='article_type', required=False, allow_blank=True)
    readTime = serializers.CharField(source='read_time', required=False, allow_blank=True)
    image = FlexibleImageField(required=False, allow_null=True)
    cover_image = FlexibleImageField(source='image', required=False, allow_null=True)
    gallery_images = BlogGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'category_details', 'category_id',
            'author', 'author_details', 'author_id', 'type', 'year', 'readTime', 'image', 'cover_image',
            'content', 'gallery_images', 'is_published', 'created_at'
        ]

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.copy()

            # Handle Category
            if 'category_id' not in data or not data['category_id']:
                raw_cat = data.get('category')
                if isinstance(raw_cat, dict) and 'id' in raw_cat:
                    data['category_id'] = raw_cat['id']
                elif isinstance(raw_cat, (int, str)) and str(raw_cat).isdigit():
                    data['category_id'] = int(raw_cat)
                elif isinstance(raw_cat, str) and raw_cat.strip():
                    cat_obj, _ = BlogCategory.objects.get_or_create(
                        name=raw_cat.strip(),
                        defaults={'slug': slugify(raw_cat.strip())}
                    )
                    data['category_id'] = cat_obj.id
                else:
                    first_cat = BlogCategory.objects.first()
                    if not first_cat:
                        first_cat = BlogCategory.objects.create(name="Architecture", slug="architecture")
                    data['category_id'] = first_cat.id

            # Handle Author
            if 'author_id' not in data or not data['author_id']:
                raw_auth = data.get('author')
                if isinstance(raw_auth, dict) and 'id' in raw_auth:
                    data['author_id'] = raw_auth['id']
                elif isinstance(raw_auth, (int, str)) and str(raw_auth).isdigit():
                    data['author_id'] = int(raw_auth)
                elif isinstance(raw_auth, str) and raw_auth.strip():
                    auth_obj, _ = Author.objects.get_or_create(name=raw_auth.strip())
                    data['author_id'] = auth_obj.id
                else:
                    first_auth = Author.objects.first()
                    if not first_auth:
                        first_auth = Author.objects.create(name="ROHA Studio Editorial")
                    data['author_id'] = first_auth.id

            # Handle Image/Cover Image
            if not data.get('image') and data.get('cover_image'):
                data['image'] = data['cover_image']
            elif not data.get('image'):
                data['image'] = '/tr/279A1756.JPG'

            # Handle article_type & read_time
            if 'type' in data and 'article_type' not in data:
                data['article_type'] = data['type']
            if 'readTime' in data and 'read_time' not in data:
                data['read_time'] = data['readTime']

        return super().to_internal_value(data)

    def create(self, validated_data):
        gallery_data = self.initial_data.get('gallery_images', None)
        post = BlogPost.objects.create(**validated_data)

        if gallery_data and isinstance(gallery_data, list):
            for idx, g in enumerate(gallery_data):
                img_path = g.get('image') or g.get('url')
                if img_path:
                    BlogGalleryImage.objects.create(
                        post=post,
                        image=img_path,
                        caption=g.get('caption') or '',
                        subtitle=g.get('subtitle', 'Visual Monograph'),
                        order=g.get('order', idx)
                    )
        return post

    def update(self, instance, validated_data):
        gallery_data = self.initial_data.get('gallery_images', None)
        post = super().update(instance, validated_data)

        if gallery_data is not None and isinstance(gallery_data, list):
            post.gallery_images.all().delete()
            for idx, g in enumerate(gallery_data):
                img_path = g.get('image') or g.get('url')
                if img_path:
                    BlogGalleryImage.objects.create(
                        post=post,
                        image=img_path,
                        caption=g.get('caption') or '',
                        subtitle=g.get('subtitle', 'Visual Monograph'),
                        order=g.get('order', idx)
                    )
        return post

