from django.conf.urls import patterns, url

general_chain_pattern = "/".join([
    r'^([^/]+)',
    r'([^/]+)',
    r'([-.0-9\[\],]+)',
    r'(\d+/)?$',
]
)

urlpatterns = patterns(
    '',
    url(r'^$', 'sources.views.home', name='source_home'),
    url(r'^(\d+)/$', 'sources.views.source_detail',
        name='source_detail'),
    url(r'^(\d+)/(\d+)/$', 'sources.views.sourcestat_default',
        name='sourcestat_default'),
    url(r'^(?P<source_number>\d+)/(?P<code_number>\d+)/'
        r'(?P<channel>[\[\],.0-9]+)/$',
        'sources.views.simple_chain',
        name='simple_chain'),
    url(
        general_chain_pattern,
        'sources.views.general_chain',
        name='general_chain'
    ),
)
