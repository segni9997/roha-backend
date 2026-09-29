from rest_framework import serializers
from apps.core.fields import FlexibleImageField
from .models import InteriorCategory, InteriorProject, InteriorSpecification, InteriorGalleryImage

class InteriorCategorySerializer(serializers.ModelSerializer):
    projects_count = serializers.IntegerField(source='projects.count', read_only=True)

    class Meta:
        model = InteriorCategory
        fields = ['id', 'name', 'slug', 'description', 'projects_count']


class InteriorGalleryImageSerializer(serializers.ModelSerializer):
    image = FlexibleImageField(required=True)

    class Meta:
        model = InteriorGalleryImage
        fields = ['id', 'image', 'caption', 'subtitle', 'order']


class InteriorSpecificationSerializer(serializers.ModelSerializer):
    floors = serializers.IntegerField(required=False, allow_null=True, default=1)

    class Meta:
        model = InteriorSpecification
        fields = [
            'area', 'floors', 'style', 'material_palette', 'lighting_design',
            'duration', 'budget', 'architect', 'client', 'status'
        ]

    def to_internal_value(self, data):
        if not data:
            return {}
        if isinstance(data, dict):
            data = data.copy()
            if 'floors' in data:
                raw_floors = str(data['floors']).strip()
                if not raw_floors:
                    data['floors'] = 1
                else:
                    digits = ''.join(c for c in raw_floors if c.isdigit())
                    data['floors'] = int(digits) if digits else 1
        return super().to_internal_value(data)


class InteriorProjectListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=InteriorCategory.objects.all(), source='category', write_only=True, required=False
    )
    cover_image = FlexibleImageField(required=False, allow_null=True)
    company_logo = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = InteriorProject
        fields = [
            'id', 'title', 'slug', 'category', 'category_id', 'category_name',
            'location', 'year', 'description', 'subtitle', 'video_url', 'cover_image',
            'company_logo', 'is_featured', 'order'
        ]


class InteriorProjectDetailSerializer(serializers.ModelSerializer):
    category = InteriorCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=InteriorCategory.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )
    cover_image = FlexibleImageField(required=False, allow_null=True)
    company_logo = FlexibleImageField(required=False, allow_null=True)
    specifications = InteriorSpecificationSerializer(required=False, allow_null=True)
    gallery_images = InteriorGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = InteriorProject
        fields = [
            'id', 'title', 'slug', 'category', 'category_id', 'location', 'year',
            'description', 'subtitle', 'video_url', 'cover_image', 'company_logo', 'is_featured', 'order',
            'specifications', 'gallery_images', 'created_at', 'updated_at'
        ]

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.copy()
            if 'category' in data and 'category_id' not in data:
                cat_val = data['category']
                if isinstance(cat_val, dict) and 'id' in cat_val:
                    data['category_id'] = cat_val['id']
                elif isinstance(cat_val, (int, str)) and str(cat_val).isdigit():
                    data['category_id'] = int(cat_val)
        return super().to_internal_value(data)

    def create(self, validated_data):
        specs_data = validated_data.pop('specifications', None)
        project = InteriorProject.objects.create(**validated_data)
        if specs_data:
            InteriorSpecification.objects.create(project=project, **specs_data)
        else:
            InteriorSpecification.objects.create(project=project)
        return project

    def update(self, instance, validated_data):
        specs_data = validated_data.pop('specifications', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if specs_data is not None:
            InteriorSpecification.objects.update_or_create(project=instance, defaults=specs_data)
        return instance
