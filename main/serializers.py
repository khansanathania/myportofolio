
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Achievement, Skill


class AchievementSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            "id",
            "title",
            "description",
            "issuer",
            "issued_at",
            "credential_url",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_issuer(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(
            user.username for user in obj.starred_by.all()
        )
    
class SkillSerializer(serializers.ModelSerializer):
    """Mengubah objek Skill menjadi JSON (dan sebaliknya) sekaligus memvalidasi input."""

    # Field hasil perhitungan: otomatis read-only, nilainya dari method get_<nama_field>
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        # Field ditulis eksplisit (bukan "__all__") agar data sensitif tidak ikut terkirim,
        # misalnya daftar pemberi star (starred_by).
        fields = ["id", "name", "level", "star_count", "is_starred"]
        read_only_fields = ["id"]  # id tidak boleh ditentukan oleh klien

    def validate_name(self, value):
        # Perlindungan XSS di sisi server: buang tag HTML, sama seperti clean_name di SkillForm
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Nama skill tidak boleh kosong atau hanya berisi tag HTML."
            )
        return value

    def get_star_count(self, obj):
        # len() memakai hasil prefetch_related, sehingga tidak ada query tambahan per skill
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        # request diambil dari context agar status star sesuai pengguna yang sedang melihat
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()
