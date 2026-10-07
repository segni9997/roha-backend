import os
from django.conf import settings
from rest_framework import serializers

class FlexibleImageField(serializers.ImageField):
    """
    Serializer field that cleanly accepts:
    - Direct file uploads (InMemoryUploadedFile)
    - Full URLs (e.g. http://127.0.0.1:8000/uploads/media_library/xyz.jpg)
    - Relative upload paths (e.g. /uploads/media_library/xyz.jpg or uploads/xyz.jpg)
    - Frontend static paths (e.g. /tr/279A1756.JPG or /1.jpg)
    
    In to_internal_value:
    Strips domains and '/uploads/' prefix so Django FieldFile stores clean relative path.
    
    In to_representation:
    Safely resolves to clean absolute URI without double '/uploads//uploads/' or corrupted domain nesting.
    """
    def to_internal_value(self, data):
        if not data:
            return None

        if isinstance(data, str):
            clean = data.strip()
            if not clean:
                return None

            # If it's a static frontend placeholder or root asset, preserve as is
            if clean.startswith('/') and not clean.startswith('/uploads/') and not clean.startswith('/media/'):
                return clean

            # Strip host if included
            if '/uploads/' in clean:
                clean = clean.split('/uploads/', 1)[1]
            elif '/media/' in clean:
                clean = clean.split('/media/', 1)[1]
            elif clean.startswith('uploads/'):
                clean = clean[8:]
            elif clean.startswith('media/'):
                clean = clean[6:]
            elif clean.startswith('/'):
                clean = clean.lstrip('/')

            return clean

        return super().to_internal_value(data)

    def to_representation(self, value):
        if not value:
            return None

        raw = getattr(value, 'name', str(value))
        if not raw:
            return None

        # If it's a static frontend placeholder, return as is
        if raw.startswith('/') and not raw.startswith('/uploads/') and not raw.startswith('/media/'):
            return raw

        # If it already had a corrupted domain or nested /uploads/ in db
        if '/uploads/' in raw:
            raw = raw.split('/uploads/', 1)[1]
        elif '/media/' in raw:
            raw = raw.split('/media/', 1)[1]
        elif raw.startswith('uploads/'):
            raw = raw[8:]
        elif raw.startswith('media/'):
            raw = raw[6:]

        raw = raw.lstrip('/')

        # If it is an external URL (e.g. unsplash or external CDN)
        if raw.startswith('http://') or raw.startswith('https://'):
            return raw

        media_url = getattr(settings, 'MEDIA_URL', '/uploads/')
        if not media_url.endswith('/'):
            media_url += '/'

        relative_url = f"{media_url}{raw}"

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(relative_url)
        return f"http://127.0.0.1:8000{relative_url}"
