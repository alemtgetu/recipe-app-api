from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URl = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    "test the users API (publics)"

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        "test creating user with valid payload is successful"
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URl, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # user = get_user_model().objects.get(**res.data)
        # self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        "test creating user that already exists fails"
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URl, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        "test that the password must be more than 5 characters"
        payload = {
            'email': 'test@test.com',
            'password': 'pw',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URl, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        "test that a token is created for the user"
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'test name'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        "test that token is not created if credentials are invalid"
        create_user(email="teset@tes.com", password="testpass")
        payload = {
            'email': 'test@test.com',
            'password': 'wronpass',
            'name': 'test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        "test that token is not created if user doesnt exist"
        payload = {
            'email': 'nouser@test.com',
            'password': 'somepass',
            'name': 'test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        "test tath email and password are required"
        res = self.client.post(TOKEN_URL, {'email': 'one', 'pasword': ""})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
