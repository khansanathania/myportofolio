
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Achievement, Skill
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import AchievementSerializer, SkillSerializer

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_list(request):
    if request.method in ("GET", "HEAD"):
        achievements = Achievement.objects.prefetch_related(
            "starred_by"
        ).order_by("title", "id")

        title = request.query_params.get("title", "").strip()

        if title:
            achievements = achievements.filter(
                title__icontains=title
            )

        serializer = AchievementSerializer(
            achievements,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    serializer = AchievementSerializer(
        data=request.data,
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_detail(request, achievement_id):
    achievement = get_object_or_404(
        Achievement.objects.prefetch_related("starred_by"),
        pk=achievement_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = AchievementSerializer(
            achievement,
            context={"request": request},
        )
        return Response(serializer.data)

    if request.method == "DELETE":
        achievement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AchievementSerializer(
        achievement,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def achievement_star(request, achievement_id):
    achievement = get_object_or_404(
        Achievement, pk=achievement_id
    )

    if achievement.starred_by.filter(
        pk=request.user.pk
    ).exists():
        achievement.starred_by.remove(request.user)
    else:
        achievement.starred_by.add(request.user)

    serializer = AchievementSerializer(
        achievement,
        context={"request": request}
    )

    return Response(serializer.data)

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])  # mengenali pengguna dari session login Django
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_list(request):
    """GET: daftar skill (bisa dicari dengan ?name=...). POST: tambah skill (pemilik saja)."""
    if request.method in ("GET", "HEAD"):
        # prefetch_related mengambil relasi starred_by sekaligus agar tidak N+1 query
        skills = Skill.objects.prefetch_related("starred_by").order_by("name", "id")
        # Pencarian dari Tugas 5 dipindahkan ke parameter query
        name = request.query_params.get("name", "").strip()
        if name:
            skills = skills.filter(name__icontains=name)
        serializer = SkillSerializer(skills, many=True, context={"request": request})
        return Response(serializer.data)

    # POST: validasi dilakukan serializer; raise_exception=True membalas 400 jika input salah
    serializer = SkillSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    """GET: detail. PUT/PATCH: ubah (pemilik dan Editor). DELETE: hapus (pemilik saja)."""
    # Permission diperiksa lebih dulu, baru objek dicari; jika tidak ada, balas 404
    skill = get_object_or_404(
        Skill.objects.prefetch_related("starred_by"), pk=skill_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = SkillSerializer(skill, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # 204: sukses, body kosong

    # PUT mengganti seluruh field (semua wajib), PATCH hanya field yang dikirim (partial)
    serializer = SkillSerializer(
        skill, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])  # semua akun yang login boleh memberi star
def skill_star(request, skill_id):
    """Toggle star: POST pertama memberi star, POST berikutnya membatalkannya."""
    skill = get_object_or_404(Skill, pk=skill_id)
    # Akun pemberi star selalu request.user, bukan dari input klien
    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
    else:
        skill.starred_by.add(request.user)
    serializer = SkillSerializer(skill, context={"request": request})
    return Response(serializer.data)


