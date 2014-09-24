from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'sources.views.home', name='source_home'),
    url(r'^(\d+)/$', 'sources.views.source_detail',
        name='source_detail'),
    url(r'^(\d+)/(\d+)/$', 'sources.views.sourcestat_default',
        name='sourcestat_default'),
    url(r'^chain/(?P<source_number>\d+)/(?P<code_number>\d+)/(?P<chain>[\[\],.0-9]+)/$',
        'sources.views.chain',
        name='sourcestat_default'),
)
