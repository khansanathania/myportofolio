from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_achievement,
    show_achievement_detail,
    create_achievement,
    update_achievement,
    get_achievements_json,
    delete_achievement,
    register,
    login_user,
    logout_user,
    toggle_star,
    create_achievement_ajax,
    show_skills,
    get_skills_json,
    create_skill_ajax,
    toggle_skill_star,
    delete_skill,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    #achievement pada halaman achhievement ditangani oleh show achievement
    path("achievement/", show_achievement, name="show_achievement"),
    path("achievement/<int:id>/", show_achievement_detail, name="show_achievement_detail"),
    path("achievement/add/", create_achievement, name="create_achievement"),
    path("achievement/<int:id>/edit/", update_achievement, name="update_achievement"),
    path("api/achievements/", get_achievements_json, name="get_achievements_json"),
    path("achievement/<int:achievement_id>/delete/", delete_achievement, name="delete_achievement"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("achievement/<int:achievement_id>/star/", toggle_star, name="toggle_star",),
    path("achievement/add-ajax/", create_achievement_ajax, name="create_achievement_ajax"),
    path("skills/", show_skills, name="show_skills"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/add-ajax/", create_skill_ajax, name="create_skill_ajax"),
    path("skills/<int:skill_id>/star/", toggle_skill_star, name="toggle_skill_star"),
    path("skills/<int:skill_id>/delete/", delete_skill, name="delete_skill"),
]