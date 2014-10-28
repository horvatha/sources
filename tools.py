import coding
import itertools
from fractions import Fraction


class Argument_URLizer:
    table = (
        ('/', 'r'),
    )

    def to_url(self, arguments):
        for from_, to in self.table:
            arguments = arguments.replace(from_, to)
        return arguments

    def from_url(self, arguments):
        for to, from_ in self.table:
            arguments = arguments.replace(from_, to)
        return arguments


def get_distribution_and_symbols(source_description):
    symbols = []
    distribution = []
    for i in source_description.split():
        symbol, probability = i.split(':')

        symbols.append(symbol)

        if '/' in probability:
            numerator, denominator = probability.split("/")
            probability = Fraction(int(numerator), int(denominator))
        else:
            probability = float(probability)
        distribution.append(probability)
    return distribution, "".join(symbols)


def get_source(source_description):
    if source_description.startswith("fix."):
        return coding.FixSource(source_description[4:])
    distribution, symbols = get_distribution_and_symbols(source_description)
    return coding.Source(distribution, symbols=symbols)


def get_code(code_description):
    code_description = code_description.replace(",", "  ")
    parts = code_description.split()
    list_of_pairs = [part.split(':', 1) for part in parts]
    symbols, codes = zip(*list_of_pairs)
    return coding.Code(" ".join(codes), symbols="".join(symbols))


def get_channel(channel_description):
    return coding.Channel(normalize(channel_description))


def normalize(channel_description):
    if isinstance(channel_description, str):
        if channel_description.startswith("["):
            channel_description = eval(channel_description)
        elif "." in channel_description:
            channel_description = eval(channel_description)
    return channel_description


def span_with_class(text, class_):
    if not text:
        return ''
    return '<span class="{}">{}</span>'.format(
        class_, text
    )


def match_span(text):
    return span_with_class(text, 'match')


def differ_span(text):
    return span_with_class(text, 'differ')


def alternate_match_diff_spans(text_list):
    span_function = itertools.cycle([match_span, differ_span])
    return "".join(
        [next(span_function)(text) for text in text_list]
    )


def color_diff(text1, text2):
    diff_function = coding.diff.diff
    if isinstance(text1, coding.Bits):
        diff_function = coding.diff.bitdiff
    if isinstance(text1, coding.Message) or isinstance(text1, coding.Bits):
        text1 = text1.message
        text2 = text2.message
    splitted_texts = diff_function(text1, text2)
    return [alternate_match_diff_spans(text) for text in splitted_texts]


def colorize_and_linearize_outputs(outputs):
    items = []
    for output_pair in reversed(outputs):
        down_length, up_length = [len(i) for i in output_pair]
        colored_down, colored_up = color_diff(*output_pair)
        down = (down_length, colored_down)
        up = (up_length, colored_up)
        items.insert(0, down)
        items.append(up)
    return tuple(items)
