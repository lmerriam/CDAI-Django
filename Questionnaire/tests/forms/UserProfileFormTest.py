import datetime
from django.test import TestCase
from ...forms import UserProfileForm
from ...models import User


class UserProfileFormTest(TestCase):
    """
    Contains unit tests for the UserProfileForm.
    """
    def setUp(self):
        """
        This method is run before each of the test methods below, and is used to setup test data. After each of the
        test methods below, a teardown method is run which purges this data. This has the effect of giving "clean" data
        to each test method.
        """
        self. user = User.objects.create_user(username='fredbob',
                                              first_name='Fred',
                                              last_name='Bob',
                                              email='fredbob@fakezzzz.com',
                                              password='foobar')

    def test_invalid_form(self):
        """
        Tests that an existing username doesn't validate, and that the passwords must match.
        """
        data = {
            'username': self.user.username,
            'first_name': 'Fred',
            'last_name': 'Bob',
            'email': 'fredbob@fakezzzz.com',
            'password': 'foobar',
            'confirm_password': 'foobar2',
            'gender': 'male',
            'birth_date': '01-01-1900',
            'diagnosis_month': 'january',
            'diagnosis_year': 1920,
            'city': 'Seattle',
            'state': 'Washington',
            'country': 'USA',
            'standard_weight': 150,
            'treatments': 'No current treatments'
        }
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ["That username is taken."])
        self.assertEqual(form.errors['__all__'], ["The passwords did not match."])

    def test_valid_user_profile_form(self):
        """
        Tests creating a form to make sure all data exists.
        """
        data = {
            'username': 'teddybear',
            'first_name': 'Fred',
            'last_name': 'Bob',
            'email': 'fredbob@fakezzzz.com',
            'password': 'foobar',
            'confirm_password': 'foobar',
            'gender': 'Male',
            'birth_date': '01/01/1900',
            'diagnosis_month': 'January',
            'diagnosis_year': 1920,
            'city': 'Seattle',
            'state': 'Washington',
            'country': 'USA',
            'standard_weight': 150,
            'treatments': 'No current treatments'
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())
        cleaned = form.cleaned_data
        self.assertEqual(cleaned['username'], data['username'])
        self.assertEqual(cleaned['first_name'], data['first_name'])
        self.assertEqual(cleaned['last_name'], data['last_name'])
        self.assertEqual(cleaned['email'], data['email'])
        self.assertEqual(cleaned['password'], data['password'])
        self.assertEqual(cleaned['gender'], data['gender'])
        self.assertEqual(cleaned['birth_date'], datetime.datetime.strptime(data['birth_date'], '%m/%d/%Y').date())
        self.assertEqual(cleaned['diagnosis_month'], data['diagnosis_month'])
        self.assertEqual(cleaned['diagnosis_year'], data['diagnosis_year'])
        self.assertEqual(cleaned['city'], data['city'])
        self.assertEqual(cleaned['state'], data['state'])
        self.assertEqual(cleaned['country'], data['country'])
        self.assertEqual(cleaned['standard_weight'], data['standard_weight'])
        self.assertEqual(cleaned['treatments'], data['treatments'])