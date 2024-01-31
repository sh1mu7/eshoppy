import itertools
from django.contrib.admin.utils import NestedObjects
from django.core.exceptions import FieldDoesNotExist
from django.db import DEFAULT_DB_ALIAS
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from rest_framework import serializers

from PIL import Image as PILImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
from django.utils import timezone


def get_related_objects(obj):
    """ Return list objects that would be deleted if we delete "obj" (excluding obj) """
    collector = NestedObjects(using=DEFAULT_DB_ALIAS)
    collector.collect([obj])

    def flatten(elem):
        if isinstance(elem, list):
            return itertools.chain.from_iterable(map(flatten, elem))
        elif obj != elem:
            return elem,
        return ()

    return flatten(collector.nested())


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).file
        return super().to_representation(instance)


def compress_image(image):
    try:
        with PILImage.open(image) as img:
            output_io = BytesIO()

            # Convert to RGBA mode for better compression
            img = img.convert('RGBA')

            # Reduce size while maintaining quality
            size_reduction_factor = 0.8
            new_size = (int(img.width * size_reduction_factor), int(img.height * size_reduction_factor))

            img = img.resize(new_size, resample=PILImage.Resampling.LANCZOS)

            # Compression and conversion to WebP with lossy compression
            img.save(output_io, format='WEBP', quality=75)  # Adjust quality as needed

            output_io.seek(0)
            # Generate a unique filename based on timestamp
            timestamp = timezone.now().strftime('%H%M%S')
            original_filename = image.name
            print(original_filename)
            filename = f"{'documents/%Y/%m/%d/'}_{original_filename}_{timestamp}.webp"
            print(filename)
        return InMemoryUploadedFile(output_io, 'ImageField', filename, 'image/webp', output_io.getvalue(), None)
    except OSError as e:
        print(f"Error compressing image: {e}")
        return None


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def generate_slug(self, field_name):
        try:
            self._meta.get_field('slug')
            if not self.slug or self.slug == '':
                self.slug = slugify(getattr(self, field_name))
                while self.__class__.objects.filter(slug=self.slug).exists():
                    self.slug = self.slug + get_random_string(5)
        except FieldDoesNotExist:
            pass
