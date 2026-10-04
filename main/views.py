import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from main.models import Experience, Achievement, Skill
from main.forms import AchievementForm, SkillForm

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
    is_editor = request.user.groups.filter(name="Editor").exists()
    context = {
        "name": "Khansa Nathania Khairunnisa",
        "title_query": request.GET.get("title", "").strip(),
        "is_editor": is_editor,
        "form": AchievementForm(),
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

@require_POST
def create_achievement_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pencapaian."},
            status=403,
        )

    form = AchievementForm(request.POST)
    if form.is_valid():
        achievement = form.save()
        return JsonResponse(
            {"message": "Pencapaian berhasil ditambahkan.", "pk": str(achievement.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

def get_achievements_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievement.objects.prefetch_related("starred_by").all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []

    for achievement in achievements:
        starred_users = achievement.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        data.append({
            "pk": str(achievement.id),
            "fields": {
                "title": achievement.title,
                "description": achievement.description,
                "issuer": achievement.issuer,
                "issued_at": achievement.issued_at.isoformat(),
                "credential_url": achievement.credential_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
            }
        })

    return JsonResponse(data, safe=False)


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

def show_skills(request):
    context = {
        "name": "Khansa Nathania Khairunnisa",
        "skill_query": request.GET.get("name", "").strip(),
        "form": SkillForm(),
    }
    return render(request, "skills.html", context)


def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.prefetch_related("starred_by").all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    data = []
    for skill in skills:
        starred_users = skill.starred_by.all()
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )
        data.append({
            "pk": str(skill.id),
            "fields": {
                "name": skill.name,
                "level": skill.level,
                "star_count": len(starred_users),
                "is_starred": is_starred,
            },
        })

    return JsonResponse(data, safe=False)


@require_POST
def create_skill_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan skill."},
            status=403,
        )

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {"message": "Skill berhasil ditambahkan.", "pk": str(skill.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def toggle_skill_star(request, skill_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login untuk memberi star."},
            status=401,
        )

    skill = get_object_or_404(Skill, pk=skill_id)

    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
        is_starred = False
    else:
        skill.starred_by.add(request.user)
        is_starred = True

    return JsonResponse({
        "is_starred": is_starred,
        "star_count": skill.starred_by.count(),
    })