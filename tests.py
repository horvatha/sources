from django.core.urlresolvers import resolve, Resolver404
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from sources.views import (home, source_detail, code_stat, sources,
                           simple_chain, general_chain)
from coding import FixSource, Source, Code, Channel, Chain
from sources import tools
from collections import OrderedDict

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


url_start = '/sources/fix:I_LOVE_YOU/'
code_desc = \
    'I:0000,A:000100,D:000101,U:00011,V:001,Y:0100,L:0101,O:011,_:10,E:11'


class ChainPageTest(TestCase):
    url_dict = {
        simple_chain: (
            "/sources/3/1/0/",
            "/sources/3/1/[6]/",
            "/sources/3/1/[3,6]/",
            "/sources/3/1/0.1/",
            "/sources/3/1/0.1/",
        ),
        general_chain: (
            "/sources/fix:3/1/0/",
            url_start + code_desc + "/0/",
            url_start + code_desc + "/2/",
            url_start + code_desc + "/[21]/",
            url_start + code_desc + "/[21,-1]/",
            url_start + code_desc + "/0.5/",
        ),
    }

    bad_urls = (
        url_start + code_desc + "/0/x5/",
    )

    def test_simple_chain_url_resolves_chain_view(self):
        for func, urls in self.url_dict.items():
            for url in urls:
                found = resolve(url)
                self.assertEqual(found.func, func)

    def test_bad_urls_does_not_resolve(self):
        for url in self.bad_urls:
            with self.assertRaises(Resolver404):
                resolve(url)

    def test_simple_chain_returns_correct_html(self):
        args = source_number, code_number, channel = 3, 1, 0
        response = simple_chain(HttpRequest(), *args)
        source_name, source, code_list = sources[source_number]
        code = code_list[code_number]
        chain_ = Chain(source, code, Channel(channel))
        chain_.run()
        run = chain_.runs[0]
        expected_html = render_to_string(
            'sources/chain.html',
            {
                "source_name": source_name,
                "source": source,
                "code": code,
                "source_number": source_number,
                "code_number": code_number,
                "channel": Channel(channel),
                "run": run,
            }
        )
        self.assertEqual(response.content.decode(), expected_html)
        self.assertContains(response, "hibament")
        self.assertContains(response, "<table")
        self.assertContains(response, "<tr><td>")


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


class ToolsTest(TestCase):
    def test_get_distribution_and_symbols(self):
        known_values = {
            "X:.2 B:.8": ([.2, .8], "XB"),
        }
        for source_description, values in known_values.items():
            expected_distribution, expected_symbols = values
            distribution, symbols = tools.get_distribution_and_symbols(
                source_description)
            self.assertEqual(distribution, expected_distribution)
            self.assertEqual(symbols, expected_symbols)

    def test_get_source(self):
        known_values = {
            "fix.ALABAMA": FixSource("ALABAMA"),
        }
        for source_description, expected_source in known_values.items():
            source = tools.get_source(source_description)
            self.assertEqual(repr(source), repr(expected_source))

    def test_get_code(self):
        known_values = {
            "X:00 Y:01 Z:10": Code("00 01 10", symbols="XYZ"),
            "X:00,Y:01,Z:10": Code("00 01 10", symbols="XYZ"),
            "X:00, Y:01, Z:10": Code("00 01 10", symbols="XYZ"),
        }
        for code_description, expected_code in known_values.items():
            code = tools.get_code(code_description)
            self.assertEqual(repr(code), repr(expected_code))

    def test_normalize(self):
        known_values = {
            "[21]": [21],
            "0.5": "0.5",
            0.5: 0.5,
        }
        for channel_description, expected in known_values.items():
            self.assertEqual(tools.normalize(channel_description), expected)

    def test_color_diff(self):
        known_values = OrderedDict([
            (
                ('AAABBB', 'AAABBB'),
                (
                    '<span class="match">AAABBB</span>',
                    '<span class="match">AAABBB</span>'
                )
            ),
            (
                ('AAABB', 'AAABBB'),
                (
                    '<span class="match">AAABB</span>',
                    '<span class="match">AAABB</span><span class="differ">B</span>'
                )
            ),
            (
                ('AAABBD', 'AAABBB'),
                (
                    '<span class="match">AAABB</span><span class="differ">D</span>',
                    '<span class="match">AAABB</span><span class="differ">B</span>'
                )
            ),
            (
                ('AABDD', 'AACDD'),
                (
                    '<span class="match">AA</span><span class="differ">B</span><span class="match">DD</span>',
                    '<span class="match">AA</span><span class="differ">C</span><span class="match">DD</span>'
                )
            ),
            (
                ('XAABDD', 'AACDD'),
                (
                    "".join([
                        '<span class="differ">X</span>',
                        '<span class="match">AA</span>',
                        '<span class="differ">B</span>',
                        '<span class="match">DD</span>'
                    ]),
                    "".join([
                        '<span class="match">AA</span>',
                        '<span class="differ">C</span>',
                        '<span class="match">DD</span>'
                    ])
                )
            ),
            # (('AAABBB', 'AABBBB'),
            #  (('', 'A', 'AABBB'), ('AABBB', 'B'))),
            # (('AAABBB', 'AAAABB'),
            #  (('AAABB', 'B'), ('', 'A', 'AAABB'))),
            # (('AABB', 'AAAB'),
            #  (('AAB', 'B'), ('', 'A', 'AAB'))),
        ])
        for args, result in known_values.items():
            self.assertEqual(tools.color_diff(*args), list(result))

    def test_can_create_span_with_class(self):
        known_values = OrderedDict([
            (
                ('AAABBB', 'match'),
                '<span class="match">AAABBB</span>'
            ),
            (
                ('AB', 'differ'),
                '<span class="differ">AB</span>'
            ),
            (
                ('', 'match'),
                ''
            ),
        ])
        for args, result in known_values.items():
            self.assertEqual(tools.span_with_class(*args), result)

    def test_can_create_differing_and_matching_text(self):
        known_values = OrderedDict([
            (
                'AAABBB',
                (
                    '<span class="match">AAABBB</span>',
                    '<span class="differ">AAABBB</span>'
                )
            ),
            (
                '',
                ('', '')
            ),
        ])
        for text, results in known_values.items():
            self.assertEqual(tools.match_span(text), results[0])
            self.assertEqual(tools.differ_span(text), results[1])
