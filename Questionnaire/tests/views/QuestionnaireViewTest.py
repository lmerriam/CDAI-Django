import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from ...models import User, UserProfile, Questionnaire, UserQuestionnaire


class QuestionnaireViewTest(TestCase):
    """
    Contains tests for the QuestionnaireView view.
    """
    # load test data from the fixture. fixture is reloaded before each test method.
    fixtures = ['test_data.json']

    def test_questionnaire_view(self):
        """
        Tests getting the page to make sure the url resolves correctly.
        """
        self.client = Client()
        login = self.client.login(username="admin", password="1")
        self.assertTrue(login)
        response = self.client.get(reverse("questionnaire"))
        self.assertEqual(200, response.status_code)

    def test_unauthorized_access(self):
        """
        Make sure users must be logged in to access the view.
        """
        self.client = Client()
        response = self.client.get(reverse("questionnaire"))
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("questionnaire"))

    def test_invalid_form(self):
        """
        Tests invalid form requests.
        """
        self.client = Client()
        login = self.client.login(username="admin", password="1")
        self.assertTrue(login)
        fields = ['liquid_stool', 'abdominal_pain', 'general_well_being', 'number_of_complications',
                  'presence_of_abdominal_mass', 'current_weight', 'hematocrit']

        # tests no data
        data = {}
        response = self.client.post(reverse("questionnaire"), data)
        self.assertEqual(200, response.status_code)
        for f in fields:
            self.assertEqual(response.context['form'][f].errors, [u'This field is required.'])

    def test_valid_form(self):
        """
        Tests a valid form request.
        """
        data = {
            'liquid_stool': 10,
            'abdominal_pain': 2,
            'general_well_being': 3,
            'number_of_complications': 3,
            'taking_lomatil_or_opiates': True,
            'presence_of_abdominal_mass': 5,
            'hematocrit': 42,
            'current_weight': 130,
            'date': '1900-01-01',
        }
        self.client = Client()
        login = self.client.login(username="admin", password="1")
        self.assertTrue(login)
        response = self.client.post(reverse("questionnaire"), data)
        self.assertRedirects(response, reverse("questionnaire_graph"))
        user = User.objects.get(username='admin')
        profile = UserProfile.objects.get(user=user)
        user_questionnaire = UserQuestionnaire.objects.get(user_profile=profile, day=data['date'])
        questions = Questionnaire.objects.get(id=user_questionnaire.questionnaire.id)
        data.pop('date')
        for key, value in data.iteritems():
            self.assertEqual(getattr(questions, key), data[key])

    def test_valid_form_with_no_date(self):
        """
        Tests a valid form request with no date to ensure it defaults to the current day.
        """
        data = {
            'liquid_stool': 10,
            'abdominal_pain': 2,
            'general_well_being': 3,
            'number_of_complications': 3,
            'taking_lomatil_or_opiates': True,
            'presence_of_abdominal_mass': 5,
            'hematocrit': 42,
            'current_weight': 130,
        }
        self.client = Client()
        login = self.client.login(username="admin", password="1")
        self.assertTrue(login)
        response = self.client.post(reverse("questionnaire"), data)
        self.assertRedirects(response, reverse("questionnaire_graph"))
        today = datetime.date.today()
        user = User.objects.get(username='admin')
        profile = UserProfile.objects.get(user=user)
        user_questionnaire = UserQuestionnaire.objects.get(user_profile=profile, day=today)
        questions = Questionnaire.objects.get(id=user_questionnaire.questionnaire.id)
        for key, value in data.iteritems():
            self.assertEqual(getattr(questions, key), data[key])