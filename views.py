from django.shortcuts import render, redirect
import coding
import collections
from sources import tools
from fractions import Fraction

kenobi_symbols = "DAUIYLVO_E"
sources = {
    1: (
        "Egyforma valószínűségű jelekből álló forrás",
        coding.Source(4),
        [coding.Code("00 01 10 11"), coding.Code("0 11 101 100")]
    ),
    2: (
        "Eltérő valószínűségű jelekből álló forrás",
        coding.Source([Fraction(1, 2), Fraction(1, 4),
                       Fraction(1, 8), Fraction(1, 8)]),
        [
            coding.Code("00 01 10 11"),
            coding.Code("0 11 101 100"),
            coding.Code("101 100 11 0"),
        ]
    ),
    3: (
        "A Kenobis példában szereplő forrás",
        coding.Source([.01, .01, .03, .04, .05, .06, .09, .13, .25, .33],
                      symbols=kenobi_symbols),
        [
            coding.Code("000101 000100 00011 0000 0100 0101 001 011 10 11",
                        symbols=kenobi_symbols),
            coding.Code("0000 0001 0010 0011 0100 0101 0110 0111 1000 1001",
                        symbols=kenobi_symbols),
        ]
    ),
}
fix_sources = (
    'I_LOVE_YOU',
    'ABCABACADACA',
    'ALABAMA',
    'CASABLANCA',
)
urlizer = tools.Argument_URLizer()


def get_fix_source(symbols, words):
    if not isinstance(symbols, (set, frozenset)):
        symbols = set(symbols)
    fix_sources_with_this_symbols = [
        fix_source
        for fix_source in fix_sources
        if set(fix_source) <= symbols
    ]
    if fix_sources_with_this_symbols:
        return "fix." + fix_sources_with_this_symbols[0]


def home(request):
    return render(request, "sources/source.html", {"sources": sources})


def source_detail(request, id):
    source_name, source, codes = sources[int(id)]
    return render(
        request,
        "sources/sourcestat_detail.html",
        {
            "source_name": source_name,
            "source": source,
            "code_list": codes,
            "id": id
        }
    )


def code_stat(source, code, message_length, number_of_samples):
    messages = [source.message(message_length)
                for i in range(number_of_samples)]
    lengths = [len(code.coder(m)) for m in messages]
    stat_values = [sum(lengths) / number_of_samples, max(lengths), min(lengths)]
    per_symbol_values = [value / message_length for value in stat_values]
    CodeStat = collections.namedtuple('CodeStat',
                                      "avg_length max_length min_length "
                                      "avg_length_sym max_length_sym "
                                      "min_length_sym message_length "
                                      "number_of_samples".split())
    all_values = stat_values + per_symbol_values + \
        [message_length, number_of_samples]
    return CodeStat(*all_values)


def sourcestat_default(request, id, code_number):
    source_name, source, codes = sources[int(id)]
    code = codes[int(code_number)-1]
    code_stat_values = code_stat(source, code,
                                 message_length=100, number_of_samples=50)
    return render(
        request,
        "sources/sourcestat_detail.html",
        {
            "source_name": source_name,
            "source": source,
            "code": code,
            "code_number": code_number,
            "id": id,
            "code_stat_values": code_stat_values,
        }
    )


def simple_chain(request, source_number, code_number, channel):
    source_name, source, codes = sources[int(source_number)]
    code = codes[int(code_number)-1]
    channel = coding.Channel(channel)
    chain = coding.Chain(source, code, channel)
    chain.run()
    run = chain.runs[0]
    return render(
        request,
        "sources/chain.html",
        {
            "source": source,
            "source_description": urlizer.to_url(str(source)),
            "code": str(code),
            "channel": channel,
            "channel_description_with_hamming":
                channel.description,
            "hamming_block_length": None,
            "linearized_outputs":
                tools.colorize_and_linearize_outputs(run.outputs),
            "fix_source":
                get_fix_source(source.symbols, fix_sources)
        }
    )


def general_chain(request, source_description,
                  code_description, channel_description,
                  hamming_block_length):
    source = tools.get_source(urlizer.from_url(source_description))
    code = tools.get_code(code_description)
    assert set(code.symbols) >= set(source.symbols)
    channel = tools.get_channel(channel_description)

    elements = [source, code, channel]
    if hamming_block_length:
        hamming_block_length = hamming_block_length[:-1]
        elements.insert(-1, coding.Hamming(int(hamming_block_length)))

    channel_description_with_hamming = channel.description
    if hamming_block_length:
        channel_description_with_hamming += ("/" + hamming_block_length)

    chain = coding.Chain(*elements)
    chain.run()
    run = chain.runs[0]
    return render(
        request,
        "sources/chain.html",
        {
            "source": source,
            "source_description": urlizer.to_url(str(source)),
            "code": str(code),
            "channel": channel,
            "channel_description_with_hamming":
                channel_description_with_hamming,
            "linearized_outputs":
                tools.colorize_and_linearize_outputs(run.outputs),
            "fix_source":
                get_fix_source(source.symbols, fix_sources),
            "hamming_block_length": hamming_block_length,
        }
    )


def change_source(request, source_description, code_description):
    pass


def change_code(request, source_description, code_description):
    pass


def change_error_handler(request, source_description, code_description):
    pass


def change_communication_system(
    request,
    source_description, code_description,
    channel_description_with_hamming,
    element_to_change
):
    channel_description = request.POST['channel_description']
    splitted_channel = channel_description_with_hamming.split('/')
    if len(splitted_channel) == 2:
        hamming_block_length = splitted_channel[1] + '/'
    elif len(splitted_channel) == 1:
        hamming_block_length = None

    return redirect(
        general_chain,
        source_description,
        code_description,
        channel_description,
        hamming_block_length,
    )
