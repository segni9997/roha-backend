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
    area = serializers.CharField(required=False, allow_blank=True, default="450 m²")
    floors = serializers.IntegerField(required=False, allow_null=True, default=1)
    style = serializers.CharField(required=False, allow_blank=True, default="Contemporary Minimalist")
    material_palette = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    lighting_design = serializers.CharField(required=False, allow_blank=True, default="")
    duration = serializers.CharField(required=False, allow_blank=True, default="")
    budget = serializers.CharField(required=False, allow_blank=True, default="")
    architect = serializers.CharField(required=False, allow_blank=True, default="ROHA Interior Studio")
    client = serializers.CharField(required=False, allow_blank=True, default="")
    status = serializers.CharField(required=False, allow_blank=True, default="Completed")

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
            if 'material_palette' not in data:
                data['material_palette'] = ''
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

            if 'category_id' not in data or not data['category_id']:
                first_cat = InteriorCategory.objects.first()
                if not first_cat:
                    first_cat = InteriorCategory.objects.create(
                        name="Luxury Residential",
                        description="Bespoke luxury residential and commercial architecture"
                    )
                data['category_id'] = first_cat.id

        return super().to_internal_value(data)

    def create(self, validated_data):
        specs_data = validated_data.pop('specifications', None)
        gallery_data = self.initial_data.get('gallery_images', None)
        project = InteriorProject.objects.create(**validated_data)
        if specs_data:
            InteriorSpecification.objects.create(project=project, **specs_data)
        else:
            InteriorSpecification.objects.create(project=project)

        if gallery_data and isinstance(gallery_data, list):
            for idx, g in enumerate(gallery_data):
                img_path = g.get('image') or g.get('url')
                if img_path:
                    InteriorGalleryImage.objects.create(
                        project=project,
                        image=img_path,
                        caption=g.get('caption') or g.get('title') or '',
                        subtitle=g.get('subtitle', 'Spatial Perspective'),
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
            InteriorSpecification.objects.update_or_create(project=instance, defaults=specs_data)

        if gallery_data is not None and isinstance(gallery_data, list):
            existing_ids = []
            for idx, g in enumerate(gallery_data):
                img_path = g.get('image') or g.get('url')
                if not img_path:
                    continue
                gid = g.get('id')
                if gid and isinstance(gid, int):
                    try:
                        g_inst = InteriorGalleryImage.objects.get(id=gid, project=instance)
                        g_inst.image = img_path
                        g_inst.caption = g.get('caption') or g.get('title') or ''
                        g_inst.subtitle = g.get('subtitle', 'Spatial Perspective')
                        g_inst.order = g.get('order', idx + 1)
                        g_inst.save()
                        existing_ids.append(g_inst.id)
                        continue
                    except InteriorGalleryImage.DoesNotExist:
                        pass

                new_g = InteriorGalleryImage.objects.create(
                    project=instance,
                    image=img_path,
                    caption=g.get('caption') or g.get('title') or '',
                    subtitle=g.get('subtitle', 'Spatial Perspective'),
                    order=g.get('order', idx + 1)
                )
                existing_ids.append(new_g.id)

            instance.gallery_images.exclude(id__in=existing_ids).delete()

        return instance
