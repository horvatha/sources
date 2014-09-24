from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from sources.views import home, source_detail, code_stat, sources
from coding import Source, Code

source = Source([.25]*4)
code = Code("00 01 10 11")


class SourceHomePageTest(TestCase):
    def test_source_url_resolves_home_page_view(self):
        found = resolve("/sources/")
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        response = home(HttpRequest())
        expected_html = render_to_string('sources/source.html',
                                         {"sources": sources})
        self.assertEqual(response.content.decode(), expected_html)


class SourceDetailPageTest(TestCase):
    def test_source_url_resolves_source_detail_view(self):
        found = resolve("/sources/1/")
        self.assertEqual(found.func, source_detail)

    def test_source_detail_returns_correct_html(self):
        response = source_detail(HttpRequest(), 1)
        source_name, source, code_list = sources[1]
        expected_html = render_to_string(
            'sources/sourcestat_detail.html',
            {
                "source_name": source_name,
                "source": source,
                "code_list": code_list,
                "id": 1
            }
        )
        self.assertEqual(response.content.decode(), expected_html)


class CodeStatTest(TestCase):
    "Testing code_stat_test function."
    def test_code_stat_returns_proper_values(self):
        known_values = (
            (
                (source, code, 100, 50), (200, 200, 200, 2, 2, 2, 100, 50),
            ),
        )
        for args, result in known_values:
            self.assertEqual(code_stat(*args), result)
