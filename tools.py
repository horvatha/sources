import coding
import itertools


def get_distribution_and_symbols(source_description):
    symbols = []
    distribution = []
    for i in source_description.split():
        symbol, probablity = i.split(':')
        symbols.append(symbol)
        probablity = float(probablity)
        distribution.append(probablity)
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
    if isinstance(channel_description, str) and \
            channel_description.startswith("["):
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
    splitted_texts = coding.diff.diff(text1, text2)
    return [alternate_match_diff_spans(text) for text in splitted_texts]
