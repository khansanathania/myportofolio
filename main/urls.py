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
]