from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Contains information related to the User model.
    """
    user = models.OneToOneField(User)

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)

    birth_date = models.DateField()

    # diagnosis month and year
    MONTHS = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )
    diagnosis_month = models.CharField(max_length=256, choices=MONTHS)
    diagnosis_year = models.IntegerField()

    # Location fields
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)

    standard_weight = models.IntegerField()

    treatments = models.TextField()

    class Meta:
        """
        Meta attributes for the UserProfile model.
        """
        app_label = 'Questionnaire'