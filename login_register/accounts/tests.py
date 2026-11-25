from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from .models import PageProfile


class AccountFlowTests(TestCase):
    def test_login_accepts_registered_email(self):
        User.objects.create_user(
            username='emailmember',
            email='asdf@sina.com',
            password='SafePassword!482',
        )

        response = self.client.post(
            reverse('login_user'),
            {'username': 'asdf@sina.com', 'password': 'SafePassword!482'},
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertContains(self.client.get(reverse('dashboard')), 'emailmember')

    def test_registration_login_dashboard_and_logout_flow(self):
        registration_response = self.client.post(
            reverse('register_user'),
            {
                'username': 'newmember',
                'email': 'newmember@example.com',
                'password1': 'SafePassword!482',
                'password2': 'SafePassword!482',
            },
        )

        self.assertRedirects(registration_response, reverse('login_user'))
        self.assertTrue(User.objects.filter(username='newmember').exists())

        login_response = self.client.post(
            reverse('login_user'),
            {'username': 'newmember', 'password': 'SafePassword!482'},
        )
        self.assertRedirects(login_response, reverse('dashboard'))

        home_response = self.client.get(reverse('home'))
        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, 'Log In')

        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertContains(dashboard_response, 'newmember')
        self.assertContains(dashboard_response, 'newmember@example.com')

        self.client.get(reverse('logout_user'))
        self.assertRedirects(
            self.client.get(reverse('dashboard')),
            f"{reverse('login_user')}?next={reverse('dashboard')}",
        )


class ProfilePictureTests(TestCase):
    def test_upload_and_delete_shared_page_profile_picture(self):
        image_buffer = BytesIO()
        Image.new('RGB', (1, 1), color='blue').save(image_buffer, format='PNG')

        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            response = self.client.post(
                reverse('dashboard'),
                {
                    'action': 'profile_picture',
                    'image': SimpleUploadedFile(
                        'profile.png',
                        image_buffer.getvalue(),
                        content_type='image/png',
                    ),
                },
            )

            self.assertRedirects(response, reverse('dashboard'))
            profile = PageProfile.objects.get(pk=1)
            self.assertTrue(profile.image.name.startswith('profile_pictures/'))
            dashboard_response = self.client.get(reverse('dashboard'))
            self.assertContains(dashboard_response, profile.image.url)
            self.assertEqual(
                dashboard_response.content.count(profile.image.url.encode()),
                1,
            )
            self.assertNotContains(dashboard_response, '+ Add a button')
            image_path = Path(profile.image.path)
            self.assertTrue(image_path.exists())

            response = self.client.post(
                reverse('dashboard'),
                {'action': 'delete_profile_picture'},
            )

            self.assertRedirects(response, reverse('dashboard'))
            profile.refresh_from_db()
            self.assertFalse(profile.image)
            self.assertFalse(image_path.exists())
            self.assertNotContains(self.client.get(reverse('dashboard')), 'Delete photo')
