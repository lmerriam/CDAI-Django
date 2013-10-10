from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from ..forms import UserProfileForm
from ..models import User, UserProfile


class UserProfileView(FormView):
    """
    View for creating a user profile.
    """
    form_class = UserProfileForm
    template_name = 'Questionnaire/user_profile.html'

    def get_success_url(self):
        """
        Returns the supplied success URL. After creating a profile, take the user to the login page. After logging in,
        take them to the questionnaire.
        """
        return str(reverse_lazy("login")) + "?next=" + str(reverse_lazy("questionnaire"))

    def form_valid(self, form):
        """
        If the form is valid, create the user and user profile objects and redirect to the questionnaire.
        """
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        gender = form.cleaned_data.get('gender')
        birth_date = form.cleaned_data.get('birth_date')
        diagnosis_month = form.cleaned_data.get('diagnosis_month')
        diagnosis_year = form.cleaned_data.get('diagnosis_year')
        city = form.cleaned_data.get('city')
        state = form.cleaned_data.get('state')
        country = form.cleaned_data.get('country')
        standard_weight = form.cleaned_data.get('standard_weight')
        treatments = form.cleaned_data.get('treatments')
        user = User.objects.create_user(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        password=password)
        UserProfile.objects.create(user=user,
                                   gender=gender,
                                   birth_date=birth_date,
                                   diagnosis_month=diagnosis_month,
                                   diagnosis_year=diagnosis_year,
                                   city=city,
                                   state=state,
                                   country=country,
                                   standard_weight=standard_weight,
                                   treatments=treatments)
        return HttpResponseRedirect(self.get_success_url())