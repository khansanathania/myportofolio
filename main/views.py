import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from main.models import Experience, Achievement
from main.forms import AchievementForm
from django.core import serializers
from django.http import HttpResponse


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Khansa Nathania Khairunnisa",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_achievement(request):
    json_response = get_achievements_json(request)
    achievements = serializers.deserialize(
        "json", json_response.content.decode("utf-8")
    )

    achievement_list = [achievement.object for achievement in achievements]

    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Khansa Nathania Khairunnisa",
        "achievement_list": achievement_list,
        "title_query": request.GET.get("title", "").strip(),
        "is_editor": is_editor,
    }
    return render(request,"achievement.html", context)

def show_achievement_detail(request, id):
    achievement = get_object_or_404(Achievement, id=id)
    context = {
        "name": "Khansa Nathania Khairunnisa",
        "achievement": achievement,
    }
    return render(request, "achievement_detail.html", context)


@login_required(login_url="/login/")
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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

    # Membatasi field JSON agar data sensitif seperti starred_by tidak ikut terekspos
    achievements_json = serializers.serialize("json", achievements, fields=["title", "description", "issuer", "issued_at", "credential_url"])
    return HttpResponse(achievements_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        achievement.delete()
        messages.success(request, "Pencapaian berhasil dihapus!")
        return redirect("main:show_achievement")

    return redirect("main:show_achievement")


@login_required(login_url="/login/")
def update_achievement(request, id):
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name="Editor").exists()
    ):
        raise PermissionDenied

    achievement = get_object_or_404(Achievement, id= id)
    form = AchievementForm(request.POST or None, instance=achievement)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pencapaian berhasil diperbaharui! ")
        return redirect("main:show_achievement")
    context = {
        "name" : "Khansa Nathania Khairunnisa",
        "form" : form,
        "achievement" : achievement
    }
    return render(request, "achievement_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Khansa Nathania Khairunnisa",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Khansa Nathania Khairunnisa",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        if request.user in achievement.starred_by.all():
            achievement.starred_by.remove(request.user)
        else:
            achievement.starred_by.add(request.user)

    return redirect("main:show_achievement")