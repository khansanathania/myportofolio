from django.shortcuts import render, get_object_or_404

from main.models import Experience, Achievement


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
    context= {
        "name" : "Khansa Nathania Khairunnisa",
        "achievement_list" : Achievement.objects.all(),
    }
    return render(request,"achievement.html", context)

def show_achievement_detail(request, id):
    achievement = get_object_or_404(Achievement, id=id)
    context = {
        "name": "Khansa Nathania Khairunnisa",
        "achievement": achievement,
    }
    return render(request, "achievement_detail.html", context)