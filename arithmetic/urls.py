from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'sources.arithmetic.views.home', name='arithmetic_home'),
    url(r'^coding/random/exercise/$',
        'sources.arithmetic.views.coding_exercise',
        name='arithmetic_coding_exercise'
        ),
    url(r'^coding/random/solution$',
        'sources.arithmetic.views.coding_solution',
        name='arithmetic_coding_solution'
        ),
    url(r'^decoding/random/exercise/$',
        'sources.arithmetic.views.decoding_exercise',
        name='arithmetic_decoding_exercise'
        ),
    url(r'^decoding/random/solution$',
        'sources.arithmetic.views.decoding_solution',
        name='arithmetic_decoding_solution'
        ),
)
