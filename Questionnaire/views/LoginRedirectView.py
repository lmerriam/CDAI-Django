import datetime
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from ..models import UserQuestionnaire


class LoginRedirectView(RedirectView):
    """
    View for redirecting the user after logging in.
    """
    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, *args, **kwargs):
        """
        If the user has already answered questions today, redirect to the graph page. Otherwise, redirect to the
        questions. Only logged in users can access this view.
        """
        tmp_user = User.objects.get(id=self.request.user.id)
        try:
            UserQuestionnaire.objects.get(user_profile__user=tmp_user, day=datetime.datetime.today())
            self.url = reverse_lazy("questionnaire_graph")
        except ObjectDoesNotExist:
            self.url = reverse_lazy("questionnaire")
        return super(LoginRedirectView, self).dispatch(*args, **kwargs)