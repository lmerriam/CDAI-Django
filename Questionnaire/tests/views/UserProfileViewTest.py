from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from ...models import User, UserProfile


class UserProfileViewTest(TestCase):
    """
    Contains tests for the UserProfileView view.
    """
    fixtures = ['test_data.json']

    def test_user_profile_view(self):
        """
        Tests getting the page to make sure the url resolves correctly.
        """
        self.client = Client()
        response = self.client.get(reverse("cdai_user_profile"))
        self.assertEqual(200, response.status_code)

    def test_invalid_form(self):
        """
        Tests invalid form requests.
        """
        data = {
            'username': 'admin',
            'first_name': 'Fred',
            'last_name': 'Bob',
            'email': 'fredbob@fakezzzz.com',
            'password': 'foobar',
            'confirm_password': 'foobar',
            'gender': 'Male',
            'birth_date': '1900-01-01',
            'diagnosis_month': 'January',
            'diagnosis_year': 1920,
            'city': 'Seattle',
            'state': 'Washington',
            'country': 'USA',
            'standard_weight': 150,
            'treatments': 'No current treatments'
        }
        self.client = Client()
        # test existing username
        response = self.client.post(reverse("cdai_user_profile"), data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context['form']['username'].errors, [u'That username is taken.'])
        # test passwords do not match
        data['password'] = 'foo'
        response = self.client.post(reverse("cdai_user_profile"), data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context['form'].errors['__all__'], [u'The passwords did not match.'])
        # test no data
        fields = [key for key, value in data.iteritems()]
        data = {}
        response = self.client.post(reverse("cdai_user_profile"), data)
        self.assertEqual(200, response.status_code)
        for f in fields:
            self.assertEqual(response.context['form'][f].errors, [u'This field is required.'])

    def test_valid_form(self):
        """
        Tests a valid form request.
        """
        data = {
            'username': 'teddybear',
            'first_name': 'Fred',
            'last_name': 'Bob',
            'email': 'fredbob@fakezzzz.com',
            'password': 'foobar',
            'confirm_password': 'foobar',
            'gender': 'Male',
            'birth_date': '1900-01-01',
            'diagnosis_month': 'January',
            'diagnosis_year': 1920,
            'city': 'Seattle',
            'state': 'Washington',
            'country': 'USA',
            'standard_weight': 150,
            'treatments': 'No current treatments'
        }
        self.client = Client()
        response = self.client.post(reverse("cdai_user_profile"), data)
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("questionnaire"))
        user = User.objects.get(username=data['username'],
                                first_name=data['first_name'],
                                last_name=data['last_name'],
                                email=data['email'])
        self.assertTrue(user.check_password('foobar'))
        UserProfile.objects.get(user=user,
                                gender=data['gender'],
                                birth_date=data['birth_date'],
                                diagnosis_month=data['diagnosis_month'],
                                diagnosis_year=data['diagnosis_year'],
                                city=data['city'],
                                state=data['state'],
                                country=data['country'],
                                standard_weight=data['standard_weight'],
                                treatments=data['treatments']
        )