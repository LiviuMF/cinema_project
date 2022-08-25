from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class MembersTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username='new_test_user',
            first_name='First Name',
            last_name='Last Name',
            email='test@new_user.com',
        )
        self.user.password = 'test123123'
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_user_exists(self):
        self.assertEqual(self.user.username, 'new_test_user')

    def test_login(self):
        url = reverse('login_page')
        c = Client()
        response = c.post(path=url, data={'email': 'test@new_user.com',
                                          'password': 'test123123'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        c = Client()
        c.logout()
        self.assertFalse("_auth_user_id" in c.session)

    def test_user_registration(self):
        url = reverse('register_page')
        c = Client()
        response = c.post(path=url, data={
            'username': self.user.username,
            'email': self.user.email,
            'password': self.user.password,
            'password2': self.user.password})
        self.assertEqual(response.status_code, 200)
