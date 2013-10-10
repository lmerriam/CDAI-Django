import datetime
from django import forms
from ..models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    """
    Form for rendering a questionnaire, including custom widgets, classes, and attributes.
    """
    def __init__(self, *args, **kwargs):
        """
        Add fields for the many to many model, UserQuestionnaire, that links a user to a questionnaire.
        """
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.DateField(required=False)

    def clean_date(self):
        """
        If the date is empty, default it to today.
        """
        date = self.cleaned_data.get('date')
        if not date:
            date = datetime.date.today()
        return date

    class Meta:
        """
        Meta options.
        """
        model = Questionnaire
        exclude = ['user_profile']