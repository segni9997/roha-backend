from rest_framework import serializers
from .fields import FlexibleImageField
from .models import StudioProfile, StudioMetric, TeamMember, Page, PageSection, TrustedClient

class StudioProfileSerializer(serializers.ModelSerializer):
    logo = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = StudioProfile
        fields = '__all__'


class StudioMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioMetric
        fields = ['id', 'metric_number', 'unit', 'label', 'order']


class TeamMemberSerializer(serializers.ModelSerializer):
    photo = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role', 'bio', 'photo', 'linkedin_url', 'order']


class PageSectionSerializer(serializers.ModelSerializer):
    background_image = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = PageSection
        fields = [
            'id', 'section_key', 'heading', 'subheading', 'body_text',
            'background_image', 'cta_text', 'cta_link', 'order', 'is_active'
        ]


class PageSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'slug', 'title', 'meta_description', 'sections', 'updated_at']

    def get_sections(self, obj):
        active_sections = obj.sections.filter(is_active=True).order_by('order')
        return PageSectionSerializer(active_sections, many=True, context=self.context).data


class TrustedClientSerializer(serializers.ModelSerializer):
    logo = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = TrustedClient
        fields = ['id', 'name', 'logo', 'industry', 'project_count', 'featured', 'order', 'website_url']

