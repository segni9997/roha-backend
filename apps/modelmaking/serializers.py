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
    scale = serializers.CharField(required=False, allow_blank=True, default="1:50")
    tolerance = serializers.CharField(required=False, allow_blank=True, default="0.1mm")
    base_material = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    finish = serializers.CharField(required=False, allow_blank=True, default="")
    lead_time = serializers.CharField(required=False, allow_blank=True, default="3 - 4 weeks")
    client = serializers.CharField(required=False, allow_blank=True, default="")
    status = serializers.CharField(required=False, allow_blank=True, default="Completed")

    class Meta:
        model = FabricationSpecification
        fields = ['scale', 'tolerance', 'base_material', 'finish', 'lead_time', 'client', 'status']

    def to_internal_value(self, data):
        if not data:
            return {}
        if isinstance(data, dict):
            data = data.copy()
            if 'base_material' not in data:
                data['base_material'] = ''
        return super().to_internal_value(data)


class PhysicalModelProjectListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelCategory.objects.all(), source='category', write_only=True, required=False
    )
    materials_used = serializers.CharField(required=False, allow_blank=True, default="")
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
    materials_used = serializers.CharField(required=False, allow_blank=True, default="")
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

            if 'category_id' not in data or not data['category_id']:
                first_cat = ModelCategory.objects.first()
                if not first_cat:
                    first_cat = ModelCategory.objects.create(
                        name="Scale Architecture",
                        description="Precision architectural scale models and urban massing studies"
                    )
                data['category_id'] = first_cat.id

        return super().to_internal_value(data)

    def create(self, validated_data):
        specs_data = validated_data.pop('specifications', None)
        gallery_data = self.initial_data.get('gallery_images', None)
        project = PhysicalModelProject.objects.create(**validated_data)
        if specs_data:
            FabricationSpecification.objects.create(project=project, **specs_data)
        else:
            FabricationSpecification.objects.create(project=project)

        if gallery_data and isinstance(gallery_data, list):
            for idx, g in enumerate(gallery_data):
                img_path = g.get('image') or g.get('url')
                if img_path:
                    ModelGalleryImage.objects.create(
                        project=project,
                        image=img_path,
                        caption=g.get('caption') or g.get('title') or '',
                        subtitle=g.get('subtitle', 'Fabrication Detail'),
                        order=g.get('order', idx + 1)
                    )
        return project

    def update(self, instance, validated_data):
        specs_data = validated_data.pop('specifications', None)
        gallery_data = self.initial_data.get('gallery_images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if specs_data is not None:
            FabricationSpecification.objects.update_or_create(project=instance, defaults=specs_data)

        if gallery_data is not None and isinstance(gallery_data, list):
            existing_ids = []
            for idx, g in enumerate(gallery_data):
                img_path = g.get('image') or g.get('url')
                if not img_path:
                    continue
                gid = g.get('id')
                if gid and isinstance(gid, int):
                    try:
                        g_inst = ModelGalleryImage.objects.get(id=gid, project=instance)
                        g_inst.image = img_path
                        g_inst.caption = g.get('caption') or g.get('title') or ''
                        g_inst.subtitle = g.get('subtitle', 'Fabrication Detail')
                        g_inst.order = g.get('order', idx + 1)
                        g_inst.save()
                        existing_ids.append(g_inst.id)
                        continue
                    except ModelGalleryImage.DoesNotExist:
                        pass

                new_g = ModelGalleryImage.objects.create(
                    project=instance,
                    image=img_path,
                    caption=g.get('caption') or g.get('title') or '',
                    subtitle=g.get('subtitle', 'Fabrication Detail'),
                    order=g.get('order', idx + 1)
                )
                existing_ids.append(new_g.id)

            instance.gallery_images.exclude(id__in=existing_ids).delete()

        return instance


class ModelQuotationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelQuotationRequest
        fields = '__all__'
