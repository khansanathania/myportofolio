from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput
from main.models import Achievement


class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = [
            "title",
            "description",
            "issuer",
            "issued_at",
            "credential_url",
        ]
        labels = {
            "title": "Nama Pencapaian",
            "description": "Deskripsi",
            "issuer": "Diberikan Oleh",
            "issued_at": "Tanggal Diterima",
            "credential_url": "URL Sertifikat",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Gold Medal International Science and Invention Fair",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pencapaianmu",
                    "rows": 3,
                }
            ),
            "issuer": TextInput(
                attrs={
                    "placeholder": "Indonesian Young Scientist Association",
                }
            ),
            "issued_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "credential_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }