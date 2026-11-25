from django.urls import path
from main import api_views
from rest_framework.authtoken import views as authtoken_views

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
        # Endpoint autentikasi token untuk klien mobile
    path("auth/token/", authtoken_views.obtain_auth_token, name="token-auth"),
    path("auth/logout/", api_views.api_logout, name="logout"),

    # Endpoint Project
    path("projects/", api_views.project_list, name="project-list"),

]
