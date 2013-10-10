from django.db import models


class Questionnaire(models.Model):
    """
    Contains questions that users answer on a daily basis. These questions are aggregated to compute CDAI scores.
    """
    liquid_stool = models.IntegerField()

    ABDOMINAL_PAIN_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )
    abdominal_pain = models.IntegerField(choices=ABDOMINAL_PAIN_CHOICES)

    GENERAL_WELL_BEING_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )
    general_well_being = models.IntegerField(choices=GENERAL_WELL_BEING_CHOICES)

    number_of_complications = models.IntegerField()

    taking_lomatil_or_opiates = models.BooleanField()

    ABDOMINAL_MASS_CHOICES = (
        (0, 'No'),
        (2, 'Maybe'),
        (5, 'Yes'),
    )
    presence_of_abdominal_mass = models.IntegerField(choices=ABDOMINAL_MASS_CHOICES)

    hematocrit = models.IntegerField()

    current_weight = models.IntegerField()

    user_profile = models.ManyToManyField('UserProfile', through='UserQuestionnaire')

    class Meta:
        """
        Meta options for the Questionnaire model.
        """
        app_label = 'Questionnaire'