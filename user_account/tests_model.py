import datetime

from django.utils import timezone
from django.test import TestCase

from .models import User


def create_user(time=timezone.now()):
    user = User.objects.create_user(
        email='example_user_mail@gmail.com',
        password="example_password",
        name='Jan',
        surname='Kowalski',
    )
    user.register_date = time
    user.register_updated = time
    user.akey_expires = time + datetime.timedelta(2)
    user.last_login = time
    return user


def create_superuser(time=timezone.now()):
    super_user = User.objects.create_superuser(
        email='example_super_user_mail@gmail.com',
        password="example_password",
        name='Jan',
        surname='Kowalski',
    )
    super_user.register_date = time
    super_user.register_updated = time
    super_user.akey_expires = time + datetime.timedelta(2)
    super_user.last_login = time
    return super_user


class UserMethodTests(TestCase):
    """
    Tests for methods of User model.
    """

    def test_get_email(self):
        """Test for method get_mail - should return email of user object. """
        user = create_user()
        self.assertEqual(user.get_email, 'example_user_mail@gmail.com')

    def test_get_short_name(self):
        """Test for method get_short_name
        - should return name of user object. """
        user = create_user()
        self.assertEqual(user.get_short_name(), 'Jan')

    def test_is_superuser(self):
        """Test for method is_superuser
        - should return False for user object. """
        user = create_user()
        self.assertEqual(user.is_superuser, False)

    def test_is_staff(self):
        """Test for method is_staff - should return False for user object. """
        user = create_user()
        self.assertEqual(user.is_staff, False)

    def test_has_perm(self):
        """Test for method has_perm - should return False for user object. """
        user = create_user()
        self.assertEqual(user.has_perm(perm=None), False)

    def test_module_perms(self):
        """Test for method module_perms
        - should return False for user object. """
        user = create_user()
        self.assertEqual(user.has_module_perms(app_label=None), False)

    def test_get_last_login(self):
        """Test for method get_last_login
        - should return time of last login for user object.
        (time = timezone.now())
        """
        time = timezone.now()
        user = create_user(time=time)
        self.assertEqual(user.get_last_login(), time)

    def test_get_full_name(self):
        """Test for method get_full_name
        - should return full name of user object."""
        user = create_user()
        self.assertEqual(user.get_full_name(), 'Jan Kowalski')


class SuperUserTests(TestCase):
    """
    Tests for methods of User model.
    """
    def test_get_email(self):
        """Test for method get_mail
        - should return email of super_user object. """
        super_user = create_superuser()
        self.assertEqual(
            super_user.get_email, 'example_super_user_mail@gmail.com'
        )

    def test_get_short_name(self):
        """Test for method get_short_name
        - should return name of super_user object. """
        super_user = create_superuser()
        self.assertEqual(super_user.get_short_name(), 'Jan')

    def test_is_superuser(self):
        """Test for method is_superuser
        - should return True for super_user object. """
        super_user = create_superuser()
        self.assertEqual(super_user.is_superuser, True)

    def test_is_staff(self):
        """Test for method is_staff
        - should return True for super_user object. """
        super_user = create_superuser()
        self.assertEqual(super_user.is_staff, True)

    def test_has_perm(self):
        """Test for method has_perm
        - should return True for super_user object. """
        super_user = create_superuser()
        self.assertEqual(super_user.has_perm(perm=None), True)

    def test_module_perms(self):
        """Test for method module_perms
        - should return True for super_user object. """
        super_user = create_superuser()
        self.assertEqual(super_user.has_module_perms(app_label=None), True)

    def test_get_last_login(self):
        """Test for method get_last_login -
        should return time of last login for super_user object.
        (time = timezone.now())
        """
        time = timezone.now()
        super_user = create_superuser(time=time)
        self.assertEqual(super_user.get_last_login(), time)

    def test_get_full_name(self):
        """Test for method get_full_name
        - should return full name of super_user object."""
        super_user = create_superuser()
        self.assertEqual(super_user.get_full_name(), 'Jan Kowalski')
