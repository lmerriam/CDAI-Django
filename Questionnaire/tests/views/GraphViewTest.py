from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from ...models import User, UserProfile, Questionnaire, UserQuestionnaire
from ...api import compute_score


class GraphViewTest(TestCase):
    """
    Contains tests for the GraphView view.
    """
    # load test data from the fixture. fixture is reloaded before each test method.
    fixtures = ['test_data.json', 'questionnaires.json']

    def test_graph_view(self):
        """
        Tests getting the page to make sure the url resolves correctly and the context contains the correct data.
        """
        self.client = Client()
        login = self.client.login(username="tempuser", password="1")
        self.assertTrue(login)
        user = User.objects.get(username='tempuser')
        profile = UserProfile.objects.get(user__id=user.id)
        user_questionnaires = UserQuestionnaire.objects.filter(user_profile=profile)
        data = []
        for q in user_questionnaires:
            data.append([q.day, compute_score(q)])
        response = self.client.get(reverse("questionnaire_graph"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context['data'], data)

    def test_unauthorized_access(self):
        """
        Make sure users must be logged in to access the view.
        """
        self.client = Client()
        response = self.client.get(reverse("questionnaire_graph"))
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("questionnaire_graph"))