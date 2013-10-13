import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from ...models import User, UserProfile, Questionnaire, UserQuestionnaire


class LoginRedirectViewTest(TestCase):
    """
    Contains tests for the GraphView view.
    """
    def setUp(self):
        """
        Setup a user and a set of answered questions for the test.
        """
        self.user = User.objects.create_user(username="admin", password=1)
        profile_data = {
            "city": "Seattle",
            "diagnosis_year": 2000,
            "gender": "Male",
            "standard_weight": 150,
            "diagnosis_month": "January",
            "state": "Washington",
            "user": self.user,
            "country": "USA",
            "birth_date": "1920-01-01",
            "treatments": "None"
        }
        self.profile = UserProfile.objects.create(**profile_data)
        questionnaire_data = {
            "general_well_being": 3,
            "number_of_complications": 1,
            "hematocrit": 4,
            "taking_lomatil_or_opiates": True,
            "liquid_stool": 5,
            "abdominal_pain": 3,
            "presence_of_abdominal_mass": 5,
            "current_weight": 200
        }
        self.questionnaire = Questionnaire.objects.create(**questionnaire_data)

    def test_unauthorized_access(self):
        """
        Make sure users must be logged in to access the view.
        """
        self.client = Client()
        response = self.client.get(reverse("login_redirect"))
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("login_redirect"))

    def test_questioned_answered_today(self):
        """
        Tests getting the page with a user who has already answered questions for the day.
        """
        self.user_questionnaire = UserQuestionnaire.objects.create(
            user_profile=self.profile,
            questionnaire=self.questionnaire,
            day=datetime.datetime.today()
        )
        self.client = Client()
        login = self.client.login(username="admin", password="1")
        self.assertTrue(login)
        response = self.client.get(reverse("login_redirect"))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'http://testserver' + reverse("questionnaire_graph"))

    def test_questioned_not_answered_today(self):
        """
        Tests getting the page with a user who has already answered questions for the day.
        """
        self.user_questionnaire = UserQuestionnaire.objects.create(
            user_profile=self.profile,
            questionnaire=self.questionnaire,
            day=datetime.datetime.today() - datetime.timedelta(days=1)
        )
        self.client = Client()
        login = self.client.login(username="admin", password="1")
        self.assertTrue(login)
        response = self.client.get(reverse("login_redirect"))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'http://testserver' + reverse("questionnaire"))

