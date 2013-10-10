from django.db import models
from . import UserProfile, Questionnaire


class UserQuestionnaire(models.Model):
    """
    Links users to a set of answered questions, and includes the day the questions are being answered for.
    """
    user_profile = models.ForeignKey(UserProfile)
    questionnaire = models.ForeignKey(Questionnaire)
    day = models.DateField()

    class Meta:
        """
        Defines constraints and other meta information for the model. Users should only answer the questions once per
        day, and the unique together constraint enforces this restriction.
        """
        unique_together = ('user_profile', 'day')
        app_label = 'Questionnaire'