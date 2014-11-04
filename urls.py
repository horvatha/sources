from django.conf.urls import patterns, url

general_chain_pattern = "/".join([
    r'^(?P<source_description>[^/]+)',
    r'(?P<code_description>[^/]+)',
    r'(?P<channel_description>[-.0-9\[\],]+)',
    r'(?P<hamming_block_length>\d+)/$',
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
        r'(?P<hamming_block_length>\d+)/$',
        'sources.views.simple_chain',
        name='simple_chain'),
    url(general_chain_pattern,
        'sources.views.general_chain',
        name='general_chain'),

    url(r'^change_source/([^/]+)/([^/]+)([^/]+)//(\d+)/$',
        'sources.views.change_communication_system',
        {"element_to_change": "source_description"},
        name='change_source'),
    url(r'^change_code/([^/]+)/([^/]+)([^/]+)//(\d+)/$',
        'sources.views.change_communication_system',
        {"element_to_change": "code_description"},
        name='change_code'),
    url(r'^change_error_handler/([^/]+)/([^/]+)/([^/]+)/(\d+)/$',
        'sources.views.change_communication_system',
        {"element_to_change": "hamming_block_length"},
        name='change_error_handler'),
    url(r'^change_channel/([^/]+)/([^/]+)/([^/]+)/(\d+)/$',
        'sources.views.change_communication_system',
        {"element_to_change": "channel_description"},
        name='change_channel'),
)
