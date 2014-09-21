from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'sources.views.home', name='source_home'),
    url(r'^(\d+)/$', 'sources.views.sourcestat_detail',
        name='sourcestat_detail'),
)
