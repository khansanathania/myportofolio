import os
import sys
import django
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

USER_PASSWORD = os.getenv("E2E_USER_PASSWORD")
ADMIN_PASSWORD = os.getenv("E2E_ADMIN_PASSWORD")

if not USER_PASSWORD or not ADMIN_PASSWORD:
    sys.exit("E2E_USER_PASSWORD dan E2E_ADMIN_PASSWORD belum diisi di .env.")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portofolio.settings")
django.setup()

from django.contrib.auth.models import User


def setup_users():
    user, _ = User.objects.get_or_create(username="user_test")
    user.set_password(USER_PASSWORD)
    user.is_superuser = False
    user.is_staff = False
    user.save()

    admin, _ = User.objects.get_or_create(username="admin_test")
    admin.set_password(ADMIN_PASSWORD)
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()


def main():
    setup_users()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    base_url = "http://127.0.0.1:8000"

    try:
        # 1. Buka halaman login
        driver.get(f"{base_url}/login/")

        wait.until(
            EC.presence_of_element_located(
                (By.NAME, "csrfmiddlewaretoken")
            )
        )

        assert driver.get_cookie("csrftoken")
        print("[PASS] Halaman login dan CSRF berhasil")

        # 2. Login sebagai user biasa
        driver.find_element(By.NAME, "username").send_keys("user_test")
        driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_to_be(f"{base_url}/"))

        assert driver.get_cookie("sessionid")
        assert driver.get_cookie("last_login")

        print("[PASS] Login user biasa berhasil")

        # 3. User biasa mencoba membuka halaman tambah achievement
        driver.get(f"{base_url}/achievement/add/")

        assert "403" in driver.title or "Forbidden" in driver.page_source

        print("[PASS] User biasa ditolak dengan 403")

        # 4. Logout
        driver.get(f"{base_url}/logout/")

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/login/')]")
            )
        )

        print("[PASS] Logout berhasil")

        # 5. Login sebagai superuser
        driver.get(f"{base_url}/login/")

        wait.until(
            EC.presence_of_element_located(
                (By.NAME, "username")
            )
        )

        driver.find_element(By.NAME, "username").send_keys("admin_test")
        driver.find_element(By.NAME, "password").send_keys(ADMIN_PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.url_to_be(f"{base_url}/"))

        print("[PASS] Login superuser berhasil")

        # 6. Superuser membuka halaman tambah achievement
        driver.get(f"{base_url}/achievement/add/")

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "form")
            )
        )

        print("[PASS] Superuser dapat mengakses form tambah achievement")

        print("\nSemua pengujian E2E berhasil!")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()