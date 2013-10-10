from django.conf.urls import patterns, url
from views import QuestionnaireView, GraphView

urlpatterns = patterns('Questionnaire.views',
                       url(r'^$', QuestionnaireView.as_view(), name='questionnaire'),
                       url(r'^graph$', GraphView.as_view(), name='questionnaire_graph'),

)