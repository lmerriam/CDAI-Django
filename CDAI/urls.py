from django.conf.urls import patterns, include, url
from Questionnaire.views import UserProfileView, LoginRedirectView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'Questionnaire/login.html'}, name="login"),
    url(r'^login_redirect/$', LoginRedirectView.as_view(), name='login_redirect'),
    url(r'^questionnaire/', include('Questionnaire.urls')),
    url(r'^user-profile$', UserProfileView.as_view(), name="cdai_user_profile"),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)