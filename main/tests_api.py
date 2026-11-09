
from datetime import date

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Achievement, Skill


class AchievementAPITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.achievement = Achievement.objects.create(
            title="Gold Medal",
            description="International invention competition",
            issuer="Science Organization",
            issued_at=date(2024, 11, 1),
            credential_url="https://example.com/",
        )

        self.list_url = reverse("api:achievement-list")

        self.detail_url = reverse(
            "api:achievement-detail",
            args=[self.achievement.id],
        )

        self.star_url = reverse(
            "api:achievement-star",
            args=[self.achievement.id],
        )

        self.payload = {
            "title": "New Achievement",
            "description": "A new achievement",
            "issuer": "Test Organization",
            "issued_at": "2026-11-02",
            "credential_url": "https://example.com/",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.achievement.id)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"title": "GOLD"},
        )
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"title": "not-found"},
        )
        self.assertEqual(response.data, [])

    def test_missing_achievement(self):
        url = reverse(
            "api:achievement-detail",
            args=[999999],
        )

        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )
            self.assertEqual(response.status_code, 403)

            response = self.client.patch(
                self.detail_url,
                {"title": "Changed"},
                format="json",
            )
            self.assertEqual(response.status_code, 403)

            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, 403)

        self.assertEqual(Achievement.objects.count(), 1)

        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Gold Medal")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Achievement.objects.filter(
                pk=response.data["id"]
            ).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        invalid_data = [
            ({"title": "   "}, "title"),
            (
                {"title": '<img src="x" onerror="alert(1)">'},
                "title",
            ),
            (
                {"credential_url": "javascript:alert(1)"},
                "credential_url",
            ),
        ]

        for changes, field in invalid_data:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )
            self.assertIn(field, response.data)

        self.assertEqual(Achievement.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.achievement.refresh_from_db()
        self.assertEqual(
            self.achievement.description,
            "International invention competition",
        )

        response = self.client.put(
            self.detail_url,
            {"title": "Incomplete"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(response.content, b"")

        self.assertFalse(
            Achievement.objects.filter(
                pk=self.achievement.id
            ).exists()
        )

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_create_or_delete(self):
        self.visitor.is_staff = True
        self.visitor.save()

        editor_group = Group.objects.get_or_create(name="Editor")[0]
        self.visitor.groups.add(editor_group)

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

        response = self.client.get(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(Achievement.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)

        client.login(
            username="owner",
            password="test-password",
        )

        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_editor_can_update_but_cannot_create_or_delete(self):
        editor_group = Group.objects.get_or_create(name="Editor")[0]
        self.visitor.groups.add(editor_group)

        self.client.force_authenticate(user=self.visitor)

        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Editor"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.achievement.refresh_from_db()
        self.assertEqual(
            self.achievement.title,
            "Updated by Editor",
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        

class SkillAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.skill = Skill.objects.create(name="Writing", level=4)
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.id])
        self.star_url = reverse("api:skill-star", args=[self.skill.id])
        self.payload = {"name": "Teaching", "level": 4}

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Writing")
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("starred_by", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"name": "WRI"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"name": "zzz"})
        self.assertEqual(response.data, [])

    def test_missing_skill(self):
        url = reverse("api:skill-detail", args=[9999])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"level": 1}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        # Periksa isi database, bukan hanya status HTTP
        self.assertEqual(Skill.objects.count(), 1)
        self.skill.refresh_from_db()
        self.assertEqual((self.skill.name, self.skill.level), ("Writing", 4))

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"level": 5}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.level, 5)
        response = self.client.put(self.detail_url, {"name": "Writing Pro", "level": 3}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Skill.objects.count(), 1)

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Skill.objects.filter(pk=response.data["id"], name="Teaching").exists())
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Skill.objects.filter(pk=self.skill.id).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"name": "   "}, "name"),
            ({"name": '<img src="x" onerror="alert(1)">'}, "name"),
            ({"level": 9}, "level"),
            ({"level": 0}, "level"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Skill.objects.count(), 1)

    def test_tags_are_stripped_from_name(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {"name": "<b>Teaching</b>", "level": 3}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Teaching")

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.skill.starred_by.count(), 0)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(self.skill.starred_by.count(), 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(self.skill.starred_by.count(), 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        created = Skill.objects.get(pk=response.data["id"])
        self.assertEqual(created.starred_by.count(), 0)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        client.get(self.list_url, HTTP_ACCEPT="text/html")  # Browsable API membuat cookie csrftoken
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
