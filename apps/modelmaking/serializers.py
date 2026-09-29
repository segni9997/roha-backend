from rest_framework import serializers
from apps.core.fields import FlexibleImageField
from .models import (
    ModelCategory,
    PhysicalModelProject,
    FabricationSpecification,
    ModelGalleryImage,
    ModelQuotationRequest
)

class ModelCategorySerializer(serializers.ModelSerializer):
    projects_count = serializers.IntegerField(source='projects.count', read_only=True)

    class Meta:
        model = ModelCategory
        fields = ['id', 'name', 'slug', 'description', 'projects_count']


class ModelGalleryImageSerializer(serializers.ModelSerializer):
    image = FlexibleImageField(required=True)

    class Meta:
        model = ModelGalleryImage
        fields = ['id', 'image', 'caption', 'subtitle', 'order']


class FabricationSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricationSpecification
        fields = ['scale', 'tolerance', 'base_material', 'finish', 'lead_time', 'client', 'status']

    def to_internal_value(self, data):
        if not data:
            return {}
        return super().to_internal_value(data)


class PhysicalModelProjectListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelCategory.objects.all(), source='category', write_only=True, required=False
    )
    cover_image = FlexibleImageField(required=False, allow_null=True)
    company_logo = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = PhysicalModelProject
        fields = [
            'id', 'title', 'slug', 'category', 'category_id', 'category_name',
            'scale_ratio', 'year', 'day', 'precision_tolerance',
            'materials_used', 'fabrication_methods', 'description', 'subtitle', 'video_url',
            'cover_image', 'company_logo', 'is_featured', 'order'
        ]


class PhysicalModelProjectDetailSerializer(serializers.ModelSerializer):
    category = ModelCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelCategory.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )
    cover_image = FlexibleImageField(required=False, allow_null=True)
    company_logo = FlexibleImageField(required=False, allow_null=True)
    specifications = FabricationSpecificationSerializer(required=False, allow_null=True)
    gallery_images = ModelGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = PhysicalModelProject
        fields = [
            'id', 'title', 'slug', 'category', 'category_id', 'scale_ratio', 'year',
            'day', 'precision_tolerance', 'materials_used',
            'fabrication_methods', 'dimensions_cm', 'illumination',
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
        project = PhysicalModelProject.objects.create(**validated_data)
        if specs_data:
            FabricationSpecification.objects.create(project=project, **specs_data)
        else:
            FabricationSpecification.objects.create(project=project)
        return project

    def update(self, instance, validated_data):
        specs_data = validated_data.pop('specifications', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if specs_data is not None:
            FabricationSpecification.objects.update_or_create(project=instance, defaults=specs_data)
        return instance


class ModelQuotationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelQuotationRequest
        fields = '__all__'
