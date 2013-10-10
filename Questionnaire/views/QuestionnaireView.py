from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..forms import QuestionnaireForm
from ..models import UserProfile, Questionnaire, UserQuestionnaire


class QuestionnaireView(FormView):
    """
    View for filling out a questionnaire.
    """
    form_class = QuestionnaireForm
    template_name = 'Questionnaire/questionnaire.html'
    success_url = reverse_lazy("questionnaire_graph")

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, *args, **kwargs):
        """
        Dispatch method is over-ridden to allow restricting access to authorized users.
        """
        return super(QuestionnaireView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form, updated with the current user's profile.
        """
        kwargs = {'initial': self.get_initial()}
        data = self.request.POST.copy()
        data.update({'user_profile': UserProfile.objects.get(user__id=self.request.user.id)})
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': data,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        """
        If the form is valid, create the necessary objects and redirect to the supplied URL.
        """
        data = form.cleaned_data
        updated_data = data.copy()
        day = updated_data.pop('date')
        profile = form.data['user_profile']
        questionnaire, created = Questionnaire.objects.get_or_create(**updated_data)
        UserQuestionnaire.objects.create(user_profile=profile, questionnaire=questionnaire, day=day)
        return HttpResponseRedirect(self.get_success_url())