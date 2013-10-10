import datetime
from django.test import TestCase
from ...forms import QuestionnaireForm
from ...models import User


class QuestionnaireFormTest(TestCase):
    """
    Contains unit tests for the QuestionnaireForm.
    """
    def setUp(self):
        """
        This method is run before each test method below, and is used to create test data. The data is purged using a
        teardown method that is run after each test method below.  This has the effect of giving each test "clean"
        data to work with.
        """
        self. user = User.objects.create_user(username='fredbob',
                                              first_name='Fred',
                                              last_name='Bob',
                                              email='fredbob@fakezzzz.com',
                                              password='foobar')

    def test_empty_date(self):
        """
        Tests that an empty date parameter defaults the date to the current day.
        """
        data = {
            'liquid_stool': 10,
            'abdominal_pain': 2,
            'general_well_being': 3,
            'number_of_complications': 3,
            'taking_lomatil_or_opiates': True,
            'presence_of_abdominal_mass': 5,
            'current_weight': 130,
            'hematocrit': 42,
        }
        form = QuestionnaireForm(data=data)
        print form.errors
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['date'], datetime.date.today())

    def test_valid_questionnaire_form(self):
        """
        Tests creating a form to make sure all data exists.
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
        form = QuestionnaireForm(data=data)
        self.assertTrue(form.is_valid())
        cleaned = form.cleaned_data
        for key, value in data.iteritems():
            if key != 'date':
                self.assertEqual(cleaned[key], data[key])
            else:
                self.assertEqual(cleaned[key], datetime.datetime.strptime(data[key], '%Y-%m-%d').date())