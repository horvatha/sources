from django.core.urlresolvers import resolve, Resolver404
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from sources.views import (home, source_detail, code_stat, sources,
                           simple_chain, general_chain, get_fix_source,
                           fix_sources, urlizer)
from sources.arithmetic import views
from coding import FixSource, Source, Code, Channel, Chain
import coding
from sources import tools
from collections import OrderedDict
import re

source = Source([.25]*4)
code = Code("00 01 10 11")

fix_source_chain = Chain(
    FixSource('ALABAMA'),
    tools.get_code('A:0 B:10 L:110 M:111'),
    Channel([2])
)
fix_source_chain.run()
fix_source_run = fix_source_chain.runs[0]
outputs = fix_source_run.outputs
# print(
#     outputs,
#     [tools.color_diff(*[o.message for o in output]) for output in outputs],
#     sep='\n'
# )


def remove_table_data(text):
    lines = text.splitlines()
    span = re.compile("<td>.*?</td>")
    new_text = []
    for line in lines:
        new_line = span.sub("<td></td>", line)
        new_text.append(new_line)
    return "\n".join(new_text)


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
        args = source_number, code_number, channel_description = 3, 1, 0
        response = simple_chain(HttpRequest(), *args)
        source_name, source, code_list = sources[source_number]
        code = code_list[code_number-1]
        channel = Channel(channel_description)
        chain_ = Chain(source, code, channel)
        chain_.run()
        run = chain_.runs[0]
        expected_html = render_to_string(
            'sources/chain.html',
            {
                "source": source,
                "source_description": urlizer.to_url(str(source)),
                "code": str(code),
                "channel": channel,
                "linearized_outputs":
                    tools.colorize_and_linearize_outputs(run.outputs),
                "fix_source":
                    get_fix_source(source.symbols, fix_sources)
            }
        )
        html = response.content.decode()
        self.assertEqual(remove_table_data(html),
                         remove_table_data(expected_html))
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
    urlizer_known_values = (
        ("A:1/4 B:1/4 C:1/4 D:1/4", "A:1r4 B:1r4 C:1r4 D:1r4"),
        ("A:0.1 B:0.7 C:0.2", "A:0.1 B:0.7 C:0.2"),
    )

    def test_argument_URLizer_decoder_returns_proper_values(self):
        urlizer = tools.Argument_URLizer()
        for from_, to in self.urlizer_known_values:
            self.assertEqual(urlizer.to_url(from_), to)

    def test_argument_URLizer_coder_returns_proper_values(self):
        urlizer = tools.Argument_URLizer()
        for to, from_ in self.urlizer_known_values:
            self.assertEqual(urlizer.from_url(from_), to)

    def test_get_distribution_and_symbols(self):
        known_values = {
            "X:.2 B:.8": ([.2, .8], "XB"),
            "X:1/4 B:3/4": ([1/4, 3/4], "XB"),
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

                    '<span class="match">AAABB</span>'
                    '<span class="differ">B</span>'
                )
            ),
            (
                ('AAABBD', 'AAABBB'),
                (
                    '<span class="match">AAABB</span>'
                    '<span class="differ">D</span>',

                    '<span class="match">AAABB</span>'
                    '<span class="differ">B</span>'
                )
            ),
            (
                ('AABDD', 'AACDD'),
                (
                    '<span class="match">AA</span>'
                    '<span class="differ">B</span>'
                    '<span class="match">DD</span>',

                    '<span class="match">AA</span>'
                    '<span class="differ">C</span>'
                    '<span class="match">DD</span>'
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
            (
                (coding.Bits('01011'), coding.Bits('00111')),
                (
                    '<span class="match">0</span>'
                    '<span class="differ">10</span>'
                    '<span class="match">11</span>',

                    '<span class="match">0</span>'
                    '<span class="differ">01</span>'
                    '<span class="match">11</span>'
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

    def test_can_colorize_and_linearize_outputs(self):
        known_values = (
            (
                fix_source_run.outputs,
                (
                    (
                        7,
                        '<span class="match">A</span>'
                        '<span class="differ">L</span>'
                        '<span class="match">ABAMA</span>'
                    ),
                    (
                        12,
                        '<span class="match">0</span>'
                        '<span class="differ">1</span>'
                        '<span class="match">1001001110</span>'
                    ),
                    (
                        12,
                        '<span class="match">0</span>'
                        '<span class="differ">0</span>'
                        '<span class="match">1001001110</span>'
                    ),
                    (
                        8,
                        '<span class="match">A</span>'
                        '<span class="differ">AB</span>'
                        '<span class="match">ABAMA</span>'
                    ),
                )
            ),
        )
        for outputs, result in known_values:
            self.assertEqual(tools.colorize_and_linearize_outputs(outputs),
                             result)


class ArithmeticHomePageTest(TestCase):
    def test_source_url_resolves_home_page_view(self):
        found = resolve("/arithmetic/")
        self.assertEqual(found.func, views.home)

    def test_home_page_returns_correct_html(self):
        response = views.home(HttpRequest())
        expected_html = render_to_string('arithmetic/home.html', {})
        self.assertEqual(response.content.decode(), expected_html)


class ArithmeticCodingExercisePageTest(TestCase):
    def test_source_url_resolves_home_page_view(self):
        found = resolve("/arithmetic/coding/random/exercise/")
        self.assertEqual(found.func, views.coding_exercise)

    def test_home_page_returns_correct_html(self):
        response = views.coding_exercise(HttpRequest())
        expected_html = render_to_string('arithmetic/coding_exercise.html', {})
        self.assertEqual(response.content.decode(), expected_html)
