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
        r'(?P<channel_description>[\[\],.0-9]+)/'
        r'(?P<hamming_block_length>\d+/)?$',
        'sources.views.simple_chain',
        name='simple_chain'),
    url(general_chain_pattern,
        'sources.views.general_chain',
        name='general_chain'),

    url(r'^change_source/([^/]+)/([^/]+)/$',
        'sources.views.change_source',
        name='change_source'),
    url(r'^change_code/([^/]+)/([^/]+)/$',
        'sources.views.change_code',
        name='change_code'),
    url(r'^change_error_handler/([^/]+)/([^/]+)/$',
        'sources.views.change_error_handler',
        name='change_error_handler'),
    url(r'^change_channel/([^/]+)/([^/]+)/([^/]+/?[^/]?)/$',
        'sources.views.change_communication_system',
        {"element_to_change": "channel"},
        name='change_channel'),
)
