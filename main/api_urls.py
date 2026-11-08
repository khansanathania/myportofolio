from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    path(
        "achievements/",
        api_views.achievement_list,
        name="achievement-list"
    ),

    path(
        "achievements/<int:achievement_id>/",
        api_views.achievement_detail,
        name="achievement-detail"
    ),

    path(
        "achievements/<int:achievement_id>/star/",
        api_views.achievement_star,
        name="achievement-star"
    ),

    # Primary key Skill berupa angka, jadi memakai <int:...> (bukan <uuid:...>)
    path("skills/", api_views.skill_list, name="skill-list"),
    path("skills/<int:skill_id>/", api_views.skill_detail, name="skill-detail"),
    path("skills/<int:skill_id>/star/", api_views.skill_star, name="skill-star"),
]
