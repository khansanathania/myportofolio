from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Khansa",
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