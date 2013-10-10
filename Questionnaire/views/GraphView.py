from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from ..models import UserQuestionnaire, UserProfile
from ..api import compute_score


class GraphView(TemplateView):
    """
    View for rendering the graph object.
    """
    template_name = "Questionnaire/graph.html"

    @method_decorator(login_required(login_url=reverse_lazy("login")))
    def dispatch(self, *args, **kwargs):
        """
        Dispatch method is over-ridden to allow restricting access to authorized users.
        """
        return super(GraphView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add the users scores to the context.
        """
        context = super(GraphView, self).get_context_data()
        user = self.request.user
        profile = UserProfile.objects.get(user__id=user.id)
        user_questionnaires = UserQuestionnaire.objects.filter(user_profile=profile)
        data = {}
        for q in user_questionnaires:
            data[q.day] = compute_score(q)
        context['data'] = data
        return context