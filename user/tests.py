from django.test import TestCase
from django.contrib.auth import get_user_model

# Aquí asumimos que estás utilizando el modelo de usuario personalizado de Django.
User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_user_created(self):
        """Comprobar si el usuario se creó correctamente"""
        self.assertEqual(User.objects.count(), 1)

    def test_user_username(self):
        """Comprobar si el nombre de usuario es correcto"""
        self.assertEqual(self.user.username, 'testuser')

    def test_user_email(self):
        """Comprobar si el correo electrónico del usuario es correcto"""
        self.assertEqual(self.user.email, 'test@example.com')
