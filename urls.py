from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'djancoding.views.home', name='home'),
    url(r'^(\d+)/$', 'djancoding.views.sourcestat_detail',
        name='sourcestat_detail'),
)
