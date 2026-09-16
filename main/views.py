from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from main.models import Experience, Achievement
from main.forms import AchievementForm
from django.core import serializers
from django.http import HttpResponse


def show_main(request):
    context = {
        "name": "Khansa Nathania",
        "npm": "2506618061",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia and teaching assistant "
            "across several courses, with interests in technology, research, finance, "
            "audit, and writing. Always exploring new ideas, developing analytical "
            "skills, and learning through both academic and teaching experiences."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Khansa Nathania Khairunnisa",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_achievement(request):
    title_query = request.GET.get("title", "").strip()
    achievement_list = Achievement.objects.all()

    if title_query:
        achievement_list = achievement_list.filter(title__icontains=title_query)

    context = {
        "name": "Khansa Nathania Khairunnisa",
        "achievement_list": achievement_list,
        "title_query": title_query,
    }
    return render(request,"achievement.html", context)

def show_achievement_detail(request, id):
    achievement = get_object_or_404(Achievement, id=id)
    context = {
        "name": "Khansa Nathania Khairunnisa",
        "achievement": achievement,
    }
    return render(request, "achievement_detail.html", context)

def create_achievement(request):
    form = AchievementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pencapaian baru berhasil ditambahkan!")
        return redirect("main:show_achievement")

    context = {
        "name": "Khansa Nathania Khairunnisa",
        "form": form,
    }
    return render(request, "achievement_form.html", context)

def get_achievements_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievement.objects.all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    achievements_json = serializers.serialize("json", achievements)
    return HttpResponse(achievements_json, content_type="application/json")

def delete_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        achievement.delete()
        messages.success(request, "Pencapaian berhasil dihapus!")
        return redirect("main:show_achievement")

    return redirect("main:show_achievement")