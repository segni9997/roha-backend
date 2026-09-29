from rest_framework import serializers
from apps.core.fields import FlexibleImageField
from .models import PanoramicTour, PanoramicScene, Hotspot, TourGalleryImage

class HotspotSerializer(serializers.ModelSerializer):
  type = serializers.CharField(source='hotspot_type')
  sceneId = serializers.CharField(source='target_scene.scene_id', default=None, read_only=True)
  targetYaw = serializers.FloatField(source='target_yaw')
  targetPitch = serializers.FloatField(source='target_pitch')
  cssClass = serializers.CharField(source='css_class')

  class Meta:
    model = Hotspot
    fields = ['pitch', 'yaw', 'type', 'text', 'sceneId', 'targetYaw', 'targetPitch', 'cssClass']


class PanoramicSceneSerializer(serializers.ModelSerializer):
  id = serializers.CharField(source='scene_id')
  panorama = FlexibleImageField(required=True)
  hotSpots = HotspotSerializer(source='hotspots', many=True, read_only=True)

  class Meta:
    model = PanoramicScene
    fields = ['id', 'name', 'panorama', 'initial_yaw', 'initial_pitch', 'hotSpots']


class TourGalleryImageSerializer(serializers.ModelSerializer):
  image = FlexibleImageField(required=True)

  class Meta:
    model = TourGalleryImage
    fields = ['id', 'image', 'caption', 'subtitle', 'order']


class PanoramicTourSerializer(serializers.ModelSerializer):
  cover_image = FlexibleImageField(required=False, allow_null=True)
  panoramicScenes = PanoramicSceneSerializer(source='scenes', many=True, read_only=True)
  gallery_images = TourGalleryImageSerializer(many=True, read_only=True)

  class Meta:
    model = PanoramicTour
    fields = ['id', 'title', 'slug', 'description', 'cover_image', 'is_featured', 'panoramicScenes', 'gallery_images', 'created_at']

