from django.urls import path

from main.views import show_main, show_experience, show_achievement, show_achievement_detail

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    #achievement pada halaman achhievement ditangani oleh show achievement
    path("achievement/", show_achievement, name="show_achievement"),
    path("achievement/<int:id>/", show_achievement_detail, name="show_achievement_detail"),
]