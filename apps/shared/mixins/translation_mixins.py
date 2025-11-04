from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class TranslatedFieldsWriteMixin:
    """Handles CREATE/UPDATE for translated text & media fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.languages = settings.LANGUAGES

        translatable_fields = getattr(self, "translatable_fields", [])
        media_fields = getattr(self, "media_fields", [])

        for field_name in translatable_fields:
            is_media = field_name in media_fields

            # Base field is optional
            if field_name in self.fields:
                self.fields[field_name].required = False

            # Create language-specific fields
            for lang_code, lang_name in self.languages:
                field_key = f"{field_name}_{lang_code.lower()}"

                if is_media:
                    self.fields[field_key] = serializers.ListField(
                        child=serializers.FileField(),
                        required=False,
                        allow_empty=True,
                        help_text=f"{lang_name} files",
                    )
                elif field_name in self.fields:
                    original = self.fields[field_name]
                    self.fields[field_key] = original.__class__(
                        required=False,
                        allow_blank=True,
                        allow_null=True,
                        help_text=f"{lang_name} translation",
                        max_length=getattr(original, "max_length", None),
                    )

    def create(self, validated_data):
        media_data = self._extract_media_data(validated_data)
        instance = super().create(validated_data)
        self._save_media_files(instance, media_data)
        return instance

    def update(self, instance, validated_data):
        media_data = self._extract_media_data(validated_data)
        instance = super().update(instance, validated_data)
        self._save_media_files(instance, media_data)
        return instance

    def _extract_media_data(self, validated_data):
        """Pop out all media-related data."""
        media_fields = getattr(self, "media_fields", [])
        translatable_fields = getattr(self, "translatable_fields", [])
        media_data = {}

        for field_name in media_fields:
            is_translatable = field_name in translatable_fields

            if is_translatable:
                for lang_code, _ in self.languages:
                    key = f"{field_name}_{lang_code.lower()}"
                    if key in validated_data:
                        media_data[key] = validated_data.pop(key)
            elif field_name in validated_data:
                media_data[field_name] = validated_data.pop(field_name)

        return media_data

    def _save_media_files(self, instance, media_data):
        """Save uploaded media files."""
        from apps.shared.models import Media

        if not media_data:
            return

        content_type = ContentType.objects.get_for_model(instance)
        request = self.context.get("request")
        user = getattr(request, "user", None) if request else None

        for field_name, files in media_data.items():
            if not files:
                continue

            language = None
            for lang_code, _ in self.languages:
                suffix = f"_{lang_code.lower()}"
                if field_name.endswith(suffix):
                    language = lang_code
                    break

            file_list = files if isinstance(files, list) else [files]
            for file_obj in file_list:
                if file_obj:
                    Media.objects.create(
                        content_type=content_type,
                        object_id=instance.pk,
                        file=file_obj,
                        media_type="image",
                        original_filename=file_obj.name,
                        uploaded_by=user,
                        language=language,
                        is_public=True,
                    )


class TranslatedFieldsReadMixin:
    """Handle representation for web vs mobile devices."""

    def to_representation(self, instance):
        data = super().to_representation(instance)

        translatable_fields = getattr(self, "translatable_fields", [])
        media_fields = getattr(self, "media_fields", [])
        request = self.context.get("request")

        device_type = getattr(request, "device_type", "WEB")  # default web
        lang = getattr(request, "lang", None)

        for field_name in translatable_fields:
            is_media = field_name in media_fields

            if is_media:
                # Media handling
                if device_type == "MOBILE" and lang:
                    data[field_name] = self._get_media(instance, field_name, lang)
                else:
                    # web → return all media
                    all_media = []
                    for lc, _ in settings.LANGUAGES:
                        all_media.extend(self._get_media(instance, field_name, lc.lower()))
                    data[field_name] = all_media
            else:
                # Text fields handling
                if device_type == "MOBILE" and lang:
                    # Only show requested language
                    data[field_name] = getattr(instance, f"{field_name}_{lang}", "")
                    # remove any _en/_uz etc fields if present
                    for lc, _ in settings.LANGUAGES:
                        key = f"{field_name}_{lc.lower()}"
                        data.pop(key, None)
                else:
                    # Web → show all languages
                    for lc, _ in settings.LANGUAGES:
                        data[f"{field_name}_{lc.lower()}"] = getattr(
                            instance, f"{field_name}_{lc.lower()}", ""
                        )
                    data.pop(field_name, None)

        return data

    def _get_media(self, instance, field_name, language):
        """Return list of media dicts filtered by language."""
        qs = instance.media_files.filter(language__iexact=language)
        return [
            {
                "id": str(m.id),
                "url": m.file.url if m.file else None,
                "filename": m.original_filename,
                "language": m.language,
            }
            for m in qs
        ]
